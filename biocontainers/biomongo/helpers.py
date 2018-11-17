import time
import logging

from pymodm import connect
from pymongo.errors import DuplicateKeyError

from biocontainers.common.models import MongoToolVersion, ContainerImage, MongoTool

logger = logging.getLogger('biocontainers.quayio.models')
QUAYIO_DOMAIN = "quay.io/biocontainers/"


class InsertContainers:
    def __init__(self, connect_url):
        connection = connect(connect_url)

    def insert_quayio_containers(self, quayio_containers):
        """
        This method provide the mechanism to insert quayio containers into the Mongo Database
        :param quayio_containers: List of Quay.io containers
        :return:
        """
        tool_versions_dic = MongoToolVersion.objects.all()
        tools_dic = MongoTool.objects.all()

        for container in quayio_containers:
            for key, val in container.tags().items():

                # Insert Tool version containers
                version = key.split("--", 1)[0]
                tool_version_id = container.name() + '--' + version
                if tool_version_id not in tool_versions_dic:
                    mongo_tool_version = MongoToolVersion()
                    mongo_tool_version.name = container.name()
                    mongo_tool_version.version = version
                    mongo_tool_version.description = container.description()
                    mongo_tool_version.tool_classes = ['TOOL']
                else:
                    mongo_tool_version = tool_versions_dic[tool_version_id]

                container_image = ContainerImage()
                container_image.tag = key
                container_image.full_tag = QUAYIO_DOMAIN + container.name() + ":" + key
                container_image.container_type = 'DOCKER'
                datetime_object = time.strptime(val['last_modified'][0:-15], '%a, %d %b %Y')
                container_image.last_updated(datetime_object)
                container_image.size = int(int(val['size']) / 1000000)
                mongo_tool_version.add_image_container(container_image)
                tool_versions_dic[tool_version_id] = mongo_tool_version

                # Insert the corresponding tool
                tool_id = container.name()
                if tool_id not in tools_dic:
                    mongo_tool = MongoTool()
                    mongo_tool.name = container.name()
                else:
                    mongo_tool = tools_dic[tool_id]
                try:
                    mongo_tool_version.save()
                except DuplicateKeyError as error:
                    logger.error(" A tool with a same name and version is in the database -- " + tool_version_id)





        containers_list = list(tool_versions_dic.values())