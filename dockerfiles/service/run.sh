#!/bin/bash

#   --mongodb.biocontainers.db.authenticationDatabase= \
#  --mongodb.biocontainers.db.port= \

cat > mongo_exec.js <<- EOM
db = db.getSiblingDB('admin');
try {
  db.createUser({ user: "$MONGODB_USER" , pwd: "$MONGODB_PASS", roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"] });
} catch(err) {
  print("Could not create user: "+err.message )
  print("Trying to add role to existing user")
  db.grantRolesToUser( "$MONGODB_USER", ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"] );
}
/* uncomment for debugging
printjson( db.getUser( "$MONGODB_USER", {
   showCredentials: false,
   showPrivileges: true,
   showAuthenticationRestrictions: true
} ) )
*/
EOM

cat mongo_exec.js


mongo --host $MONGODB_HOST -u root -p $MONGO_ROOT_PASS --authenticationDatabase \
  $MONGODB_ADMIN_DB mongo_exec.js

python /biocontainers-backend/biocontainers_flask/server/server.py --db-name $BIOCONT_DB_NAME --db-host $MONGODB_HOST \
  --db-auth-database $MONGODB_ADMIN_DB  --db-user $MONGODB_USER --db-password $MONGODB_PASS

