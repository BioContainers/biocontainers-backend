import datetime
import time
from itertools import groupby
import logging

from pymodm import connect
from pymongo.errors import DuplicateKeyError

from biocontainers.common.models import MongoToolVersion, ContainerImage

logger = logging.getLogger('biocontainers.quayio.models')

class InsertContainers:
    def __init__(self, connect_url):
        connection = connect(connect_url)

    def insert_quayio_containers(self, quayio_containers):
        containers_dic = {}
        for container in quayio_containers:

           for key,val in container.tags().items():
               version = key.split("--", 1)[0]
               tool_version_id = container.name() +'--' + version
               if tool_version_id not in containers_dic:
                   mongo_tool = MongoToolVersion()
                   mongo_tool.name = container.name()
                   mongo_tool.version = version
                   mongo_tool.description = container.description()
                   mongo_tool.tool_classes = ['TOOL']
               else:
                   mongo_tool = containers_dic[tool_version_id]

               container_image = ContainerImage()
               container_image.tag = key
               container_image.full_tag = "quay.io/biocontainers/" + container.name() + ":" + key
               container_image.container_type = 'DOCKER'
               datetime_object = time.strptime(val['last_modified'][0:-15], '%a, %d %b %Y')
               container_image.last_updated(datetime_object)
               container_image.size = int(int(val['size'])/1000000)
               mongo_tool.add_image_container(container_image)
               containers_dic[tool_version_id] = mongo_tool
               try:
                   mongo_tool.save()
               except (DuplicateKeyError) as error:
                   logger.error(" A tool with a same name and version is in the database -- " + tool_version_id)

        containers_list = list(containers_dic.values())


