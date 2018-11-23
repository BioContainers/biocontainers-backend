#!/usr/bin/env python3

import connexion
from pymodm import connect

from biocontainers_flask.server import encoder

_MONGO_URI='mongodb://localhost:27017/testdb'
connect(_MONGO_URI)

_PUBLIC_REGISTRY_URL = "http://biocontainers.pro/registry/"

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'GA4GH Tool Discovery API'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
