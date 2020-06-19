from biocontainers.common.models import MongoToolVersion, MongoTool, Facet
from biocontainers_flask.server.models import ToolClass, Tool, ToolVersion, Facet, FacetValue, ImageData, ImageType
from biocontainers_flask.server.models.container_image import ContainerImage

_PUBLIC_REGISTRY_URL = "http://api.biocontainers.pro/ga4gh/trs/v2/"
_FACET_PROPERTIES = ['licenses', 'tool_tags']


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
    if 'license' in mongo_tool:
        tool.license = mongo_tool['license']
    # By default all our tools will be declare as verified
    tool.verified = True
    tool.author = MongoTool.get_main_author_dict(mongo_tool["authors"])
    tool.name = mongo_tool["name"]
    tool.url = _PUBLIC_REGISTRY_URL + "tools/" + tool.id
    count = 0
    if 'total_pulls' in mongo_tool:
        count = mongo_tool['total_pulls']
    tool.pulls = count

    if 'tool_tags' in mongo_tool and len(mongo_tool['tool_tags']) > 0:
        tool.tool_tags = mongo_tool['tool_tags']

    # Set the Tool Class
    mongo_tool_class = MongoTool.get_main_tool_class_dict(mongo_tool["tool_classes"])
    tool.toolclass = transform_dic_tool_class(mongo_tool_class)
    if 'home_url' in mongo_tool:
        tool.tool_url = mongo_tool['home_url']

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
    tool.license = mongo_tool.license
    tool.toolname = mongo_tool.name
    tool.pulls = mongo_tool.get_pulls()
    tool.url = _PUBLIC_REGISTRY_URL + "tool/" + tool.id

    # Set the Tool Class
    mongo_tool_class = mongo_tool.get_main_tool_class()
    tool.toolclass = transform_mongo_tool_class(mongo_tool_class)
    tool.tool_url = mongo_tool.home_url

    tool.versions = []

    for mongo_tool_version in mongo_tool_versions:
        tool.versions.append(transform_tool_version(mongo_tool_version, mongo_tool.id))

    return tool


def transform_mongo_tool(mongo_tool):
    tool = Tool()
    tool.id = mongo_tool.id
    tool.description = mongo_tool.description
    # By default all our tools will be declare as verified
    tool.verified = True
    tool.author = mongo_tool.get_main_author()
    tool.license = mongo_tool.license
    tool.toolname = mongo_tool.name
    tool.url = _PUBLIC_REGISTRY_URL + "tool/" + tool.id

    # Set the Tool Class
    mongo_tool_class = mongo_tool.get_main_tool_class()
    tool.toolclass = transform_mongo_tool_class(mongo_tool_class)
    tool.tool_url = mongo_tool.home_url

    tool.versions = []

    return tool


def get_facets(mongo_tools):
    licenses = {}
    tool_tags = {}
    for tool in mongo_tools:
        if 'license' in tool:
            if tool['license'] in licenses:
                licenses[tool['license']] = licenses[tool['license']] + 1
            else:
                licenses[tool['license']] = 1
        if 'tool_tags' in tool:
            for tag in tool['tool_tags']:
                if tag in tool_tags:
                    tool_tags[tag] = tool_tags[tag] + 1
                else:
                    tool_tags[tag] = 1

    facets = []
    if len(licenses) > 0:
        facetValues = []
        for license in licenses:
            facetValue = FacetValue(license, licenses[license])
            facetValues.append(facetValue)
        facets.append(Facet('licenses', facetValues))
    if len(tool_tags) > 0:
        facetValues = []
        for tag in tool_tags:
            facetValue = FacetValue(tag, tool_tags[tag])
            facetValues.append(facetValue)
        facets.append(Facet('tool_tags', facetValues))
    return facets


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
        container_image = ImageData()

        container_image.registry_host = 'registry.hub.docker.com'
        if 'quay.io' in old_container_image.full_tag:
            container_image.registry_host = 'quay.io/'
            container_image.image_type = ImageType.DOCKER
        if old_container_image.container_type == 'CONDA':
            container_image.registry_host = 'http://anaconda.org/'
            container_image.image_type = ImageType.CONDA
        if old_container_image.container_type == 'SINGULARITY':
            container_image.registry_host = 'depot.galaxyproject.org/singularity/'
            container_image.image_type = ImageType.SINGULARITY
        if 'containers.biocontainers.pro' in old_container_image.full_tag:
            container_image.registry_host = 'containers.biocontainers.pro'
            container_image.image_type = ImageType.DOCKER

        container_image.image_name = old_container_image.full_tag
        container_image.downloads = old_container_image.downloads
        container_image.size = old_container_image.size
        container_image.updated = old_container_image.last_updated
        container_images.append(container_image)

    tool_version.images = container_images

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
    tool_version.name = mongo_tool_version['name']
    tool_version.meta_version = mongo_tool_version['version']
    container_images = []
    for old_container_image in mongo_tool_version['image_containers']:
        container_image = ContainerImage()
        if 'full_tag' in old_container_image:
            container_image.full_tag = old_container_image['full_tag']
        if 'downloads' in old_container_image:
            container_image.downloads = old_container_image['downloads']
        if 'size' in old_container_image:
            container_image.size = old_container_image['size']
        if 'container_type' in old_container_image:
            container_image.container_type = old_container_image['container_type']
        if 'last_updated' in old_container_image:
            container_image.last_updated = old_container_image['last_updated']
        container_images.append(container_image)

    tool_version.container_images = container_images

    return tool_version
