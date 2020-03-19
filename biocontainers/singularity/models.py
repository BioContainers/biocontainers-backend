import logging
from urllib.parse import unquote
from datetime import datetime

from biocontainers.common.models import MongoToolVersion, ContainerImage
from biocontainers.common.utils import call_api
from bs4 import BeautifulSoup

logger = logging.getLogger('biocontainers.singularity.models')


class SingularityReader:
    """
    This class contains the services to retrieve the containers from Quay.io
    """

    def __init__(self, containers_list_url):
        self.containers_list_url = containers_list_url
        self.containers_list = None

    def get_containers(self):
        """
        This method returns the list of small/short containers descriptions for
        all Singularity containers.
        :return: list of container minimum metadata
        """
        container_list = {}
        response = call_api(self.containers_list_url)
        if response.status_code == 200:
            html = response.text
            for line in html.splitlines():
                if line.startswith("<a href="):
                    entry = BeautifulSoup(line, 'html.parser').find('a')
                    image_name = unquote(entry['href'])
                    if image_name.endswith("/"):
                        continue
                    sibling = entry.next_sibling
                    line_splits = sibling.split()
                    last_updated = line_splits[0] + " " + line_splits[1]
                    size = line_splits[2]
                    # print(image_name + "\t" + last_updated + "\t" +size)
                    image_name_split = image_name.split(':')
                    tool_version = image_name_split[0]+"-"+image_name_split[1].split('--')[0]
                    container = ContainerImage()
                    container.container_type = "SINGULARITY"
                    container.tag = image_name_split[1]
                    container.full_tag = self.containers_list_url + "/" + image_name
                    container.size = size
                    container.last_updated = datetime.strptime(last_updated, '%d-%b-%Y %H:%M')
                    if tool_version not in container_list:
                        container_list[tool_version] = []

                    container_list[tool_version].append(container)

        return container_list
