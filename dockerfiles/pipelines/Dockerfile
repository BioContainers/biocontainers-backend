
################## BASE IMAGE ######################

FROM python:3.4.9-alpine3.7

################## METADATA ######################

LABEL base_image="python:3.4.9-alpine3.7"
LABEL version="1"
LABEL software="biocontainers-pipelines-py"
LABEL software.version="1.0.0"
LABEL about.summary="The pipelines retrieve all the biocontainers sources dockerhub, quay.io and other resources"
LABEL about.home="https://biocontainers.pro"
LABEL about.license="SPDX:Apache-2"

################## MAINTAINER ######################

MAINTAINER Yasset Perez-Riverol <ypriverol@gmail.com>

################## INSTALLATION ######################

RUN apk update && apk wget git
RUN python -m pip install requests
RUN python --version
RUN pip --version
RUN git clone --single-branch -b master https://github.com/BioContainers/biocontainers-backend.git
RUN cd /biocontainers-backend && pip install -r biocontainers/requirements.txt && pip install -r biocontainers_flask/requirements.txt

FROM openjdk:8-jre-stretch

RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update && apt-get install -y --allow-unauthenticated mongodb-org-shell


ADD run.sh /usr/local/bin/run.sh
RUN chmod u+x /usr/local/bin/run.sh
ENTRYPOINT ["run.sh"]

