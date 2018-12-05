[![Python 3.4](https://img.shields.io/badge/python-3.4-green.svg)](https://www.python.org/downloads/release/python-340/)  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

BioContainers backed
=====================================================

The BioContainers backed for the [Biocontainers Registry](http://biocontainers.pro/registry). The library defines two main components:

- BioContianers pipelines
- BioContainers Restful API


BioContainers Pipelines
----------------------------

The BioContainers pipelines contains the tools and workflows to insert quay.io and and dockerhub containers. In addition,
it gets the information from containers recipes Dockefile or Conda recipes to annotate the containers.

## Pre-requisites


- MongoDB
- Python > 3.4

### Setting the environment

Before lunching the pipelines you should add to the ```PYTHONPATH``` the biocontainers-backend folder:

```bash
$ cd biocontainers-backend
$ export PYTHONPATH=$PYTHONPATH:./
```



The pipelines can be run using the following command:

```bash
python3.4 biocontainers/pipelines.py --config-file biocontainers/configuration.ini
```

This will pront the following options:

```
  -q, --import-quayio             Import Quay.io Recipes
  -k, --import-docker             Import Docker Recipes
  -c, --config-file PATH
  -a, --config-profile TEXT       This option allow to select a config profile
  -db, --db-name TEXT             Name of the database
  -h, --db-host TEXT              Host the database
  -auth, --db-auth-database TEXT  Authentication database in Mongo
  -u, --db-user TEXT              Database root user
  -pw, --db-password TEXT         Database password
  -p, --db-port TEXT              Database port
  --help                          Show this message and exit.
```


BioContainers Flask API
--------------------------


