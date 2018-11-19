import argparse
import configparser
import logging

from biocontainers.biomongo.helpers import InsertContainers
from biocontainers.dockerhub.models import DockerHubReader
from biocontainers.github.models import GitHubCondaReader, GitHubConfiguration
from biocontainers.quayio.models import QuayIOReader

logger = logging.getLogger('biocontainers.pipelines')


def get_config():
    """
    This method read the default configuration file configuration.ini in the same path of the pipeline execution
    :return:
    """
    config = configparser.ConfigParser()
    config.read("configuration.ini")
    return config


def get_parameters():
    """
    This method provide a possibility to read arguments for the pipeline and combine then with the default
    configuration
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--import_quayio", help="Import Quay.io Recipes", action='store_true')
    parser.add_argument("-d", "--import_docker", help="Import Docker Recipes", action='store_true')

    return parser


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
    quayio_containers = reader.get_containers()
    mongo_helper = InsertContainers(config['TEST']['CONNECTION_URL'])
    mongo_helper.insert_quayio_containers(quayio_containers)

    # github_conf = GitHubConfiguration(config['DEFAULT']['GITHUB_API_CONDA'],
    #                                   config['DEFAULT']['GITHUB_CONDA_RECIPES_READABLE'])
    # github_reader = GitHubCondaReader(github_conf)
    # conda_recipes = github_reader.read_conda_recipes()
    # print(recipe.description())


def import_dockerhub(config):
    """
    Import dockerhub containers into the registry database
    :param config:
    :return:
    """

    logger.info("Starting importing DockerHub packages")
    reader = DockerHubReader()
    reader.dockerhub_list_url(config['DEFAULT']['DOCKER_HUB'])
    # reader.dockerhub_details_url(config['DEFAULT']['DOCKER_HUB_CONTAINER'])
    reader.dockerhub_tags_url(config['DEFAULT']['DOCKER_HUB_TAG'])
    reader.namespace(config['DEFAULT']['NAMESPACE'])
    containers = reader.get_containers()


def main(args):
    config = get_config()
    if config['DEFAULT']['VERBOSE'] == "True":
        for key in config['DEFAULT']:
            print(key + "=" + config['DEFAULT'][key])
        print(args)
    if args.import_quayio is not False:
        import_quayio(config)

    if args.import_docker is not False:
        import_dockerhub(config)


if __name__ == "__main__":
    parameters = get_parameters().parse_args()
    main(parameters)
