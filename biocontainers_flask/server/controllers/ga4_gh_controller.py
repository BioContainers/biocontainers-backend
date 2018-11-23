import connexion
import six

from biocontainers.common.models import MongoTool, _CONSTANT_TOOL_CLASSES
from biocontainers_flask.server.controllers.utils import transform_mongo_tool, transform_mongo_tool_class, \
    transform_dic_tool_class
from biocontainers_flask.server.models.error import Error  # noqa: E501
from biocontainers_flask.server.models.file_wrapper import FileWrapper  # noqa: E501
from biocontainers_flask.server.models.metadata import Metadata  # noqa: E501
from biocontainers_flask.server.models.tool import Tool  # noqa: E501
from biocontainers_flask.server.models.tool_class import ToolClass  # noqa: E501
from biocontainers_flask.server.models.tool_file import ToolFile  # noqa: E501
from biocontainers_flask.server.models.tool_version import ToolVersion  # noqa: E501
from biocontainers_flask.server import util


def metadata_get():  # noqa: E501
    """Return some metadata that is useful for describing this registry

    Return some metadata that is useful for describing this registry # noqa: E501


    :rtype: Metadata
    """
    metadata = Metadata(version="2.0", api_version="2.0", country="Europe", friendly_name="BioContainers API")
    return metadata


def tool_classes_get():  # noqa: E501
    """List all tool types

    This endpoint returns all tool-classes available  # noqa: E501


    :rtype: List[ToolClass]
    """
    tool_classes = []
    for key in _CONSTANT_TOOL_CLASSES:
        tool_classes.append(transform_dic_tool_class(_CONSTANT_TOOL_CLASSES[key]))

    return tool_classes


def tools_get(id=None, alias=None, registry=None, organization=None, name=None, toolname=None, description=None,
              author=None, checker=None, offset=None, limit=None):  # noqa: E501
    """List all tools

    This endpoint returns all tools available or a filtered subset using metadata query parameters.  # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param alias: OPTIONAL for tool registries that support aliases. If provided will only return entries with the given alias.
    :type alias: str
    :param registry: The image registry that contains the image.
    :type registry: str
    :param organization: The organization in the registry that published the image.
    :type organization: str
    :param name: The name of the image.
    :type name: str
    :param toolname: The name of the tool.
    :type toolname: str
    :param description: The description of the tool.
    :type description: str
    :param author: The author of the tool (TODO a thought occurs, are we assuming that the author of the CWL and the image are the same?).
    :type author: str
    :param checker: Return only checker workflows
    :type checker: bool
    :param offset: Start index of paging. Pagination results can be based on numbers or other values chosen by the registry implementor (for example, SHA values). If this exceeds the current result set return an empty set.  If not specified in the request, this will start at the beginning of the results.
    :type offset: str
    :param limit: Amount of records to return in a given page.
    :type limit: int

    :rtype: List[Tool]
    """
    mongo_tools = MongoTool.get_all_tools()
    tools = []
    for mongo_tool in mongo_tools:
        # Transform the mongo tool to API tool
        mongo_tool_versions = mongo_tool.get_tool_versions()
        tool = transform_mongo_tool(mongo_tool, mongo_tool_versions)
        tools.append(tool)

    return tools


def tools_id_get(id):  # noqa: E501
    """List one specific tool, acts as an anchor for self references

    This endpoint returns one specific tool (which has ToolVersions nested inside it) # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str

    :rtype: Tool
    """
    mongo_tool = MongoTool.get_tool_by_id(id)
    if mongo_tool is not None:
        mongo_tool_versions = mongo_tool.get_tool_versions()
        return transform_mongo_tool(mongo_tool, mongo_tool_versions)

    return None


def tools_id_versions_get(id):  # noqa: E501
    """List versions of a tool

    Returns all versions of the specified tool # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str

    :rtype: List[ToolVersion]
    """
    return 'do some magic!'


def tools_id_versions_version_id_containerfile_get(id, version_id):  # noqa: E501
    """Get the container specification(s) for the specified image.

    Returns the container specifications(s) for the specified image. For example, a CWL CommandlineTool can be associated with one specification for a container, a CWL Workflow can be associated with multiple specifications for containers # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;
    :type version_id: str

    :rtype: List[FileWrapper]
    """
    return 'do some magic!'


def tools_id_versions_version_id_get(id, version_id):  # noqa: E501
    """List one specific tool version, acts as an anchor for self references

    This endpoint returns one specific tool version # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param version_id: An identifier of the tool version, scoped to this registry, for example &#x60;v1&#x60;
    :type version_id: str

    :rtype: ToolVersion
    """
    return 'do some magic!'


def tools_id_versions_version_id_type_descriptor_get(type, id, version_id):  # noqa: E501
    """Get the tool descriptor for the specified tool

    Returns the descriptor for the specified tool (examples include CWL, WDL, or Nextflow documents). # noqa: E501

    :param type: The output type of the descriptor. If not specified, it is up to the underlying implementation to determine which output type to return. Plain types return the bare descriptor while the \&quot;non-plain\&quot; types return a descriptor wrapped with metadata. Allowable values include \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;PLAIN_CWL\&quot;, \&quot;PLAIN_WDL\&quot;, \&quot;PLAIN_NFL\&quot;.
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param version_id: An identifier of the tool version, scoped to this registry, for example &#x60;v1&#x60;
    :type version_id: str

    :rtype: FileWrapper
    """
    return 'do some magic!'


def tools_id_versions_version_id_type_descriptor_relative_path_get(type, id, version_id, relative_path):  # noqa: E501
    """Get additional tool descriptor files relative to the main file

    Descriptors can often include imports that refer to additional descriptors. This returns additional descriptors for the specified tool in the same or other directories that can be reached as a relative path. This endpoint can be useful for workflow engine implementations like cwltool to programmatically download all the descriptors for a tool and run it. This can optionally include other files described with FileWrappers such as test parameters and containerfiles.  # noqa: E501

    :param type: The output type of the descriptor. If not specified, it is up to the underlying implementation to determine which output type to return. Plain types return the bare descriptor while the \&quot;non-plain\&quot; types return a descriptor wrapped with metadata. Allowable values are \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;PLAIN_CWL\&quot;, \&quot;PLAIN_WDL\&quot;, \&quot;PLAIN_NFL\&quot;.
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;
    :type version_id: str
    :param relative_path: A relative path to the additional file (same directory or subdirectories), for example &#39;foo.cwl&#39; would return a &#39;foo.cwl&#39; from the same directory as the main descriptor. &#39;nestedDirectory/foo.cwl&#39; would return the file  from a nested subdirectory.  Unencoded paths such &#39;sampleDirectory/foo.cwl&#39; should also be allowed
    :type relative_path: str

    :rtype: FileWrapper
    """
    return 'do some magic!'


def tools_id_versions_version_id_type_files_get(type, id, version_id):  # noqa: E501
    """Get a list of objects that contain the relative path and file type

    Get a list of objects that contain the relative path and file type. The descriptors are intended for use with the /tools/{id}/versions/{version_id}/{type}/descriptor/{relative_path} endpoint. # noqa: E501

    :param type: The output type of the descriptor. Examples of allowable values are \&quot;CWL\&quot;, \&quot;WDL\&quot;, and \&quot;NextFlow.\&quot;
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;
    :type version_id: str

    :rtype: List[ToolFile]
    """
    return 'do some magic!'


def tools_id_versions_version_id_type_tests_get(type, id, version_id):  # noqa: E501
    """Get a list of test JSONs

    Get a list of test JSONs (these allow you to execute the tool successfully) suitable for use with this descriptor type. # noqa: E501

    :param type: The type of the underlying descriptor. Allowable values include \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;PLAIN_CWL\&quot;, \&quot;PLAIN_WDL\&quot;, \&quot;PLAIN_NFL\&quot;. For example, \&quot;CWL\&quot; would return an list of ToolTests objects while \&quot;PLAIN_CWL\&quot; would return a bare JSON list with the content of the tests. 
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;
    :type version_id: str

    :rtype: List[FileWrapper]
    """
    return 'do some magic!'