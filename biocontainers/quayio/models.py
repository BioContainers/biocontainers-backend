import json
import requests


class QuayIOReader(object):
    """
    This class containes the services to retrieve the containers from Quay.io
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
        stringURL = self.quayIOContainers.replace('%namespace%', self.namespace)
        response = requests.get(stringURL)

        containerList = None
        if response.status_code == 200:
            containerList = json.loads(response.content.decode('utf-8'))

        return containerList
