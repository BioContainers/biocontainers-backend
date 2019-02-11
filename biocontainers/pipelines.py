import configparser
import logging

import click

from biocontainers.biomongo.helpers import InsertContainers
from biocontainers.dockerhub.models import DockerHubReader
from biocontainers.github.models import GitHubCondaReader, GitHubConfiguration, GitHubDockerReader, GitHubMulledReader
from biocontainers.quayio.models import QuayIOReader

logger = logging.getLogger('biocontainers.pipelines')


def print_help(ctx, param, value):
    if value is False:
        return
    click.echo(ctx.get_help())
    ctx.exit()


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
    :param config_profile:
    :param config: Parameters for quayio
    :return:
    """
    logger.info("Starting importing Conda packages")

    reader = QuayIOReader(config[config_profile]['QUAYIO_CONTAINER_LIST'],
                          config[config_profile]['QUAYIO_CONTAINER_DETAILS'], config[config_profile]['NAMESPACE'])
    quayio_containers = reader.get_containers()

    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.insert_quayio_containers(quayio_containers)


def import_dockerhub_containers(config, config_profile):
    """
    Import dockerhub containers into the registry database
    :param config_profile:
    :param config:
    :return:
    """

    logger.info("Starting importing DockerHub packages")
    reader = DockerHubReader(config[config_profile]['DOCKER_HUB'], config[config_profile]['DOCKER_HUB_TAG'],
                             config[config_profile]['NAMESPACE'])
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

def annotate_multi_package_containers(config, config_profile):
    github_conf = GitHubConfiguration(config[config_profile]['GITHUB_API_MULLED_FILES'],
                                      config[config_profile]['GITHUB_MULLED_FILE_CONTENTS'])

    reader = GitHubMulledReader(github_conf)
    mulled_entries = reader.get_mulled_entries()
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.update_multi_package_containers(mulled_entries)


def get_database_uri(param):
    uri = 'mongodb://' + param['MONGODB_USER'] + ":" + param['MONGODB_PASS'] + '@' + param['MONGODB_HOST'] + ':' + \
          param['MONGO_PORT'] + '/' + param['BIOCONT_DB_NAME'] + '?ssl=false&authSource=' + param['MONGODB_ADMIN_DB']
    return uri


@click.command()
@click.option('--import-quayio', '-q', help='Import Quay.io Recipes', is_flag=True)
@click.option('--import-docker', '-k', help="Import Docker Recipes", is_flag=True)
@click.option('--config-file', '-c', type=click.Path(), default='configuration.ini')
@click.option('--config-profile', '-a', help="This option allow to select a config profile", default='PRODUCTION')
@click.option('-db', '--db-name', help="Name of the database", envvar='BIOCONT_DB_NAME')
@click.option('-h', '--db-host', help='Host the database', envvar='MONGODB_HOST')
@click.option('-a', '--db-auth-database', help='Authentication database in Mongo', envvar='MONGODB_ADMIN_DB')
@click.option('-u', '--db-user', help='Database root user', envvar='MONGODB_USER', default='admin')
@click.option('-pw', '--db-password', help='Database password', envvar='MONGODB_PASS')
@click.option('-p', '--db-port', help='Database port', envvar='MONGO_PORT', default='27017')
@click.pass_context
def main(ctx, import_quayio, import_docker, config_file, config_profile, db_name, db_host, db_auth_database, db_user,
         db_password, db_port):
    config = get_config(config_file)
    if config[config_profile]['VERBOSE'] == "True":
        for key in config[config_profile]:
            print(key + "=" + config[config_profile][key])

    if (db_name is None) or (db_host is None) or (db_user is None):
        print_help(ctx, None, value=True)
    else:
        config[config_profile]['BIOCONT_DB_NAME'] = db_name
        config[config_profile]['MONGODB_HOST'] = db_host
        config[config_profile]['MONGO_PORT'] = db_port
        config[config_profile]['MONGODB_USER'] = db_user
        config[config_profile]['MONGODB_ADMIN_DB'] = db_auth_database
        config[config_profile]['MONGODB_PASS'] = db_password
        config[config_profile]['DATABASE_URI'] = get_database_uri(config[config_profile])

    if import_quayio is not False:
        import_quayio_containers(config, config_profile)

    if import_docker is not False:
        import_dockerhub_containers(config, config_profile)

    annotate_multi_package_containers(config, config_profile)

if __name__ == "__main__":
    main()
