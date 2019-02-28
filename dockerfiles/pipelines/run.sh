#!/bin/bash

python /biocontainers-backend/biocontainers/pipelines.py \
    --config-file /biocontainers-backend/biocontainers/configuration.ini \
    --db-password $MONGODB_PASS --db-host $MONGODB_HOST --db-auth-database $MONGODB_ADMIN_DB \
    --db-name $BIOCONT_DB_NAME --db-user $MONGODB_USER -k -q -ad -aq
