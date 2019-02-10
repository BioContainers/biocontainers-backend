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
                                                        "tool_contains": {"$each": tools_array},
                                                        "aliases": {"$each": aliases}
                                                    }
                                                })

            # collection "tool_version: id" field has "-" instead of ":"
            mulled_name = mulled_name.replace(":", "-")
            MongoToolVersion.manager_versions.exec_update_query({"id": mulled_name},
                                                                {"$set":
                                                                     {"tool_contains": tools_array,
                                                                      "aliases": aliases
                                                                      }
                                                                 })
