class PipelineConfiguration:
    def __init__(self, docker_hub, docker_hub_container, docker_hub_tags):
        self.dockerHub = docker_hub
        self.dockerHubContainer = docker_hub_container
        self.dockerHubTags = docker_hub_tags


class ContainerImage:
    """ This class handle how a container is build. Singularity, Docker, Conda, etc. """
    maintainers = []

    def __init__(self, tag, full_tag, container_type, binary_urls, description, recipe_url, license, software_url,
                 doc_url, additional_metadata):
        self.tag = tag
        """quay.io/biocontainers/abaca:1.2 --python"""
        self.full_tag = full_tag
        self.container_type = container_type
        self.binary_urls = binary_urls
        self.description = description
        self.recipe_url = recipe_url
        self.license = license
        self.software_url = software_url
        self.doc_url = doc_url
        self.additional_metadata = additional_metadata

    def update_size(self, size):
        self.size = size

    def update_downloads(self, downloads):
        self.downloads = downloads

    def update_last_update(self, last_update):
        self.last_update = last_update

    def add_maintainer(self, maintainer):
        self.maintainers.append(maintainer)


class Tool:
    """
    This class contains the information about a tool (PeptideShacker) in Biocontainers, it can be a tool, a workflow, a service or a multi-tool container
    """
    tool_classes = []
    authors = []
    tool_contains = []
    tool_versions = []
    additional_identifiers = []

    def __init__(self, id, name, description, home_url, last_version, organization, has_checker, checker_url,
                 is_verified, verified_source, registry_url, license, additional_metadata):
        self.id = id
        self.name = name
        self.description = description
        self.home_url = home_url
        self.last_version = last_version
        self.organization = organization
        self.has_checker = has_checker
        self.checker_url = checker_url
        self.is_verified = is_verified
        self.verified_source = verified_source
        self.registry_url = registry_url
        self.license = license
        self.additional_metadata = additional_metadata

    def add_tool_class(self, tool_class):
        self.tool_classes.append(tool_class)


class ToolVersion:
    """
    This class store the information of a Tool version (e.g. PeptideShacker 2.0 )
    """
    tool_classes = []
    descriptors = []
    image_containers = []
    tool_contains = []
    authors = []

    def __init__(self, id, name, version, description, home_url, doc_url, license, additional_identifiers, hash_name,
                 last_update, additional_metadata):
        self.id = id
        self.name = name
        self.version = version
        self.description = description
        self.home_url = home_url
        self.doc_url = doc_url
        self.license = license
        self.additional_identifiers = additional_identifiers
        self.hash_name = hash_name
        self.last_update = last_update
        self.additional_metadata = additional_metadata

    def update_downloads(self, downloads):
        self.downloads = downloads

    def add_tool_class(self, tool_class):
        self.tool_classes.append(tool_class)

    def add_image_container(self, image_container):
        self.image_containers.append(image_container)
