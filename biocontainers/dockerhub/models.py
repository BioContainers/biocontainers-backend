import json

import logging

from biocontainers.common.utils import call_api

logger = logging.getLogger('biocontainers.dockerhub.models')


class DockerHubContainer(object):
    """
    This class contains the information of one small docker container
    """
    tags = []

    def __init__(self, attributes):
        self.attributes = attributes

    def name(self):
        return self.attributes['name']

    def description(self):
        return self.attributes['description']

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


class DockerHubReader(object):
    """
    This class contains the services to retrieve the containers from Quay.io
    """
    containers_list = []

    def __new__(cls):
        return object.__new__(cls)

    def dockerhub_list_url(self, url):
        self.dockerhub_list_url = url

    def dockerhub_tags_url(self, url):
        self.dockerhub_tags_url = url

    def namespace(self, namespace):
        self.namespace = namespace

    def get_list_containers(self):
        """
        This method returns the list of small/short containers descriptions for
        all DockerHub containers.
        :return: list of container minimum metadata
        """
        string_url = self.dockerhub_list_url.replace('%namespace%', self.namespace)
        self.container_list = []
        while string_url is not None:
            response = call_api(string_url)
            if response.status_code == 200:
                json_data = json.loads(response.content.decode('utf-8'))
                for key in json_data['results']:
                    container = DockerHubContainer(key)
                    self.container_list.append(container)
                    print(container.name())
                string_url = json_data['next']

        return self.container_list

    def get_containers(self, page=None, batch=None):
        """
        This method returns the of containers descriptions for
        all DockerHub containers.
        :return: Containers List
        """
        if not self.containers_list:
            self.containers_list = self.get_list_containers()

        if page == None:
            page = 0

        if batch == None:
            batch = len(self.container_list)

        string_url = self.dockerhub_tags_url.replace('%namespace%', self.namespace)
        containers_list = []

        for index in range(page * batch, batch * (page + 1)):
            short_container = self.container_list[index]
            url = string_url.replace('%container_name%', short_container.name())
            try:
                response = call_api(url)
                if response.status_code == 200:
                    json_data = json.loads(response.content.decode('utf-8'))
                    short_container.add_all_tags(json_data['results'])
                    container = short_container
                    containers_list.append(container)
                    print(container.name())
            except ConnectionError:
                logger.error("Connection has failed to DockerHub for container ID --" + container.id)

        self.container_list = containers_list
        return self.container_list
