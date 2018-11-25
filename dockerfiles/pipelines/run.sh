#!/bin/bash

java -jar /registry-pipelines.jar --mongodb.biocontainers.db.database=$BIOCONT_DB_NAME \
  --mongodb.biocontainers.db.user=$MONGODB_USER \
  --mongodb.biocontainers.db.password=$MONGODB_PASS \
  --mongodb.biocontainers.db.authenticationDatabase=$MONGODB_ADMIN_DB \
  --mongodb.biocontainers.db.host=$MONGODB_HOST \
  --mongodb.biocontainers.db.port=27017
