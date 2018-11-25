#!/usr/bin/env python3

import click
import connexion
from pymodm import connect

from biocontainers_flask.server import encoder

_PUBLIC_REGISTRY_URL = "http://biocontainers.pro/registry/"


@staticmethod
def connect_to_db(db_name, db_host, db_auth_database, db_user, db_password, db_port):
    uri = 'mongodb://' + db_user + ":" + db_password + '@' + db_host + ':' + \
          db_port + '/' + db_name + '?ssl=true&replicaSet=mongo-shard-0&authSource=' + db_auth_database
    connect(uri, 'api-alias')


def print_help(ctx, param, value):
    if value is False:
        return
    click.echo(ctx.get_help())
    ctx.exit()

@click.command()
@click.option('-db', '--db-name', help="Name of the database", envvar='BIOCONT_DB_NAME')
@click.option('-h', '--db-host', help='Host the database', envvar='MONGODB_HOST')
@click.option('-a', '--db-auth-database', help='Authentication database in Mongo', envvar='MONGODB_ADMIN_DB')
@click.option('-u', '--db-user', help='Database root user', envvar='MONGODB_USER', default='admin')
@click.option('-pw', '--db-password', help='Database password', envvar='MONGODB_PASS')
@click.option('-p', '--db-port', help='Database port', envvar='MONGO_PORT', default='27017')
@click.option('--help', is_flag=True, expose_value=False, is_eager=False, callback=print_help,
              help="Print help message")
@click.pass_context
def main(ctx, db_name, db_host, db_auth_database, db_user, db_password, db_port):
    if (db_name is None) or (db_host is None) or (db_user is None):
        print_help(ctx, None, value=True)
    connect_to_db(db_name, db_host, db_auth_database, db_user, db_password, db_port)
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'GA4GH Tool Discovery API'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
