import logging
from pymodm import connect
from biocontainers.common.models import MongoTool
import click
import yaml
import requests

logger = logging.getLogger('annotations_yml_generator')


def print_help(ctx, value):
    if value is False:
        return
    click.echo(ctx.get_help())
    ctx.exit()


def get_database_uri(param):
    uri = 'mongodb://' + param['MONGODB_USER'] + ":" + param['MONGODB_PASS'] + '@' + param['MONGODB_HOST'] + ':' + \
          param['MONGO_PORT'] + '/' + param['BIOCONT_DB_NAME'] + '?ssl=false&authSource=' + param['MONGODB_ADMIN_DB']
    return uri


@click.command()
@click.option('-db', '--db-name', help="Name of the database", envvar='BIOCONT_DB_NAME')
@click.option('-h', '--db-host', help='Host the database', envvar='MONGODB_HOST')
@click.option('-a', '--db-auth-database', help='Authentication database in Mongo', envvar='MONGODB_ADMIN_DB')
@click.option('-u', '--db-user', help='Database root user', envvar='MONGODB_USER', default='admin')
@click.option('-pw', '--db-password', help='Database password', envvar='MONGODB_PASS')
@click.option('-p', '--db-port', help='Database port', envvar='MONGO_PORT', default='27017')
@click.option('-ay', '--annotations-yml-url', help='Annotations Yaml file')
@click.option('-st', '--slack-token', help='Slack  token')
@click.pass_context
def main(ctx, db_name, db_host, db_auth_database, db_user, db_password, db_port, annotations_yml_url, slack_token):
    config = {}
    if (db_name is None) or (db_host is None) or (db_user is None) or (annotations_yml_url is None):
        print_help(ctx, value=True)
    else:
        config['BIOCONT_DB_NAME'] = db_name
        config['MONGODB_HOST'] = db_host
        config['MONGO_PORT'] = db_port
        config['MONGODB_USER'] = db_user
        config['MONGODB_ADMIN_DB'] = db_auth_database
        config['MONGODB_PASS'] = db_password
        config['DATABASE_URI'] = get_database_uri(config)

    db_uri = get_database_uri(config)
    connect(db_uri)
    tools = list(MongoTool.get_all_tools())

    i = len(tools)
    print("Total tools: {}".format(i))

    yml_tools = set()

    outfile = requests.get(annotations_yml_url).text
    yml_contents = yaml.load(outfile, Loader=yaml.FullLoader)

    for key, value in yml_contents.items():
        yml_tools.add(str(key))

    print("total yaml tools: {}".format(len(yml_tools)))

    missing_tools = []
    for tool in tools:
        if tool.id not in yml_tools:
            tool1 = {tool.id: {'name': tool.id, 'description': tool.description, 'license': tool.license,
                               'home_url': tool.home_url, 'total_pulls': tool.total_pulls, 'manually_check': False,
                               'identifiers': tool.additional_identifiers, 'keywords': tool.tool_tags}}

            # print(tool1)
            missing_tools.append(tool1)

    # print(missing_tools)
    out_yml = 'out.yml'
    with open(out_yml, 'w') as outfile:
        yaml.dump(missing_tools, outfile)

    if slack_token is None:
        logger.info("Slack token is empty: skipping sending to slack")
    else:
        url = 'https://slack.com/api/files.upload'
        data = {'initial_comment': 'Missing annotations', 'channels': 'biocontainers'}
        files = {'file': open(out_yml, 'rb')}
        headers = {"Authorization": "Bearer " + slack_token}
        x = requests.post(url, data=data, files=files, headers=headers)
        print(x.status_code)
        print(x.text)
        logger.info("response sending to slack: {} {}".format(x.status_code, x.text))

if __name__ == "__main__":
    main()
