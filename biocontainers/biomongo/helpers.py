from itertools import groupby

from pymodm import connect

from biocontainers.common.models import MongoToolVersion


class InsertContainers:
    def __init__(self, connect_url):
        connection = connect(connect_url)

    def insert_quayio_containers(self, quayio_containers):
        containers_dic = {}
        for container in quayio_containers:
           for key,val in container.tags().items():
               version = key.split("--", 1)[0]
               print(version)
               print(val)

