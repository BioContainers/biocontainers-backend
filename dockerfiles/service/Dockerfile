
################## BASE IMAGE ######################

FROM openjdk:8-jdk-alpine

################## METADATA ######################

LABEL base_image="biocontainers:debian-stretch-backports"
LABEL version="1"
LABEL software="biocontainers-api-py"
LABEL software.version="1.0.0"
LABEL about.summary="The biocontainers API provides an entry point to retrieve all containers"
LABEL about.home="https://biocontainers.pro"
LABEL about.license="SPDX:Apache-2"

################## MAINTAINER ######################

MAINTAINER Yasset Perez-Riverol <ypriverol@gmail.com>

################## INSTALLATION ######################

RUN apk update && apk add maven wget git
RUN git clone --single-branch -b master https://github.com/BioContainers/registry-backend.git
RUN cd /registry-backend && mvn install -DskipTests

FROM openjdk:8-jre-stretch

RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update && apt-get install -y --allow-unauthenticated mongodb-org-shell

COPY --from=0 /registry-backend/biocontainers-api/target/biocontainers-api-1.0-SNAPSHOT.jar /api-service.jar

ADD run.sh /usr/local/bin/run.sh
RUN chmod u+x /usr/local/bin/run.sh
ENTRYPOINT ["run.sh"]
