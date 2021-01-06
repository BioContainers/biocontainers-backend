import logging

import yaml
from pymodm import connect
from biocontainers.common.models import MongoTool
import click
from ruamel.yaml import YAML
import requests

logger = logging.getLogger('misc_jobs')


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
@click.option('--find-missing-annotations', '-ma', help='Find missing annotations', is_flag=True)
@click.option('--find-duplicate-tools', '-dt', help='Find duplicate tools', is_flag=True)
@click.option('--find-invalid-annotations', '-ia', help='invalid_annotations', is_flag=True)
@click.option('-ay', '--annotations-yml-url', help='Annotations Yaml file')
@click.option('-db', '--db-name', help="Name of the database", envvar='BIOCONT_DB_NAME')
@click.option('-h', '--db-host', help='Host the database', envvar='MONGODB_HOST')
@click.option('-a', '--db-auth-database', help='Authentication database in Mongo', envvar='MONGODB_ADMIN_DB')
@click.option('-u', '--db-user', help='Database root user', envvar='MONGODB_USER', default='admin')
@click.option('-pw', '--db-password', help='Database password', envvar='MONGODB_PASS')
@click.option('-p', '--db-port', help='Database port', envvar='MONGO_PORT', default='27017')
@click.option('-st', '--slack-token', help='Slack  token')
@click.pass_context
def main(ctx, find_missing_annotations, find_duplicate_tools, find_invalid_annotations, annotations_yml_url, db_name,
         db_host, db_auth_database,
         db_user, db_password, db_port, slack_token):
    config = {}
    if (db_name is None) or (db_host is None) or (db_user is None):
        print_help(ctx, value=True)
    elif ((find_missing_annotations is True) or (find_invalid_annotations is True)) and (annotations_yml_url is None):
        print_help(ctx, value=True)
    else:
        config['BIOCONT_DB_NAME'] = db_name
        config['MONGODB_HOST'] = db_host
        config['MONGO_PORT'] = db_port
        config['MONGODB_USER'] = db_user
        config['MONGODB_ADMIN_DB'] = db_auth_database
        config['MONGODB_PASS'] = db_password
        config['DATABASE_URI'] = get_database_uri(config)

    tools = []
    if find_missing_annotations is True or find_duplicate_tools is True:
        db_uri = get_database_uri(config)
        connect(db_uri)
        tools = list(MongoTool.get_all_tools())
        i = len(tools)
        print("Total tools: {}".format(i))

    if find_missing_annotations is True:
        missing_annotations(annotations_yml_url, tools, slack_token)

    if find_duplicate_tools is True:
        duplicate_tools(tools, slack_token)

    if find_invalid_annotations is True:
        invalid_annotations(annotations_yml_url)


def duplicate_tools(tools, slack_token):
    biotools = {}
    for tool in tools:
        if tool.additional_identifiers:
            for i in tool.additional_identifiers:
                if str(i).startswith("biotools:"):
                    add_tool(biotools, i, tool.id)

    for biotool in biotools:
        print(biotool)

    # out_yml = 'duplicate_tools.yml'
    # with open(out_yml, 'w') as outfile:
    #     yaml.dump(missing_tools, outfile)

    # slack_notify(out_yml, slack_token)


def invalid_annotations(annotations_yml_url):
    yml_tools = []
    outfile = requests.get(annotations_yml_url).text
    yml_contents = yaml.load(outfile, Loader=yaml.FullLoader)
    for key, value in yml_contents.items():
        yml_tools.append(value)
    print("total yaml tools: {}".format(len(yml_tools)))

    missing_home_urls = []
    missing_licenses = []
    for tool in yml_tools:
        tool_keys = tool.keys()
        if 'home_url' not in tool_keys:
            missing_home_urls.append(tool['name'])
        if 'license' not in tool_keys:
            missing_licenses.append(tool['name'])

    print(missing_home_urls)
    print(missing_licenses)


def add_tool(biotools, identifier, tool_id):
    if identifier not in biotools:
        biotools[identifier] = []
    biotools[identifier].append(tool_id)


def missing_annotations(annotations_yml_url, tools, slack_token):
    yaml = YAML()
    yml_tools = set()
    outfile = requests.get(annotations_yml_url).text
    yml_contents = yaml.load(outfile)
    for key, value in yml_contents.items():
        yml_tools.add(str(key))
    print("total yaml tools: {}".format(len(yml_tools)))
    missing_tools = []
    for tool in tools:
        if (not str(tool.id).startswith("mulled-")) and (tool.id not in yml_tools):
            tool1 = {tool.id: {'name': tool.id, 'description': tool.description, 'license': tool.license,
                               'home_url': tool.home_url, 'total_pulls': tool.total_pulls, 'manually_check': False,
                               'identifiers': tool.additional_identifiers, 'keywords': tool.tool_tags}}

            # print(tool1)
            missing_tools.append(tool1)
    # print(missing_tools)
    out_yml = 'missing_annotations.yml'
    with open(out_yml, 'w') as outfile:
        yaml.dump(missing_tools, outfile)

    slack_notify(out_yml, slack_token)


def slack_notify(out_yml, slack_token):
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
