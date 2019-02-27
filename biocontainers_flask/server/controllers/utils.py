from biocontainers.common.models import MongoToolVersion, MongoTool
from biocontainers_flask.server.models import ToolClass, Tool, ToolVersion
from biocontainers_flask.server.models.container_image import ContainerImage

_PUBLIC_REGISTRY_URL = "http://api.biocontainers.pro/api/v2/"


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
    :param dic_tool_class:
    :return:
    """
    tool_class = ToolClass()
    tool_class.id = dic_tool_class['id']
    tool_class.description = dic_tool_class['description']
    tool_class.name = dic_tool_class['name']
    return tool_class


def transform_mongo_tool_dict(mongo_tool):
    tool = Tool()
    tool.id = mongo_tool["id"]
    tool.description = mongo_tool["description"]
    tool.organization = mongo_tool["organization"]
    # By default all our tools will be declare as verified
    tool.verified = True
    tool.author = MongoTool.get_main_author_dict(mongo_tool["authors"])
    tool.toolname = mongo_tool["name"]
    tool.url = _PUBLIC_REGISTRY_URL + "tools/" + tool.id

    # Set the Tool Class
    mongo_tool_class = MongoTool.get_main_tool_class_dict(mongo_tool["tool_classes"])
    tool.toolclass = transform_dic_tool_class(mongo_tool_class)

    tool.versions = []

    for mongo_tool_version in mongo_tool["tool_versions"]:
        tool.versions.append(transform_tool_version_dict(mongo_tool_version, mongo_tool["id"]))

    return tool


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
        tool.versions.append(transform_tool_version(mongo_tool_version, mongo_tool.id))

    return tool


def transform_tool_version(mongo_tool_version: MongoToolVersion, mongo_tool_id: str) -> ToolVersion:
    """
    This method retrieve the ToolVersion for an MongoToolVersion.
    :param mongo_tool_version: MongoToolVersion to be Transformed
    :param mongo_tool_id: Tool id
    :return:
    """
    tool_version = ToolVersion()
    tool_version.id = mongo_tool_version.id
    # Todo: We should not hard-coded this in the future. This should be dynamically pick
    tool_version.url = _PUBLIC_REGISTRY_URL + "tools/" + mongo_tool_id + "/versions/" + tool_version.id
    tool_version.name = mongo_tool_version.name
    tool_version.meta_version = mongo_tool_version.version
    container_images = []
    for old_container_image in mongo_tool_version.image_containers:
        container_image = ContainerImage()
        container_image.full_tag = old_container_image.full_tag
        container_image.downloads = old_container_image.downloads
        container_image.size = old_container_image.size
        container_image.container_type = old_container_image.container_type
        container_image.last_updated = old_container_image.last_updated

        container_images.append(container_image)
    tool_version.container_images = container_images

    return tool_version


def transform_tool_version_dict(mongo_tool_version, mongo_tool_id: str) -> ToolVersion:
    """
    This method retrieve the ToolVersion for an MongoToolVersion.
    :param mongo_tool_version: MongoToolVersion to be Transformed
    :param mongo_tool_id: Tool id
    :return:
    """
    tool_version = ToolVersion()
    tool_version.id = mongo_tool_version["id"]
    # Todo: We should not hard-coded this in the future. This should be dynamically pick
    tool_version.url = _PUBLIC_REGISTRY_URL + "tools/" + mongo_tool_id + "/versions/" + tool_version.id
    tool_version.name = mongo_tool_version.name
    tool_version.meta_version = mongo_tool_version.version
    container_images = []
    for old_container_image in mongo_tool_version.image_containers:
        container_image = ContainerImage()
        container_image.full_tag = old_container_image.full_tag
        container_image.downloads = old_container_image.downloads
        container_image.size = old_container_image.size
        container_image.container_type = old_container_image.container_type
        container_image.last_updated = old_container_image.last_updated

        container_images.append(container_image)
    tool_version.container_images = container_images

    return tool_version
