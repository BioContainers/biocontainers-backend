import datetime
import logging
import os

from pymodm import connect
from pymongo.errors import DuplicateKeyError
from sklearn.feature_extraction.text import TfidfVectorizer

from biocontainers.common.models import MongoToolVersion, ContainerImage, MongoTool, _CONSTANT_TOOL_CLASSES, \
    MongoWorkflow, Publication, SimilarTool
from biocontainers.conda.conda_metrics import CondaMetrics
from biocontainers.github.models import LocalGitReader

logger = logging.getLogger('biocontainers.quayio.models')
QUAYIO_DOMAIN = "quay.io/biocontainers/"
DOCKER_DOMAIN = "biocontainers/"

BIOCONTAINERS_USER = "BioContainers Core Team <biodocker@gmail.com>"
BICONDA_USER = "BioConda Core Team <https://github.com/bioconda/bioconda-recipes/issues>"

TOOL_VERSION_SPLITTER = '-'

NOT_AVAILABLE = "Not available"


class InsertContainers:

    def __init__(self, connect_url):
        connection = connect(connect_url)

    @staticmethod
    def compute_similarity():
        tool_ids = []
        descriptions = []
        tools = list(MongoTool.get_all_tools())
        count = 0
        for tool in tools:
            tool.build_complete_metadata()
            tool_ids.append({"index":count, "id":tool.id, "description":tool.additional_metadata})
            count = count + 1
            descriptions.append(tool.additional_metadata)
        dic_results = []
        vect = TfidfVectorizer(min_df=1)
        tfidf = vect.fit_transform(descriptions)
        results = (tfidf * tfidf.T).A
        print(results)
        for i in range(0 , len(tool_ids) -1):
            similars = []
            for j in range(0, len(tool_ids) -1):
                if i != j and results[i][j] > 0.2:
                    similars.append({"id": tool_ids[j]["id"], "score": (results[i][j]) * 100})
            dic_results.append({"id": tool_ids[i]["id"], "similars": similars})
            print(i)
        for result in dic_results:
            similar = SimilarTool()
            similar.id = result['id']
            for a in result['similars']:
                similar.add_similar(a['id'], a['score'])
            similar.save()

    @staticmethod
    def insert_quayio_containers(quayio_containers):
        """
        This method provide the mechanism to insert quayio containers into the Mongo Database
        :param quayio_containers: List of Quay.io containers
        :return:
        """
        list_versions = list(MongoToolVersion.get_all_tool_versions())
        tool_versions_dic = {}
        for tool_version in list_versions:
            tool_versions_dic[tool_version.id] = tool_version

        tools_dic = {}
        list_tools = list(MongoTool.get_all_tools())
        for tool in list_tools:
            tools_dic[tool.id] = tool

        for container in quayio_containers:
            # The version is read from the container tag.
            version_list = []
            current_tool = None
            for key, val in container.tags().items():

                # First insert Tool version containers. For that we need to parse first the version of the tool. Version is also handle as defined by
                # the container provider Docker or Quay.io

                version = key.split("--", 1)[0]
                tool_version_id = container.name() + TOOL_VERSION_SPLITTER + version
                if tool_version_id not in tool_versions_dic:
                    mongo_tool_version = MongoToolVersion()
                    mongo_tool_version.name = container.name()
                    mongo_tool_version.version = version
                    mongo_tool_version.description = container.description()
                    mongo_tool_version.organization = container.organization()
                    if "mulled-v2" not in mongo_tool_version.name:
                        mongo_tool_version.tool_classes = [_CONSTANT_TOOL_CLASSES['CommandLineTool']]
                    else:
                        mongo_tool_version.tool_classes = [_CONSTANT_TOOL_CLASSES['CommandLineMultiTool']]
                    mongo_tool_version.id = tool_version_id
                    mongo_tool_version.add_author(BIOCONTAINERS_USER)
                    mongo_tool_version.add_author(BICONDA_USER)
                else:
                    mongo_tool_version = tool_versions_dic[tool_version_id]

                ## Add only one conda package for each version
                if key not in version_list:
                    container_image = ContainerImage()
                    container_image.tag = "conda:" + key
                    container_image.full_tag = container.name() + "==" + key
                    container_image.container_type = 'CONDA'
                    container_image.size = 0
                    container_image.downloads = 0
                    mongo_tool_version.add_image_container(container_image)
                    version_list.append(key)

                ## Add container
                container_image = ContainerImage()
                container_image.tag = key
                container_image.full_tag = QUAYIO_DOMAIN + container.name() + ":" + key
                container_image.container_type = 'DOCKER'
                datetime_object = datetime.datetime.strptime(val['last_modified'][0:-15], '%a, %d %b %Y')
                container_image.last_updated = datetime_object
                container_image.size = int(int(val['size']))
                container_image.downloads = 0
                mongo_tool_version.add_image_container(container_image)

                tool_versions_dic[tool_version_id] = mongo_tool_version

                # Insert the corresponding tool
                tool_id = container.name()
                if tool_id not in tools_dic:
                    mongo_tool = MongoTool()
                    mongo_tool.name = container.name()
                    if "mulled-v2" not in mongo_tool_version.name:
                        mongo_tool.tool_classes = [_CONSTANT_TOOL_CLASSES['CommandLineTool']]
                    else:
                        mongo_tool.tool_classes = [_CONSTANT_TOOL_CLASSES['CommandLineMultiTool']]
                    mongo_tool.id = container.name()
                    mongo_tool.description = container.description()
                    mongo_tool.add_authors(mongo_tool_version.authors)
                    mongo_tool.organization = container.organization()
                    mongo_tool.checker = container.checker()
                else:
                    mongo_tool = tools_dic[tool_id]

                mongo_tool.add_registry(container.registry())
                mongo_tool.add_alias(container.alias())
                tools_dic[tool_id] = mongo_tool

                try:
                    mongo_tool.save()
                    current_tool = mongo_tool
                except DuplicateKeyError as error:
                    logger.error(" A tool with same name is already in the database -- " + tool_id)

                mongo_tool_version.ref_tool = mongo_tool

                try:
                    mongo_tool_version.save()
                except DuplicateKeyError as error:
                    logger.error(
                        " A tool version with a same name and version is in the database -- " + tool_version_id)

            if current_tool is not None:
                count = 0
                for stat in container.pulls():
                    count = count + stat['count']
                current_tool.add_pull_provider("quay.io", count)
                current_tool.save()
        containers_list = list(tool_versions_dic.values())

    @staticmethod
    def insert_dockerhub_containers(dockerhub_containers):
        """
                This method provide the mechanism to insert dockerhub containers into the Mongo Database
                :param dockerhub_containers: List of DockerHub containers
                :return:
                """
        list_versions = list(MongoToolVersion.get_all_tool_versions())
        tool_versions_dic = {}
        for tool_version in list_versions:
            tool_versions_dic[tool_version.id] = tool_version

        tools_dic = {}
        list_tools = list(MongoTool.get_all_tools())
        for tool in list_tools:
            tools_dic[tool.id] = tool

        for container in dockerhub_containers:
            # The version is read from the container tag.
            current_tool = None
            for key in container.tags:

                # First insert Tool version containers. For that we need to parse first the version of the tool. Version is also handle as defined by
                # the container provider Docker or Quay.io

                version = key['name'].split("_", 1)[0]
                tool_version_id = container.name() + TOOL_VERSION_SPLITTER + version
                if tool_version_id not in tool_versions_dic:
                    mongo_tool_version = MongoToolVersion()
                    mongo_tool_version.name = container.name()
                    mongo_tool_version.version = version
                    mongo_tool_version.description = container.description()
                    mongo_tool_version.tool_classes = [_CONSTANT_TOOL_CLASSES['CommandLineTool']]
                    mongo_tool_version.id = tool_version_id
                    mongo_tool_version.add_author(BIOCONTAINERS_USER)
                    mongo_tool_version.organization = container.organization()
                else:
                    mongo_tool_version = tool_versions_dic[tool_version_id]

                ## Get the tag information (Container image) and add to the ToolVersion
                container_image = ContainerImage()
                container_image.tag = key
                container_image.full_tag = DOCKER_DOMAIN + container.name() + ":" + key['name']

                container_image.container_type = 'DOCKER'
                datetime_object = datetime.datetime.strptime(key['last_updated'][0:10], '%Y-%m-%d')
                container_image.last_updated = datetime_object
                container_image.size = int(int(key['full_size']))
                mongo_tool_version.add_image_container(container_image)
                tool_versions_dic[tool_version_id] = mongo_tool_version

                # Insert the corresponding tool
                tool_id = container.name()
                if tool_id not in tools_dic:
                    mongo_tool = MongoTool()
                    mongo_tool.name = container.name()
                    mongo_tool.id = container.name()
                    mongo_tool.description = container.description()
                    mongo_tool.tool_classes = [_CONSTANT_TOOL_CLASSES['CommandLineTool']]
                    tools_dic[tool_id] = mongo_tool
                    mongo_tool.add_authors(mongo_tool_version.authors)
                    mongo_tool.organization = container.organization()
                    mongo_tool.checker = container.checker()
                else:
                    mongo_tool = tools_dic[tool_id]

                mongo_tool.add_registry(container.registry())
                mongo_tool.add_alias(container.alias())
                tools_dic[tool_id] = mongo_tool

                try:
                    mongo_tool.save()
                    current_tool = mongo_tool
                except DuplicateKeyError as error:
                    logger.error(" A tool with same name is already in the database -- " + tool_id)

                mongo_tool_version.ref_tool = mongo_tool
                # mongo_versions = mongo_tool.get_tool_versions()

                try:
                    mongo_tool_version.save()
                except DuplicateKeyError as error:
                    logger.error(
                        " A tool version with a same name and version is in the database -- " + tool_version_id)

            if current_tool is not None:
                current_tool.add_pull_provider("dockerhub", container.get_pull_count())
                current_tool.save()

        containers_list = list(tool_versions_dic.values())

    @staticmethod
    def insert_singularity_containers(singularity_containers):
        """
                This method provide the mechanism to insert Singularity containers into the Mongo Database
                :param singularity_containers: List of Singularity containers
                :return:
                """
        for key in singularity_containers.keys():
            tool_version = MongoToolVersion.get_tool_version_by_id(key)
            if tool_version is not None:
                update = False
                image_containers = tool_version.image_containers
                for i in singularity_containers[key]:
                    found = False
                    for j in image_containers:
                        if i.full_tag == j.full_tag:
                            found = True
                            break
                    if not found:
                        update = True
                        tool_version.image_containers.append(i)
                        logger.info("Added singularity image: " + i.tag + "to tool version: " + key)

                if update:
                    tool_version.save()

    @staticmethod
    def update_multi_package_containers(mulled_entries):
        for entry in mulled_entries:
            mulled_name = os.path.splitext(entry.file_name)[0]
            mulled_tool_name = mulled_name.split(':')[0]
            tools_array = entry.file_contents.split(',')
            aliases = []
            for tool in tools_array:
                aliases.append(tool.split('=')[0])

            MongoTool.manager.exec_update_query({"id": mulled_tool_name},
                                                {"$addToSet":
                                                    {
                                                        "contains": {"$each": tools_array},
                                                        "aliases": {"$each": aliases}
                                                    }
                                                })

            # collection "tool_version: id" field has "-" instead of ":" as a separator between tool-name & version
            mulled_name = mulled_name.replace(":", "-")
            MongoToolVersion.manager_versions.exec_update_query({"id": mulled_name},
                                                                {"$set":
                                                                     {"contains": tools_array,
                                                                      "aliases": aliases
                                                                      }
                                                                 })

    @staticmethod
    def annotate_docker_containers(docker_recipes):
        for entry in docker_recipes:
            logger.info("Annotating the recipe -- " + entry['name'])
            name = entry['name']
            name_parts = name.split("/")
            tool_version_id = name_parts[0] + "-v" + name_parts[1]
            tool_id = name_parts[0]
            tool_version = MongoToolVersion.get_tool_version_by_id(tool_version_id)
            tool = MongoTool.get_tool_by_id(tool_id)
            if tool_version is not None:
                if entry["recipe"].get_description() is not None:
                    tool_version.description = entry["recipe"].get_description().capitalize()
                if entry['recipe'].get_home_url() is not None:
                    tool_version.home_url = entry['recipe'].get_home_url()
                if entry['recipe'].get_license() is not None:
                    tool_version.license = entry['recipe'].get_license()
                else:
                    tool_version.license = NOT_AVAILABLE
                tool_version.save()
                logger.info("Updated tool version description of -- " + tool_version_id)
            if tool is not None:
                if entry["recipe"].get_description() is not None:
                    tool.description = entry["recipe"].get_description().capitalize()
                if entry['recipe'].get_home_url() is not None:
                    tool.home_url = entry['recipe'].get_home_url()
                if entry['recipe'].get_license() is not None:
                    tool.license = entry['recipe'].get_license()
                else:
                    tool.license = NOT_AVAILABLE
                if entry['recipe'].get_tags() is not None:
                    tool.tool_tags = entry['recipe'].get_tags()
                if entry['recipe'].get_additional_ids() is not None:
                    tool.add_additional_identifiers(entry['recipe'].get_additional_ids())
                tool.save()
                logger.info("Updated tool description of -- " + tool_version_id)

    @staticmethod
    def annotate_quayio_containers(conda_recipes):
        for entry in conda_recipes:
            logger.info("Annotating the recipe -- " + entry['name'])
            tool_version_id = None
            if (entry['recipe'].get_name() is not None) and (entry['recipe'].get_version() is not None) \
                    and ("{" not in entry['recipe'].get_name()) \
                    and ("|" not in entry['recipe'].get_name()) and ("{" not in entry['recipe'].get_version()) \
                    and ("|" not in entry['recipe'].get_version()):
                tool_version_id = (entry['recipe'].get_name() + "-" + entry['recipe'].get_version()).lower()
                tool_id = entry['recipe'].get_name().lower()
                tool_version = MongoToolVersion.get_tool_version_by_id(tool_version_id)
                tool = MongoTool.get_tool_by_id(tool_id)
                if tool_version is not None:
                    if entry["recipe"].get_description() is not None:
                        tool_version.description = entry["recipe"].get_description().capitalize()
                    if entry['recipe'].get_home_url() is not None:
                        tool_version.home_url = entry['recipe'].get_home_url()
                    if entry['recipe'].get_license() is not None and len(entry['recipe'].get_license()) > 0:
                        tool_version.license = entry['recipe'].get_license()
                    else:
                        tool_version.license = NOT_AVAILABLE
                    tool_version.save()
                    logger.info("Updated tool version description of -- " + tool_version_id)
                if tool is not None:
                    if entry["recipe"].get_description() is not None:
                        tool.description = entry["recipe"].get_description().capitalize()
                    if entry['recipe'].get_home_url() is not None:
                        tool.home_url = entry['recipe'].get_home_url()
                    if entry['recipe'].get_license() is not None and bool(entry['recipe'].get_license()):
                        tool.license = entry['recipe'].get_license()
                    if entry['recipe'].get_biotool_ids() is not None:
                        tool.add_additional_identifiers(entry['recipe'].get_biotool_ids())
                    else:
                        tool.license = NOT_AVAILABLE

                    tool.save()
                    logger.info("Updated tool description of -- " + tool_version_id)

            logger.info("The following tool has been analyzed -- " + str(tool_version_id))

    @staticmethod
    def annotate_conda_recipes():
        conda_helper = CondaMetrics()
        mongo_versions = MongoToolVersion.get_all_tool_versions()
        tools = []
        for tool_version in mongo_versions:
            count = 0
            tool_not_found = True
            for tool in tools:
                if tool['id'] == tool_version.name:
                    count = tool['count']
                    tool_not_found = False

            old_images = []
            for image in tool_version.image_containers:
                if image.container_type == 'CONDA':
                    annotations = conda_helper.get_number_downloas_by_version(tool_version.name, tool_version.version)
                    image.downloads = annotations['downloads']
                    count = count + image.downloads
                    image.size = annotations['size']
                    if annotations['last_update'][0:10] is not None and bool(annotations['last_update'][0:10].strip()):
                        image.last_updated = annotations['last_update'][0:10]
                    # else:
                    #     image.last_updated = None
                    print(annotations)
                old_images.append(image)
            tool_version.image_containers = old_images

            if tool_not_found and count > 0:
                tools.append({"id": tool_version.name, "count":count})
            else:
                for tool in tools:
                    if tool['id'] == tool_version.name:
                        tool['count'] = count
            tool_version.save()
        print(tools)
        for stat in tools:
            tool = MongoTool.get_tool_by_id(stat['id'])
            tool.add_pull_provider("conda", stat['count'])
            tool.save()


    @staticmethod
    def annotate_biotools_metadata(tools_recipes):
        global tool_id
        for entry in tools_recipes:
            logger.info("Annotating the recipe -- " + entry['name'])
            if entry['recipe'].get_id() is not None:
                tool_id = entry['recipe'].get_id()
                tools = MongoTool.get_tool_by_additional_id("biotools:" + tool_id)
                if len(tools) > 0 and tools[0] is not None:
                    tool = tools[0]
                    found = False
                    for id in tool.additional_identifiers:
                        if id in ("biotools:" + tool_id):
                            found = True
                    if found:
                        if entry["recipe"].get_description() is not None:
                            tool.description = entry["recipe"].get_description().capitalize()
                        if entry['recipe'].get_home_url() is not None:
                            tool.home_url = entry['recipe'].get_home_url()
                        if entry['recipe'].get_license() is not None and bool(entry['recipe'].get_license()):
                            tool.license = entry['recipe'].get_license()
                        if entry['recipe'].get_references() is not None:
                            for reference in entry['recipe'].get_references():
                                publication = Publication()
                                if 'pmcid' in reference and reference['pmcid'] is not None:
                                    publication.pmc_id = reference['pmcid']
                                if 'pmid' in reference and reference['pmid'] is not None:
                                    publication.pubmed_id = reference['pmid']
                                if 'doi' in reference and reference['doi'] is not None:
                                    publication.doi = reference['doi']

                                if 'metadata' in reference and reference['metadata'] is not None:
                                    if 'title' in reference['metadata'] and reference['metadata']['title']:
                                        publication.title = reference['metadata']['title']
                                    if 'abstract' in reference['metadata'] and reference['metadata']['abstract'] is not None and len((reference['metadata']['abstract']).strip()) > 0:
                                        publication.abstract = reference['metadata']['abstract']
                                    if 'citationCount' in reference['metadata'] and reference['metadata']['citationCount'] is not None:
                                        publication.citation_count = reference['metadata']['citationCount']
                                    if 'journal' in reference['metadata'] and reference['metadata']['journal'] is not None:
                                        publication.journal = reference['metadata']['journal']
                                    if 'date' in reference['metadata'] and reference['metadata']['date']:
                                        publication.publication_date = reference['metadata']['date']
                                    if 'authors' in reference['metadata'] and reference['metadata']['authors'] is not None:
                                        for author in reference['metadata']['authors']:
                                            publication.add_author(author['name'])

                                tool.add_publication(publication)
                        tool.build_complete_metadata()
                        tool.save()
                        logger.info("Updated tool description of -- " + tool_id)

            logger.info("The following tool has been analyzed -- " + str(tool_id))


    @staticmethod
    def annotate_workflows(config, config_profile):
        logger_local = logging.getLogger('annotate_workflows')
        github_local = config[config_profile]['GITHUB_LOCAL_REPO']
        mongo_workflows = MongoWorkflow.get_all_workflows()
        for workflow in mongo_workflows:
            try:
                InsertContainers.annotate_workflow(workflow, github_local)
            except Exception as e:
                logger_local.error("Error while cloning repo: " + workflow.git_repo)
                continue

    @staticmethod
    def annotate_workflow(workflow, github_local):
        logger_local = logging.getLogger('annotate_workflow')
        git_repo = workflow.git_repo
        logger_local.info("Annotating the Workflow : " + git_repo)
        github_reader = LocalGitReader(git_repo, github_local)
        github_reader.clone_url()
        files = github_reader.get_list_files(github_local)
        containers = []
        for file in files:
            if file.endswith(".nf"):
                # print(file)
                with open(file, "r") as file_contents:
                    for line in file_contents:
                        line = line.strip()
                        container = None
                        if line.startswith("container "):  # container  xyz OR container = xyz
                            splits = line.split()
                            if len(splits) == 2:  # container  xyz
                                container = splits[1]
                            elif len(splits) == 3 and splits[1] == '=':  # container = xyz
                                container = splits[2]
                        elif line.startswith("container="):  # container=xyz
                            splits = line.split("=")
                            if len(splits) == 2:
                                container = splits[1]

                        if container is not None:
                            container = container.replace("'", "").replace('"', "")
                            if container not in containers:
                                containers.append(container)

        workflow.containers = containers
        workflow.save()

    def get_missing_info_tools(self):
        list_tools = list(MongoTool.get_all_tools())
        to_map = []

        for tool in list_tools:
            export = False
            if tool.description is None or len(tool.description) == 0:
                export = True
            if tool.license is None or tool.license.upper() == 'NOT AVAILABLE':
                export = True
            if tool.home_url is None or len(tool.home_url) == 0:
                export = True
            to_map.append(tool)
        return to_map

    def update_from_file(self, file_annotations):
        for key in file_annotations:
            tool_file = file_annotations[key]
            if 'manually_check' in tool_file and tool_file['manually_check'] and tool_file['manually_check'] == True:
                mongo_tool = MongoTool.get_tool_by_id(key)
                changed = False
                if mongo_tool is not None:
                    if mongo_tool.description != tool_file['description']:
                        mongo_tool.description = tool_file['description']
                        changed = True
                    if mongo_tool.license != tool_file['license']:
                        mongo_tool.license = tool_file['license']
                        changed = True
                    if mongo_tool.home_url != tool_file['home_url']:
                        mongo_tool.home_url = tool_file['home_url']
                        changed =True
                    if changed:
                        mongo_tool.save()
                        logger.info("The tool has been updated  " + key)


