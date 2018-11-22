# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "biocontainers_flask_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="GA4GH Tool Discovery API",
    author_email="",
    url="",
    keywords=["Swagger", "GA4GH Tool Discovery API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['biocontainers_flask_server=biocontainers_flask_server.__main__:main']},
    long_description="""\
    Proposed API for GA4GH (Global Alliance for Genomics &amp; Health) tool repositories. A tool consists of a set of container images that are paired with a set of documents. Examples of documents include CWL (Common Workflow Language) or WDL (Workflow Description Language) or NFL (Nextflow) that describe how to use those images and a set of specifications for those images (examples are Dockerfiles or Singularity recipes) that describe how to reproduce those images in the future. We use the following terminology, a \&quot;container image\&quot; describes a container as stored at rest on a filesystem, a \&quot;tool\&quot; describes one of the triples as described above. In practice, examples of \&quot;tools\&quot; include CWL CommandLineTools, CWL Workflows, WDL workflows, and Nextflow workflows that reference containers in formats such as Docker or Singularity. 
    """
)

