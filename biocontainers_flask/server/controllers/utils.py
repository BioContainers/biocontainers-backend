from biocontainers_flask.server.models import ToolClass, Tool, ToolVersion

_PUBLIC_REGISTRY_URL = "http://biocontainers.pro/registry/"


def transform_mongo_tool_class(mongo_tool_class):
    """
    This method transform a Mongo Tool Class to an API Tool Class.
    :param mongo_tool_class:
    :return:
    """
    tool_class = ToolClass()
    tool_class.id = mongo_tool_class.id
    tool_class.description = mongo_tool_class.description
    tool_class.name = mongo_tool_class.name
    return tool_class


def transform_dic_tool_class(dic_tool_class):
    """
    This method transform a Mongo Tool Class to an API Tool Class.
    :param mongo_tool_class:
    :return:
    """
    tool_class = ToolClass()
    tool_class.id = dic_tool_class['id']
    tool_class.description = dic_tool_class['description']
    tool_class.name = dic_tool_class['name']
    return tool_class


def transform_mongo_tool(mongo_tool, mongo_tool_versions):
    tool = Tool()
    tool.id = mongo_tool.id
    tool.description = mongo_tool.description
    # By default all our tools will be declare as verified
    tool.verified = True
    tool.author = mongo_tool.get_main_author()
    tool.toolname = mongo_tool.name
    tool.url = _PUBLIC_REGISTRY_URL + "tool/" + tool.id

    # Set the Tool Class
    mongo_tool_class = mongo_tool.get_main_tool_class()
    tool.toolclass = transform_mongo_tool_class(mongo_tool_class)

    tool.versions = []

    for mongo_tool_version in mongo_tool_versions:
        tool_version = ToolVersion()
        tool_version.id = mongo_tool_version.id
        # Todo: We should not hard-coded this in the future. This should be dynamically pick
        tool_version.url = _PUBLIC_REGISTRY_URL + "tool/" + tool.id + "/version" + tool_version.id
        tool.versions.append(tool_version)

    return tool
