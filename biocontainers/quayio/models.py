import json
import requests


class QuayIOContainer(object):
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

    def tags(self):
        return self.dict['tags']

    def is_starred(self):
        return self.dict['is_starred']

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
        """
        This method returns the list of small/short containers descriptions for
        all Quay.io containers.
        :return:
        """
        string_url = self.quayIOContainers.replace('%namespace%', self.namespace)
        response = requests.get(string_url)
        self.container_list = []
        if response.status_code == 200:
            json_data = json.loads(response.content.decode('utf-8'))
            for key in json_data['repositories']:
                container = QuayIOContainer(key)
                self.container_list.append(container)
                print(container.name())

        return self.container_list

    def get_containers(self):
        """
        This method returns the of containers descriptions for
        all Quay.io containers.
        :return:
        """
        string_url = self.quayIODetails.replace('%namespace%', self.namespace)
        for short_container in self.container_list:
            url = string_url.replace('%container_name%', short_container.name())
            response = requests.get(url)
            if response.status_code == 200:
                json_data = json.loads(response.content.decode('utf-8'))
                container = QuayIOContainer(json_data)
                print(container.name())

        return self.container_list

