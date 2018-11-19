import operator
import time
import logging
from collections import defaultdict

from pymodm import connect
from pymongo.errors import DuplicateKeyError

import itertools
from operator import itemgetter

from biocontainers.common.models import MongoToolVersion, ContainerImage, MongoTool

logger = logging.getLogger('biocontainers.quayio.models')
QUAYIO_DOMAIN = "quay.io/biocontainers/"
TOOL_VERSION_SPLITTER = '-'


class InsertContainers:
    def __init__(self, connect_url):
         connection = connect(connect_url)

    def insert_quayio_containers(self, quayio_containers):
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
                    mongo_tool_version.tool_classes = ['TOOL']
                    mongo_tool_version.id = tool_version_id
                else:
                    mongo_tool_version = tool_versions_dic[tool_version_id]

                ## Get the tag information (Container image) and add to the ToolVersion
                container_image = ContainerImage()
                container_image.tag = key
                container_image.full_tag = QUAYIO_DOMAIN + container.name() + ":" + key

                container_image.container_type = 'DOCKER'
                datetime_object = time.strptime(val['last_modified'][0:-15], '%a, %d %b %Y')
                container_image.last_updated(datetime_object)
                container_image.size = int(int(val['size']) / 1000000)
                mongo_tool_version.add_image_container(container_image)
                if tool_version_id in tool_versions_dic:
                    tool_versions_dic[tool_version_id] = mongo_tool_version
                else:
                    tool_versions_dic[tool_version_id] = mongo_tool_version

                # Insert the corresponding tool
                tool_id = container.name()
                if tool_id not in tools_dic:
                    mongo_tool = MongoTool()
                    mongo_tool.name = container.name()
                    mongo_tool.id = container.name()
                    mongo_tool.description = container.description()
                    tools_dic[tool_id].append(mongo_tool)
                else:
                    mongo_tool = tools_dic[tool_id]

                try:
                    mongo_tool.save()
                except DuplicateKeyError as error:
                    logger.error(" A tool with same name is already in the database -- " + tool_id)

                mongo_tool_version.ref_tool = mongo_tool
                #mongo_versions = mongo_tool.get_tool_versions()

                try:
                    mongo_tool_version.save()
                except DuplicateKeyError as error:
                    logger.error(" A tool version with a same name and version is in the database -- " + tool_version_id)





        containers_list = list(tool_versions_dic.values())
