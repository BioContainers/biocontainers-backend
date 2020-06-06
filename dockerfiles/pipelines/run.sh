#!/bin/bash

cd /biocontainers-backend/biocontainers/
python pipelines.py \
    --config-file configuration.ini \
    --db-password $MONGODB_PASS --db-host $MONGODB_HOST --db-auth-database $MONGODB_ADMIN_DB \
    --db-name $BIOCONT_DB_NAME --db-user $MONGODB_USER  $PIPELINE_ARGS

CODE=$?

if [ $CODE -eq 0 ]
then
     MSG='biocontainer-pipelines finished SUCCESSFULLY'
else
     MSG='ERROR: biocontainer-pipelines FAILED with return code: '$CODE
fi

echo $MSG

if [ -z "$SLACK_REPORT_URL" ]
then
      echo "no slack reporting"
else
      echo "sending report to slack"
      curl -X POST --data-urlencode "payload={\"channel\": \"#$SLACK_CHANNEL\", \"username\": \"biocontainer-report-bot\", \"text\": \"$MSG\", \"icon_emoji\": \":biocontainer-logo:\"}" $SLACK_REPORT_URL
fi