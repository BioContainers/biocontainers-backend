import logging
import os
import shutil
import subprocess
import sys

import requests

import base64
import json

from jinja2 import Environment
from ruamel.yaml import YAML

from yaml.constructor import ConstructorError
from yaml.scanner import ScannerError

from dockerfile_parse import DockerfileParser
import tempfile

from biocontainers.common.utils import call_api

logger = logging.getLogger('biocontainers.github.models')
logging.basicConfig(level=logging.INFO)


class CondaRecipe:
    def __init__(self, attributes):
        self.attributes = attributes

    def description(self):
        return self.attributes['about']['summary']

    def get_description(self):
        if 'about' in self.attributes and 'summary' in self.attributes['about']:
            return self.attributes['about']['summary']
        return None

    def get_home_url(self):
        if 'about' in self.attributes and 'home' in self.attributes['about']:
            return self.attributes['about']['home']
        return None

    def get_license(self):
        if 'about' in self.attributes and 'license' in self.attributes['about'] and self.attributes['about'][
            'license'] is not None:
            return (self.attributes['about']['license']).strip()
        return None

    def get_version(self):
        if 'package' in self.attributes and 'version' in self.attributes['package']:
            return str(self.attributes['package']['version'])
        return None

    def get_name(self):
        if 'package' in self.attributes and 'name' in self.attributes['package']:
            return self.attributes['package']['name']
        return None

    def get_biotool_ids(self):
        if 'extra' in self.attributes and 'identifiers' in self.attributes['extra']:
            id_strings = self.attributes['extra']['identifiers']
            ids = []
            for id in id_strings:
                if 'biotools' in id:
                    ids.append(id)
            if len(ids) > 0:
                return ids;

        return None


class DockerRecipe:
    def __init__(self, attributes):
        self.attributes = attributes

    def get_description(self):
        if 'about.summary' in self.attributes.labels:
            return self.attributes.labels['about.summary']
        return None

    def get_home_url(self):
        if 'about.home' in self.attributes.labels:
            return self.attributes.labels['about.home']
        return None

    def get_license(self):
        if 'about.license' in self.attributes.labels:
            return self.attributes.labels['about.license']
        return None

    def get_additional_ids(self):
        ids = []
        if 'extra.identifiers.biotools' in self.attributes.labels:
            ids.append("biotools:" + self.attributes.labels['extra.identifiers.biotools'])
            return ids

    def get_tags(self):
        """
        This function returns the different tags added to
        :return:
        """
        if 'about.tags' in self.attributes.labels:
            final_tags = []
            tags = self.attributes.labels['about.tags']
            all_tags = tags.split(",")
            for tag in all_tags:
                tag_values = tag.split(":")
                value = tag_values[len(tag_values) - 1]
                if len(value) > 0:
                    final_tags.append(value.lower())
            if len(final_tags) > 0:
                return final_tags
        return None


class ToolRecipe:

    def __init__(self):
        self.attributes = {}

    def __init__(self, attributes = {}):
        self.attributes = attributes

    def get_description(self):
        if 'description' in self.attributes:
            return self.attributes['description']
        return None

    def get_home_url(self):
        if 'homepage' in self.attributes:
            return self.attributes['homepage']
        return None

    def get_license(self):
        if 'license' in self.attributes and self.attributes['license'] is not None:
            return (self.attributes['license']).strip()
        return None

    def get_id(self):
        if 'biotoolsID' in self.attributes:
            return self.attributes['biotoolsID']
        return None

    def get_publications(self):
        if 'publication' in self.attributes:
            return self.attributes['publication']
        return None

    def get_topics(self):
        if 'topic' in self.attributes:
            return self.attributes['topic']
        return None

    def get_references(self):
        if 'publication' in self.attributes:
            return self.attributes['publication']
        return None



class GitHubConfiguration:
    """
    This class contains the information to configure a GitHub interaction for docker/conda recipes
    """

    def __init__(self, repository_recursive_url, repository_readable_url):
        self.repository_recursive_url = repository_recursive_url
        self.repository_readable_url = repository_readable_url
        self.use_api = False

    def use_api(self, use_api):
        self.use_api = use_api


class GitHubDockerReader:
    """
        This class contains the methods needed to Read the Conda Recipes from GitHub
        """
    docker_github_files = []
    docker_recipes = []

    def __init__(self, github_config):
        self.github_config = github_config

    @staticmethod
    def get_dockerfile_reader(content):
        """
        This method retrieve the corresponding Docker Reader
        :return:
        """
        with tempfile.TemporaryDirectory() as tmp_directory:
            fout = open(tmp_directory + '/Dockerfile', 'w')
            fout.write(content)
            fout.close()
            return DockerfileParser(path=tmp_directory, cache_content=True)

    def get_list_recipes(self):
        """
        This method retrirve all the docker file recipes in Biocontainers
        :return:
        """
        string_url = self.github_config.repository_recursive_url
        response = requests.get(string_url)
        self.docker_github_files = []
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            for key in json_data['tree']:
                if key['path'].endswith('Dockerfile'):
                    self.docker_github_files.append({'path': key['path'], 'url': key['url']})

        return self.docker_github_files

    def read_docker_recipes(self):
        """
        This method allow to retrieve the information of each docker recipe  in a list self.conda_recipes
        :return:
        """
        if not self.docker_github_files:
            self.docker_github_files = self.get_list_recipes()

        self.docker_recipes = []
        for key in self.docker_github_files:
            logger.info(key['path'])
            if self.github_config.use_api:
                response = requests.get(key['url'])
                if response.status_code == 200:
                    json_data = json.loads(response.content.decode('utf-8'))
                    hash_content = json_data['content']
                    content = base64.b64decode(hash_content).decode("utf-8")
                    try:
                        yaml_content = self.get_dockerfile_reader(content)
                        recipe = DockerRecipe(yaml_content)
                        entry = {'name': key['path'], 'recipe': recipe}
                        self.docker_recipes.append(entry)
                        logger.info(key['path'])
                    except (ScannerError, ConstructorError, TypeError, AttributeError) as error:
                        logger.error("Error reading conda definition of tool -- " + key['path'] + " " + error)
            else:
                string_url = self.github_config.repository_readable_url.replace("%recipe_software_tool_name%",
                                                                                key['path'])
                response = requests.get(string_url)
                if response.status_code == 200:
                    try:
                        json_data = response.content.decode('utf-8')
                    except (ScannerError, ConstructorError, TypeError, AttributeError):
                        json_data = response.content.decode('latin-1')
                        json_data = json_data.decode('utf-8')

                    yaml_content = self.get_dockerfile_reader(json_data)
                    recipe = DockerRecipe(yaml_content)
                    entry = {'name': key['path'], 'recipe': recipe}
                    self.docker_recipes.append(entry)

        return self.docker_recipes


class GitHubCondaReader:
    """
    This class contains the methods needed to Read the Conda Recipes from GitHub
    """
    conda_github_files = []
    conda_recipes = []

    def __init__(self, github_config):
        self.github_config = github_config

    @staticmethod
    def init_yaml():
        """
        This static method return a yml reader for jinja2 templates
        :return:
        """
        yaml = YAML(typ='safe')
        return yaml

    def get_list_recipes(self):
        string_url = self.github_config.repository_recursive_url
        response = requests.get(string_url)
        self.conda_github_files = []
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            for key in json_data['tree']:
                if key['path'].endswith('meta.yaml') or key['path'].endswith('meta.yml'):
                    self.conda_github_files.append({'path': key['path'], 'url': key['url']})

        return self.conda_github_files

    def read_conda_recipe(self, name, version):
        """
        Read the specific Conda recipe for one conda package
        :param name: name of the conda package
        :param version:  version of the conda package
        :return:
        """
        if not self.conda_github_files:
            self.conda_github_files = self.get_list_recipes()

        yaml = self.init_yaml()
        recipe = None
        for key in self.conda_github_files:
            if name in key['path'] and version in key['path']:
                if self.github_config.use_api:
                    response = requests.get(key['url'])
                    if response.status_code == 200:
                        json_data = json.loads(response.content.decode('utf-8'))
                        hash_content = json_data['content']
                        content = base64.b64decode(hash_content).decode("utf-8")
                        try:
                            yaml_content = yaml.load(content)

                            recipe = CondaRecipe(yaml_content)
                        except (ScannerError, ConstructorError, TypeError, AttributeError) as error:
                            logger.error("Error reading conda definition of tool -- " + name + " " + error)
                    else:
                        logger.debug("Error connecting to GitHub API -- " + response.status_code)
                else:
                    string_url = self.github_config.repository_readable_url.replace("%recipe_software_tool_name%",
                                                                                    key['path'])
                    response = requests.get(string_url)
                    if response.status_code == 200:
                        json_data = response.content.decode('utf-8')
                        yaml_content = yaml.load(json_data)
                        recipe = CondaRecipe(yaml_content)

        return recipe

    def read_conda_recipes(self):
        """
        This method allow to retrieve the information of each recipe in a list self.conda_recipes
        :return:
        """
        if not self.conda_github_files:
            self.conda_github_files = self.get_list_recipes()

        yaml = self.init_yaml()
        self.conda_recipes = []

        for key in self.conda_github_files:
            logger.info(key['path'])
            if len(self.conda_recipes) > 50:
                continue
            if self.github_config.use_api:
                response = call_api(key['url'])
                if response.status_code == 200:
                    json_data = json.loads(response.content.decode('utf-8'))
                    hash_content = json_data['content']
                    content = base64.b64decode(hash_content).decode("utf-8")
                    try:
                        yaml_content = yaml.load(content)
                        recipe = CondaRecipe(yaml_content)
                        entry = {'name': key['path'], 'recipe': recipe}
                        self.conda_recipes.append(entry)
                        logger.info(key['path'])
                    except (ScannerError, ConstructorError, TypeError, AttributeError) as error:
                        logger.error("Error reading conda definition of tool -- " + key['path'] + " " + error)
            else:
                string_url = self.github_config.repository_readable_url.replace("%recipe_software_tool_name%",
                                                                                key['path'])
                response = call_api(string_url)
                if response.status_code == 200:
                    try:
                        json_data = response.content.decode('utf-8')
                    except (ScannerError, ConstructorError, TypeError, AttributeError):
                        json_data = response.content.decode('latin-1')
                        json_data = json_data.decode('utf-8')
                    try:
                        yaml_content = yaml.load(Environment().from_string(json_data).render())
                        recipe = CondaRecipe(yaml_content)
                        entry = {'name': key['path'], 'recipe': recipe}
                        self.conda_recipes.append(entry)
                    except:
                        logger.error("An error parsing the yaml file of -- " + string_url)

        return self.conda_recipes


class MulledEntry:
    def __init__(self, file_name, file_contents):
        self.file_name = file_name
        self.file_contents = file_contents


class GitHubMulledReader:
    """
    This class contains the methods needed to Read the Mulled files from GitHub
    """
    local_logger = logging.getLogger('MulledReader')

    def __init__(self, github_config):
        self.mulled_files = []
        self.mulled_entries = []
        self.github_config = github_config

    def get_files(self):
        """
        This method returns list of all mulled file names from Github.
        :return: list of all mulled file names
        """
        string_url = self.github_config.repository_recursive_url
        GitHubMulledReader.local_logger.info("Sending request : " + string_url)
        response = requests.get(string_url)
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            for file in json_data:
                name = file['name']
                if name.startswith("mulled"):
                    self.mulled_files.append(name)
        return self.mulled_files

    def get_mulled_entries(self):
        """
        This method returns list of all mulled file names & its contents from Github.
        :return: list of all mulled file names & its contents
        """
        if not self.mulled_files:
            self.mulled_files = self.get_files()

        for file_name in self.mulled_files:
            string_url = self.github_config.repository_readable_url.replace("%file_name%",
                                                                            file_name)
            GitHubMulledReader.local_logger.info("Sending request : " + string_url)
            response = requests.get(string_url)
            if response.status_code == 200:
                json_data = response.content.decode('utf-8')
                self.mulled_entries.append(MulledEntry(file_name, json_data))

        return self.mulled_entries


class LocalGitReader:

    def __init__(self, repo_url, local_folder):
        self._repo_url = repo_url
        self._absolute_local_folder = local_folder
        self._conda_recipes = []
        self._conda_github_files = []

    def clone_url(self):
        logger.info("Cloning the following repo -- " + self._repo_url)
        if os.path.exists(self._absolute_local_folder):
            shutil.rmtree(self._absolute_local_folder, ignore_errors=True)
        # repo = clone_repository(self._repo_url, self._local_folder)
        pr = subprocess.Popen(['git', 'clone', '--depth=1', str(self._repo_url), self._absolute_local_folder],
                              stdout=subprocess.PIPE)
        for line in pr.stdout:
            logger.info(line)
        logger.info("Repo has been clone -- " + self._repo_url)

    @staticmethod
    def init_yaml():
        """
        This static method return a yml reader for jinja2 templates
        :return:
        """
        yaml = YAML(typ='safe')
        return yaml

    @staticmethod
    def get_list_files(dir_name):
        list_of_files = os.listdir(dir_name)
        all_files = list()
        for entry in list_of_files:
            full_path = os.path.join(dir_name, entry)
            if os.path.isdir(full_path):
                all_files = all_files + LocalGitReader.get_list_files(full_path)
            else:
                all_files.append(full_path)

        return all_files

    def get_list_recipes(self):
        self._conda_github_files = []
        all_files = LocalGitReader.get_list_files(self._absolute_local_folder + "/recipes/")
        for key in all_files:
            if key.endswith('meta.yaml'):
                self._conda_github_files.append(key)
        return self._conda_github_files

    def read_conda_recipes(self):
        """
        This method allow to retrieve the information of each recipe in a list self.conda_recipes
        :return:
        """
        if not self._conda_github_files:
            self._conda_github_files = self.get_list_recipes()

        yaml = self.init_yaml()
        self._conda_recipes = []

        for key in self._conda_github_files:
            logger.info(key)
            try:
                with open(key, 'r') as file:
                    data = file.read()
                yaml_content = yaml.load(Environment().from_string(data).render())
                recipe = CondaRecipe(yaml_content)
                entry = {'name': key, 'recipe': recipe}
                self._conda_recipes.append(entry)
            except:
                logger.error("Error reading conda definition of tool -- " + key)

        return self._conda_recipes

    def read_biotools_recipes(self):
        all_files = LocalGitReader.get_list_files(self._absolute_local_folder + "/")
        yaml = self.init_yaml()
        self._biotools_recipes = []

        for key in all_files:
            if key.endswith('.yaml'):
                self._conda_github_files.append(key)
                logger.info(key)
                try:
                    with open(key, 'r') as file:
                        data = file.read()
                        yaml_content = yaml.load(Environment().from_string(data).render())
                        recipe = ToolRecipe(yaml_content)
                        entry = {'name': key, 'recipe': recipe}
                        logger.info(recipe.get_id() + " , " + recipe.get_description() + " , " + recipe.get_home_url())
                        self._biotools_recipes.append(entry)
                except:
                    logger.error("Error reading conda definition of tool -- " + key)
        return self._biotools_recipes;

    def read_biotools_github_recipes(self):
        all_files = LocalGitReader.get_list_files(self._absolute_local_folder + "/data/")
        self._biotools_recipes = []

        for key in all_files:
            if key.endswith('.biotools.json'):
                self._conda_github_files.append(key)
                logger.info(key)
                try:
                    with open(key, 'r') as file:
                        data = file.read()
                        json_data = json.loads(data)
                        recipe = ToolRecipe(json_data)
                        entry = {'name': key, 'recipe': recipe}
                        logger.info(recipe.get_id() + " , " + recipe.get_description() + " , " + recipe.get_home_url())
                        self._biotools_recipes.append(entry)
                except:
                    logger.error("Error reading conda definition of tool -- " + key)
        return self._biotools_recipes;



if __name__ == "__main__":
    # local_git = LocalGitReader("git@github.com:bioconda/bioconda-recipes.git", "/tmp/bioconda-recipes/")
    # local_git.clone_url()
    # conda_recipes = local_git.read_conda_recipes()

    local_git = LocalGitReader("git@github.com:BioContainers/tools-metadata.git", "/tmp/tools-recipes/")
    local_git.clone_url()
    conda_recipes = local_git.read_biotools_recipes()
