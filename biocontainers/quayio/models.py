import json
import requests


class QuayIOShortContainer(object):
    """ This class contains the information of one small container"""

    def __init__(self, dict):
        self.dict = dict

    def name(self):
        return self.dict['name']

    def description(self):
        return self.dict['description']

    def is_public(self):
        return self.dict['is_public']

    def namespace(self):
        return self.dict['namespace']

    def last_modified(self):
        return self.dict['last_modified']


class QuayIOReader(object):
    """
    This class contains the services to retrieve the containers from Quay.io
    """

    def __int__(self):
        pass

    def quayio_list_url(self, containers):
        self.quayIOContainers = containers

    def quayio_details_url(self, containers):
        self.quayIODetails = containers

    def namespace(self, namespace):
        self.namespace = namespace

    def get_list_containers(self):
        string_url = self.quayIOContainers.replace('%namespace%', self.namespace)
        response = requests.get(string_url)
        container_list = []
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            for key in json_data['repositories']:
                container = QuayIOShortContainer(key)
                container_list.append(container)
                print(container.name())

        return container_list
