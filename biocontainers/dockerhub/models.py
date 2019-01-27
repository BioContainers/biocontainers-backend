import json

import logging

from biocontainers.common.utils import call_api

logger = logging.getLogger('biocontainers.dockerhub.models')


class DockerHubContainer:
    """
    This class contains the information of one small docker container
    """
    tags = []

    def __init__(self, attributes):
        self.attributes = attributes

    @staticmethod
    def registry():
        return 'dockerhub'

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
        return self.attributes['is_private'] != 'false'

    def namespace(self):
        return self.attributes['namespace']

    def last_modified(self):
        return self.attributes['last_updated']

    def tags(self):
        return self.attributes['tags']

    def is_starred(self):
        return self.attributes['start_count'] > 0

    def add_all_tags(self, tags):
        self.tags = []
        for key in tags:
            self.tags.append(key)


class DockerHubReader:
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
        all DockerHub containers.
        :return: list of container minimum metadata
        """
        container_list = []
        string_url = self.containers_list_url.replace('%namespace%', self.namespace)
        while string_url is not None:
            response = call_api(string_url)
            if response.status_code == 200:
                json_data = json.loads(response.content.decode('utf-8'))
                for key in json_data['results']:
                    container = DockerHubContainer(key)
                    container_list.append(container)
                    logger.info(" Current tool has been retrieve from DockerHub -- " + container.name())
                string_url = json_data['next']

        return container_list

    def get_containers(self, page=0, batch=None):
        """
        This method returns the of containers descriptions for
        all DockerHub containers.
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
                    short_container.add_all_tags(json_data['results'])
                    container = short_container
                    container_details_list.append(container)
                    logger.info(" Current tool has been retrieve from DockerHub -- " + container.name())
            except ConnectionError:
                logger.error(" Connection has failed to DockerHub for container ID --" + short_container.name())

        self.containers_list = container_details_list
        return self.containers_list
