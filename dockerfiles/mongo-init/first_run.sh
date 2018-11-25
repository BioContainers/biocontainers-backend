#!/bin/bash

# Create User
echo "Creating user: \"$USER\"..."
mongo  --host $MONGODB_HOST --username $ADMIN_USER --password $ADMIN_PASSWORD --eval "db.createUser({ user: '$MONGODB_USER', pwd: '$MONGODB_PASS', roles: [ { role: '$MONGODB_ROLES', db: '$MONGO_DB' } ] });"


echo "========================================================================"
echo "MongoDB User: \"$USER\""
echo "MongoDB Password: \"$PASS\""
echo "MongoDB Database: \"$DB\""
echo "MongoDB Role: \"$ROLE\""
echo "========================================================================"
