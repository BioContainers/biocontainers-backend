import json

import logging
import requests

logger = logging.getLogger('biocontainers.quayio.models')


class QuayIOContainer(object):
    """ This class contains the information of one small container"""

    def __init__(self, attributes):
        self.attributes = attributes

    def name(self):
        return self.attributes['name']

    def description(self):
        return self.attributes['description']

    def is_public(self):
        return self.attributes['is_public']

    def namespace(self):
        return self.attributes['namespace']

    def last_modified(self):
        return self.attributes['last_modified']

    def tags(self):
        return self.attributes['tags']

    def is_starred(self):
        return self.attributes['is_starred']


class QuayIOReader(object):
    """
    This class contains the services to retrieve the containers from Quay.io
    """
    containers_list = []

    def __new__(cls):
        return object.__new__(cls)

    def quayio_list_url(self, containers):
        self.quayIOContainers = containers

    def quayio_details_url(self, containers):
        self.quayio_details_url = containers

    def namespace(self, namespace):
        self.namespace = namespace

    def get_list_containers(self):
        """
        This method returns the list of small/short containers descriptions for
        all Quay.io containers.
        :return: list of container minimum metadata
        """
        string_url = self.quayIOContainers.replace('%namespace%', self.namespace)
        response = requests.get(string_url)
        self.container_list = []
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            for key in json_data['repositories']:
                container = QuayIOContainer(key)
                self.container_list.append(container)
                logger.info(" A short description has been retrieved from Quay.io for this container -- " + container.name())

        return self.container_list

    def get_containers(self, page=None, batch=None):
        """
        This method returns the of containers descriptions for
        all Quay.io containers.
        :return: Containers List
        """
        if not self.containers_list:
            self.containers_list = self.get_list_containers()

        if page == None:
            page = 0

        if batch == None:
            batch = len(self.container_list)

        string_url = self.quayio_details_url.replace('%namespace%', self.namespace)
        containers_list = []
        for index in range(page * batch, batch * (page + 1)):
            short_container = self.container_list[index]
            url = string_url.replace('%container_name%', short_container.name())
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    json_data = json.loads(response.content.decode('utf-8'))
                    container = QuayIOContainer(json_data)
                    containers_list.append(container)
                    logger.info(" A full description has been retrieved from Quay.io for this container -- " + container.name())
            except ConnectionError:
                logger.error(" Connection has failed to QuaIO for container ID --" + short_container.id)

        self.container_list = containers_list
        return self.container_list
