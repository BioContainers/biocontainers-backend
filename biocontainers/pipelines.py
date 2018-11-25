import argparse
import configparser
import logging

import click

from biocontainers.biomongo.helpers import InsertContainers
from biocontainers.dockerhub.models import DockerHubReader
from biocontainers.github.models import GitHubCondaReader, GitHubConfiguration, GitHubDockerReader
from biocontainers.quayio.models import QuayIOReader

logger = logging.getLogger('biocontainers.pipelines')


def get_config(file):
    """
    This method read the default configuration file configuration.ini in the same path of the pipeline execution
    :return:
    """
    config = configparser.ConfigParser()
    config.read(file)
    return config


def import_quayio_containers(config, config_profile):
    """
    Import quayio containers into the registry database
    :param config: Parameters for quayio
    :return:
    """
    logger.info("Starting importing Conda packages")

    reader = QuayIOReader()
    reader.quayio_list_url(config[config_profile]['QUAYIO_CONTAINER_LIST'])
    reader.quayio_details_url(config[config_profile]['QUAYIO_CONTAINER_DETAILS'])
    reader.namespace(config[config_profile]['NAMESPACE'])
    quayio_containers = reader.get_containers(batch=50)

    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.insert_quayio_containers(quayio_containers)


def import_dockerhub_containers(config, config_profile):
    """
    Import dockerhub containers into the registry database
    :param config:
    :return:
    """

    logger.info("Starting importing DockerHub packages")
    reader = DockerHubReader()
    reader.dockerhub_list_url(config[config_profile]['DOCKER_HUB'])
    reader.dockerhub_tags_url(config[config_profile]['DOCKER_HUB_TAG'])
    reader.namespace(config[config_profile]['NAMESPACE'])
    dockerhub_containers = reader.get_containers()

    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.insert_dockerhub_containers(dockerhub_containers)


def annotate_conda_recipes(config, config_profile):
    github_conf = GitHubConfiguration(config[config_profile]['GITHUB_API_CONDA'],
                                      config[config_profile]['GITHUB_CONDA_RECIPES_READABLE'])
    github_reader = GitHubCondaReader(github_conf)
    conda_recipes = github_reader.read_conda_recipes()


def annotate_docker_recipes(config, config_profile):
    github_conf = GitHubConfiguration(config[config_profile]['GITHUB_API_CONDA'],
                                      config[config_profile]['GITHUB_CONDA_RECIPES_READABLE'])
    github_reader = GitHubDockerReader(github_conf)
    conda_recipes = github_reader.read_docker_recipes()


@click.command()
@click.option('--import-quayio',     '-q', help='Import Quay.io Recipes', is_flag=True)
@click.option('--import-docker',     '-k', help="Import Docker Recipes", is_flag=True)
@click.option('--config-file',       '-c', type=click.Path(), default='configuration.ini')
@click.option('--database-uri',      '-d', help="Mongo Database URI (e.g. mongodb://localhost:27017/testdb)", envvar='BICONTAINERS_DATABASE_URI')
@click.option('--database-user',     '-u', help="Mongo database username", envvar='BICONTAINERS_DATABASE_USER')
@click.option('--database-password', '-p', help="Mongo database password", envvar='BICONTAINERS_DATABASE_PASSWORD')
@click.option('--config-profile',    '-a', help="This option allow to select a config profile", default='PRODUCTION')
def main(import_quayio, import_docker, config_file, database_uri, database_user, database_password, config_profile):
    config = get_config(config_file)
    if config[config_profile]['VERBOSE'] == "True":
        for key in config[config_profile]:
            print(key + "=" + config[config_profile][key])

    if import_quayio is not False:
        import_quayio_containers(config, config_profile)

    if import_docker is not False:
        import_dockerhub_containers(config, config_profile)


if __name__ == "__main__":
    main()
