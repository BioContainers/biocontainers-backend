import json

import logging
from urllib3.exceptions import NewConnectionError
from biocontainers.common.utils import call_api

logger = logging.getLogger('biocontainers.quayio.models')


class QuayIOContainer:
    """ This class contains the information of one small Quay container"""

    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def registry():
        return 'quay'

    def name(self):
        return self.attributes['name']

    def alias(self):
        return self.attributes['name']

    def description(self):
        return self.attributes['description']

    def organization(self):
        return self.attributes['namespace']

    def checker(self):
        return True

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


class QuayIOReader:
    """
    This class contains the services to retrieve the containers from Quay.io
    """

    def __init__(self, containers_list_url, container_details_url, namespace):
        self.containers_list_url = containers_list_url
        self.container_details_url = container_details_url
        self.namespace = namespace
        self.containers_list = None


    def get_containers_list(self):
        """
        This method returns the list of small/short containers descriptions for
        all Quay.io containers.
        :return: list of container minimum metadata
        """
        container_list = []
        string_url = self.containers_list_url.replace('%namespace%', self.namespace)
        try:
            response = call_api(string_url)
            if response.status_code == 200:
                json_data = json.loads(response.content.decode('utf-8'))
                for key in json_data['repositories']:
                    container = QuayIOContainer(key)
                    container_list.append(container)
                    logger.info(
                        " A short description has been retrieved from Quay.io for this container -- " + container.name())
        except (ConnectionError, NewConnectionError) as error:
            logger.error(" Connection has failed to QuaIO for following url --" + string_url)

        return container_list

    def get_containers(self, page=0, batch=None):
        """
        This method returns the of containers descriptions for
        all Quay.io containers.
        :return: Containers List
        """
        if self.containers_list is None:
            containers_list = self.get_containers_list()
        else:
            return self.containers_list

        if batch is None:
            batch = len(containers_list)

        string_url = self.container_details_url.replace('%namespace%', self.namespace)
        container_details_list = []

        for index in range(page * batch, batch * (page + 1)):
            short_container = containers_list[index]
            url = string_url.replace('%container_name%', short_container.name())
            try:
                response = call_api(url)
                if response.status_code == 200:
                    json_data = json.loads(response.content.decode('utf-8'))
                    container = QuayIOContainer(json_data)
                    container_details_list.append(container)
                    logger.info(
                        " A full description has been retrieved from Quay.io for this container -- " + container.name())
            except (ConnectionError, NewConnectionError) as error:
                logger.error(" Connection has failed to QuaIO for container ID --" + short_container.name())

        self.containers_list = container_details_list
        return self.containers_list
