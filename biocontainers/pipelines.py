import configparser
import logging

import click

from biocontainers.biomongo.helpers import InsertContainers
from biocontainers.dockerhub.models import DockerHubReader
from biocontainers.github.models import GitHubConfiguration, GitHubDockerReader, GitHubMulledReader, \
    LocalGitReader
from biocontainers.quayio.models import QuayIOReader
from biocontainers.singularity.models import SingularityReader
from ruamel.yaml import YAML

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

def import_singularity_containers(config, config_profile):
    """
    Import singularity containers into the registry database
    :param config_profile:
    :param config:
    :return:
    """

    logger.info("Starting importing singularity packages")
    reader = SingularityReader(config[config_profile]['SINGULARITY_CONTAINERS'])
    containers = reader.get_containers()

    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.insert_singularity_containers(containers)

def annotate_quayio_recipes(config, config_profile):
    github_url = config[config_profile]['GITHUB_GIT_URL']
    github_local = config[config_profile]['GITHUB_LOCAL_REPO']

    github_reader = LocalGitReader(github_url, github_local)
    github_reader.clone_url()
    conda_recipes = github_reader.read_conda_recipes()
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.annotate_quayio_containers(conda_recipes)


def annotate_docker_recipes(config, config_profile):
    github_conf = GitHubConfiguration(config[config_profile]['GITHUB_API_DOCKER'],
                                      config[config_profile]['GITHUG_DOCKER_RECIPES_READABLE'])
    github_reader = GitHubDockerReader(github_conf)
    docker_recipes = github_reader.read_docker_recipes()
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.annotate_docker_containers(docker_recipes)


def annotate_conda_recipes(config, config_profile):
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.annotate_conda_recipes()


def annotate_workflows_func(config, config_profile):
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.annotate_workflows(config, config_profile)


def annotate_multi_package_containers_func(config, config_profile):
    github_conf = GitHubConfiguration(config[config_profile]['GITHUB_API_MULLED_FILES'],
                                      config[config_profile]['GITHUB_MULLED_FILE_CONTENTS'])

    reader = GitHubMulledReader(github_conf)
    mulled_entries = reader.get_mulled_entries()
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.update_multi_package_containers(mulled_entries)


def annotate_biotools_recipes(config, config_profile):
    github_url = config[config_profile]['GITHUB_TOOLS_URL']
    github_local = config[config_profile]['GITHUB_TOOLS_LOCAL_REPO']
    github_reader = LocalGitReader(github_url, github_local)
    github_reader.clone_url()
    tools_recipes = github_reader.read_biotools_recipes()
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.annotate_biotools_metadata(tools_recipes)

    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.compute_similarity()

def annotate_biotools_recipes_github(config, config_profile):
    github_url = config[config_profile]['GITHUB_BIOTOOLS_REPO']
    github_local = config[config_profile]['GITHUB_BIOTOOLS_LOCAL_REPO']
    github_reader = LocalGitReader(github_url, github_local)
    github_reader.clone_url()
    tools_recipes = github_reader.read_biotools_github_recipes()
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.annotate_biotools_metadata(tools_recipes)

    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    mongo_helper.compute_similarity()

def report_missing_tools(config, config_profile):
    mongo_helper = InsertContainers(config[config_profile]['DATABASE_URI'])
    missing_info = mongo_helper.get_missing_info_tools()
    tools = {}
    missing_info.sort(key=lambda x: x.total_pulls, reverse=True)
    for tool in missing_info:
        missing_tool = {}
        missing_tool['name'] = tool.name
        missing_tool['description'] = tool.description
        missing_tool['license'] = tool.license
        missing_tool['home_url'] = tool.home_url
        missing_tool['total_pulls'] = tool.total_pulls
        tools[tool.name] = missing_tool
    yaml = YAML()
    yaml.indent(mapping=4, sequence=6, offset=3)
    with open('../missing_annotations.yaml', 'w') as outfile:
        yaml.dump(tools, outfile)

def get_database_uri(param):
    uri = 'mongodb://' + param['MONGODB_USER'] + ":" + param['MONGODB_PASS'] + '@' + param['MONGODB_HOST'] + ':' + \
          param['MONGO_PORT'] + '/' + param['BIOCONT_DB_NAME'] + '?ssl=false&authSource=' + param['MONGODB_ADMIN_DB']
    return uri


@click.command()
@click.option('--import-quayio', '-q', help='Import Quay.io Recipes', is_flag=True)
@click.option('--import-docker', '-k', help="Import Docker Recipes", is_flag=True)
@click.option('--import-singularity', '-s', help="Import Singularity Recipes", is_flag=True)
@click.option('--annotate-docker', '-ad', help='Annotate Docker Recipes', is_flag=True)
@click.option('--annotate-quayio', '-aq', help='Annotate Quay.io Recipes', is_flag=True)
@click.option('--annotate-conda', '-ac', help='Annotate Conda packages', is_flag=True)
@click.option('--annotate-biotools', '-ab', help='Annotate BioTools metadata from Github', is_flag = True)
@click.option('--annotate-workflows', '-aw', help='Annotate Workflows', is_flag=True)
@click.option('--annotate-identifiers', '-ai', help='Annotate external identifiers (e.g biotools)', is_flag=True)
@click.option('--annotate-multi-package-containers', '-am', help='Annotate multi package containers', is_flag=True)
@click.option('--report-missing-info', '-ri', help = "This pipeline will report the containers without metadata", is_flag =True)
@click.option('--config-file', '-c', type=click.Path(), default='configuration.ini')
@click.option('--config-profile', '-a', help="This option allow to select a config profile", default='PRODUCTION')
@click.option('-db', '--db-name', help="Name of the database", envvar='BIOCONT_DB_NAME')
@click.option('-h', '--db-host', help='Host the database', envvar='MONGODB_HOST')
@click.option('-a', '--db-auth-database', help='Authentication database in Mongo', envvar='MONGODB_ADMIN_DB')
@click.option('-u', '--db-user', help='Database root user', envvar='MONGODB_USER', default='admin')
@click.option('-pw', '--db-password', help='Database password', envvar='MONGODB_PASS')
@click.option('-p', '--db-port', help='Database port', envvar='MONGO_PORT', default='27017')
@click.pass_context
def main(ctx, import_quayio, import_docker, import_singularity, annotate_docker, annotate_quayio,
         annotate_conda, annotate_biotools, annotate_workflows, annotate_identifiers, annotate_multi_package_containers, report_missing_info,
         config_file, config_profile, db_name,
         db_host, db_auth_database, db_user,
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

    if import_singularity is not False:
        import_singularity_containers(config, config_profile)

    if annotate_docker is not False:
        annotate_docker_recipes(config, config_profile)

    if annotate_quayio is not False:
        annotate_quayio_recipes(config, config_profile)

    if annotate_conda is not False:
        annotate_conda_recipes(config, config_profile)

    if annotate_workflows is not False:
        annotate_workflows_func(config, config_profile)

    if annotate_identifiers is not False:
        annotate_biotools_recipes(config, config_profile)

    if annotate_multi_package_containers is not False:
        annotate_multi_package_containers_func(config, config_profile)

    if annotate_biotools is not False:
        annotate_biotools_recipes_github(config, config_profile)

    if report_missing_info is not False:
        report_missing_tools(config, config_profile)


if __name__ == "__main__":
    main()
