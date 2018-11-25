
################## BASE IMAGE ######################

FROM python:2.7.15-alpine3.6

################## METADATA ######################

LABEL base_image="python:2.7.15-alpine3.6"
LABEL version="1"
LABEL software="biocontainers-pipelines-py"
LABEL software.version="1.0.0"
LABEL about.summary="The pipelines retrieve all the biocontainers sources dockerhub, quay.io and other resources"
LABEL about.home="https://biocontainers.pro"
LABEL about.license="SPDX:Apache-2"

################## MAINTAINER ######################

MAINTAINER Yasset Perez-Riverol <ypriverol@gmail.com>

################## INSTALLATION ######################

RUN apk update && apk add wget git python
RUN git clone --single-branch -b master https://github.com/BioContainers/biocontainers-backend.git
RUN cd /biocontainers-backend && python pip -r requirements.txt

FROM openjdk:8-jre-stretch

RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update && apt-get install -y --allow-unauthenticated mongodb-org-shell

COPY --from=0 /registry-backend/registry-pipelines/target/registry-pipelines-1.0-SNAPSHOT.jar /registry-pipelines.jar


