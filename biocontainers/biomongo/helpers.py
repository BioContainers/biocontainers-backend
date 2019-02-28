import datetime
import logging
import os

from pymodm import connect
from pymongo.errors import DuplicateKeyError

from biocontainers.common.models import MongoToolVersion, ContainerImage, MongoTool, _CONSTANT_TOOL_CLASSES

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

                ## Get the tag information (Container image) and add to the ToolVersion
                container_image = ContainerImage()
                container_image.tag = key
                container_image.full_tag = QUAYIO_DOMAIN + container.name() + ":" + key

                container_image.container_type = 'DOCKER'
                datetime_object = datetime.datetime.strptime(val['last_modified'][0:-15], '%a, %d %b %Y')
                container_image.last_updated = datetime_object
                container_image.size = int(int(val['size']) / 1000000)
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
                except DuplicateKeyError as error:
                    logger.error(" A tool with same name is already in the database -- " + tool_id)

                mongo_tool_version.ref_tool = mongo_tool
                # mongo_versions = mongo_tool.get_tool_versions()

                try:
                    mongo_tool_version.save()
                except DuplicateKeyError as error:
                    logger.error(
                        " A tool version with a same name and version is in the database -- " + tool_version_id)

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
                datetime_object = datetime.datetime.strptime(key['last_updated'][0:-17], '%Y-%m-%d')
                container_image.last_updated = datetime_object
                container_image.size = int(int(key['full_size']) / 1000000)
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
                except DuplicateKeyError as error:
                    logger.error(" A tool with same name is already in the database -- " + tool_id)

                mongo_tool_version.ref_tool = mongo_tool
                # mongo_versions = mongo_tool.get_tool_versions()

                try:
                    mongo_tool_version.save()
                except DuplicateKeyError as error:
                    logger.error(
                        " A tool version with a same name and version is in the database -- " + tool_version_id)

        containers_list = list(tool_versions_dic.values())

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
                    tool_version.description = entry["recipe"].get_description()
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
                    tool.description = entry["recipe"].get_description()
                if entry['recipe'].get_home_url() is not None:
                    tool.home_url = entry['recipe'].get_home_url()
                if entry['recipe'].get_license() is not None:
                    tool.license = entry['recipe'].get_license()
                else:
                    tool.license = NOT_AVAILABLE
                if entry['recipe'].get_tags() is not None:
                    tool.tool_tags = entry['recipe'].get_tags()
                if entry['recipe'].get_additional_ids() is not None:
                    tool.additional_identifiers = entry['recipe'].get_additional_ids()
                tool.save()
                logger.info("Updated tool description of -- " + tool_version_id)

    @staticmethod
    def annotate_conda_containers(conda_recipes):
        for entry in conda_recipes:
            logger.info("Annotating the recipe -- " + entry['name'])
            tool_version_id = None
            if (entry['recipe'].get_name() is not None) and (entry['recipe'].get_version() is not None) \
                    and ("{" not in entry['recipe'].get_name()) \
                    and ("|" not in entry['recipe'].get_name()) and ("{" not in entry['recipe'].get_version()) \
                    and ("|" not in entry['recipe'].get_version()):
                tool_version_id = entry['recipe'].get_name() + "-" + entry['recipe'].get_version()
                tool_id = entry['recipe'].get_name()
                tool_version = MongoToolVersion.get_tool_version_by_id(tool_version_id)
                tool = MongoTool.get_tool_by_id(tool_id)
                if tool_version is not None:
                    if entry["recipe"].get_description() is not None:
                        tool_version.description = entry["recipe"].get_description()
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
                        tool.description = entry["recipe"].get_description()
                    if entry['recipe'].get_home_url() is not None:
                        tool.home_url = entry['recipe'].get_home_url()
                    if entry['recipe'].get_license() is not None:
                        tool.license = entry['recipe'].get_license()
                    else:
                        tool.license = NOT_AVAILABLE

                    tool.save()
                    logger.info("Updated tool description of -- " + tool_version_id)

            logger.info("The following tool has been analyzed -- " + str(tool_version_id))




