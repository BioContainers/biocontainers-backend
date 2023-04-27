
################## BASE IMAGE ######################

FROM python:3.7

################## METADATA ######################

LABEL base_image="python:3.4.9-alpine3.7"
LABEL version="1"
LABEL software="biocontainers-api-py"
LABEL software.version="1.0.0"
LABEL about.summary="The BioContainers Restful API allow to retrieve all the biocontainers sources dockerhub, quay.io and other resources"
LABEL about.home="https://api.biocontainers.pro"
LABEL about.license="SPDX:Apache-2"

################## MAINTAINER ######################

MAINTAINER Yasset Perez-Riverol <ypriverol@gmail.com>

################## INSTALLATION ######################

RUN apt-get update && apt-get install -y wget git
RUN python -m pip install requests
RUN python --version
RUN pip --version
#force git clone.. not to use cache
ARG CACHEBUST=1
RUN git clone --depth=1 --single-branch -b master https://github.com/BioContainers/biocontainers-backend.git
RUN cd /biocontainers-backend && pip install -r biocontainers/requirements.txt && pip install -r biocontainers_flask/requirements.txt
ENV PYTHONPATH /biocontainers-backend

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
#RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb.list
#RUN apt-get update && apt-get install -y --allow-unauthenticated mongodb-org-shell
RUN echo "deb [trusted=yes] http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb.list
RUN apt-get --allow-insecure-repositories update && apt-get --allow-unauthenticated  install -y mongodb-org-shell


ADD run.sh /biocontainers-backend/run.sh
RUN chmod u+x /biocontainers-backend/run.sh
ENV PATH    $PATH:/biocontainers-backend/
ENTRYPOINT ["run.sh"]
