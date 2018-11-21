import argparse
import configparser
import logging

import click

from biocontainers.biomongo.helpers import InsertContainers
from biocontainers.dockerhub.models import DockerHubReader
from biocontainers.github.models import GitHubCondaReader, GitHubConfiguration
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


def import_quayio(config):
    """
    Import quayio containers into the registry database
    :param config: Parameters for quayio
    :return:
    """
    logger.info("Starting importing Conda packages")

    reader = QuayIOReader()
    reader.quayio_list_url(config['DEFAULT']['QUAYIO_CONTAINER_LIST'])
    reader.quayio_details_url(config['DEFAULT']['QUAYIO_CONTAINER_DETAILS'])
    reader.namespace(config['DEFAULT']['NAMESPACE'])
    quayio_containers = reader.get_containers(batch=2000)

    mongo_helper = InsertContainers(config['TEST']['CONNECTION_URL'])
    mongo_helper.insert_quayio_containers(quayio_containers)

    # github_conf = GitHubConfiguration(config['DEFAULT']['GITHUB_API_CONDA'],
    #                                   config['DEFAULT']['GITHUB_CONDA_RECIPES_READABLE'])
    # github_reader = GitHubCondaReader(github_conf)
    # # conda_recipes = github_reader.read_conda_recipes()
    # # print(recipe.description())


def import_dockerhub(config):
    """
    Import dockerhub containers into the registry database
    :param config:
    :return:
    """

    logger.info("Starting importing DockerHub packages")
    reader = DockerHubReader()
    reader.dockerhub_list_url(config['DEFAULT']['DOCKER_HUB'])
    reader.dockerhub_tags_url(config['DEFAULT']['DOCKER_HUB_TAG'])
    reader.namespace(config['DEFAULT']['NAMESPACE'])
    dockerhub_containers = reader.get_containers(batch=200)

    mongo_helper = InsertContainers(config['TEST']['CONNECTION_URL'])
    mongo_helper.insert_dockerhub_containers(dockerhub_containers)


@click.command()
@click.option('--import-quayio', '-q', help='Import Quay.io Recipes', is_flag=True)
@click.option('--import-docker','-d', help="Import Docker Recipes", is_flag=True)
@click.option('--config-file', '-c',type=click.Path(),default='configuration.ini')
def main(import_quayio, import_docker, config_file):
    config = get_config(config_file)
    if config['DEFAULT']['VERBOSE'] == "True":
        for key in config['DEFAULT']:
            print(key + "=" + config['DEFAULT'][key])

    if import_quayio is not False:
        import_quayio(config)

    if import_docker is not False:
        import_dockerhub(config)


if __name__ == "__main__":
    main()
