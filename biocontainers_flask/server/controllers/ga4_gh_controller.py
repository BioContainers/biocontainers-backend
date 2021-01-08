import json

from flask import request
from pymongo.errors import DuplicateKeyError
from werkzeug.urls import url_encode

from biocontainers.biomongo.helpers import InsertContainers

from biocontainers.common.models import MongoTool, _CONSTANT_TOOL_CLASSES, MongoToolVersion, MongoWorkflow, SimilarTool
from biocontainers_flask.server.controllers.utils import transform_dic_tool_class, \
    transform_tool_version, transform_mongo_tool_dict, transform_mongo_tool, get_facets

from biocontainers_flask.server.models.file_wrapper import FileWrapper  # noqa: E501
from biocontainers_flask.server.models.stat import Stat
from biocontainers_flask.server.models.tool import Tool  # noqa: E501
from biocontainers_flask.server.models.tool_version import ToolVersion  # noqa: E501
from biocontainers_flask.server.models.workflow import Workflow


def facets_get(id=None, alias=None, tool_class=None, registry=None, organization=None, name=None, toolname=None,
               description=None, author=None, checker=None, facets=None,
               all_fields_search=None):  # noqa: E501
    """Facets all the properties from tools

    This endpoint returns all facets properties available or a filtered subset using  metadata query parameters.  # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param alias: Support for this parameter is optional for tool registries that support aliases. If provided will only return entries with the given alias.
    :type alias: str
    :param tool_class: Filter tools by the name of the subclass (#/definitions/ToolClass)
    :type tool_class: str
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
    :param checker: Return only checker workflows.
    :type checker: bool
    :param offset: Start index of paging. Pagination results can be based on numbers or other values chosen by the registry implementor (for example, SHA values). If this exceeds the current result set return an empty set.  If not specified in the request, this will start at the beginning of the results.
    :type offset: str
    :param limit: Amount of records to return in a given page.
    :type limit: int

    :rtype: List[Facet]
    """
    tools = []
    is_all_field_search = False
    license = None
    tool_tags = None
    if all_fields_search is not None:
        id = license = tool_tags = alias = organization = name = toolname = description = author = all_fields_search
        is_all_field_search = True

    facets_dic = {}
    if facets is not None:
        facets_list = facets.split(",")
        for facet in facets_list:
            value_list = facet.split(":")
            if value_list[0] not in facets_dic:
                facets_dic[value_list[0]] = []
                facets_dic[value_list[0]].append(value_list[1])
            else:
                facets_dic[value_list[0]].append(value_list[1])

    resp = MongoTool.get_tools(id=id, alias=alias, registry=registry, organization=organization, name=name,
                               toolname=toolname, description=description, author=author,
                               checker=checker, license=license, tool_tags=tool_tags, facets=facets_dic, offset=0,
                               limit=100000, is_all_field_search=is_all_field_search)

    if resp is None:
        return None

    mongo_tools = resp.tools
    facets = get_facets(mongo_tools)
    return facets


def tool_classes_get():  # noqa: E501
    """List all tool types

    This endpoint returns all tool-classes available.  # noqa: E501


    :rtype: List[ToolClass]
    """
    tool_classes = []
    for key in _CONSTANT_TOOL_CLASSES:
        tool_classes.append(transform_dic_tool_class(_CONSTANT_TOOL_CLASSES[key]))

    return tool_classes


def tools_get(id=None, alias=None, tool_class=None, registry=None, organization=None, name=None, toolname=None,
              description=None, author=None, checker=None, facets=None, offset=None, limit=None,
              all_fields_search=None, sort_field=None, sort_order=None):  # noqa: E501
    """List all tools

    This endpoint returns all tools available or a filtered subset using metadata query parameters.  # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param alias: Support for this parameter is optional for tool registries that support aliases. If provided will only return entries with the given alias.
    :type alias: str
    :param tool_class: Filter tools by the name of the subclass (#/definitions/ToolClass)
    :type tool_class: str
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
    :param author: The author of the tool
    (TODO a thought occurs, are we assuming that the author of the CWL and the image are the same?).
    :type author: str
    :param checker: Return only checker workflows.
    :type checker: bool
    :param offset: Start index of paging. Pagination results can be based on numbers or other values chosen by the registry implementor (for example, SHA values). If this exceeds the current result set return an empty set.  If not specified in the request, this will start at the beginning of the results.
    :type offset: str
    :param limit: Amount of records to return in a given page.
    :type limit: int
    :param all_fields_search: Search by all fields.
    :param sort_field: field to sort the results
    :param sort_order: sort order, asc or desc
    :rtype: List[Tool]
    """

    is_all_field_search = False
    license = None
    tool_tags = None

    if offset is None:
        offset = 0
    else:
        offset = int(offset)

    if all_fields_search is not None:
        id = license = tool_tags = alias = organization = name = toolname = description = author = all_fields_search
        is_all_field_search = True

    facets_dic = {}
    if facets is not None:
        facets_list = facets.split(",")
        if (len(facets_list) > 0):
            for facet in facets_list:
                value_list = facet.split(":")
                if (len(value_list) == 2):
                    if value_list[0] not in facets_dic:
                        facets_dic[value_list[0]] = []
                        facets_dic[value_list[0]].append(value_list[1])
                    else:
                        facets_dic[value_list[0]].append(value_list[1])

    resp = tools_get_common(id=id, alias=alias, registry=registry, organization=organization, name=name,
                            toolname=toolname, toolclass=tool_class, description=description, author=author,
                            checker=checker, license=license, tool_tags=tool_tags, facets=facets_dic, offset=offset,
                            limit=limit, is_all_field_search=is_all_field_search,
                            sort_field=sort_field, sort_order=sort_order)

    if resp is None:
        return None

    next_page = None
    if resp.next_offset is not None:
        args_next_page = request.args.copy()
        args_next_page['offset'] = resp.next_offset
        args_next_page['limit'] = limit
        next_page = '{}?{}'.format(request.base_url, url_encode(args_next_page))

    args_last_page = request.args.copy()
    args_last_page['offset'] = resp.last_page_offset
    args_last_page['limit'] = limit
    last_page = '{}?{}'.format(request.base_url, url_encode(args_last_page))

    return resp.tools, 200, {'next_page': next_page, 'last_page': last_page,
                             'self_link': request.url, 'current_offset': offset,
                             'current_limit': limit}


def tools_get_common(id=None, alias=None, registry=None, organization=None, name=None, toolname=None, toolclass=None,
                     description=None, author=None, checker=None, license=None, tool_tags=None, facets=None, offset=0,
                     limit=1000, is_all_field_search=False,
                     sort_field=None, sort_order=None):
    tools = []
    resp = MongoTool.get_tools(id=id, alias=alias, registry=registry, organization=organization, name=name,
                               toolname=toolname, toolclass=toolclass, description=description, author=author,
                               checker=checker, license=license, tool_tags=tool_tags, facets=facets, offset=offset,
                               limit=limit, is_all_field_search=is_all_field_search,
                               sort_field=sort_field, sort_order=sort_order)

    if resp is None:
        return None

    mongo_tools = resp.tools
    if mongo_tools is not None:
        for mongo_tool in mongo_tools:
            if ('anchor_tool' in mongo_tool) and (len(mongo_tool['anchor_tool']) > 0):
                continue  # don't include tools that have 'anchor_tool' field
            # Transform the mongo tool to API tool
            tool = transform_mongo_tool_dict(mongo_tool)
            tools.append(tool)
    # If the checker is provided, we filter for checker tools.
    if checker is not None:
        new_tools = []
        for tool in tools:
            if tool.has_checker == checker:
                new_tools.append(tool)
        tools = new_tools
    resp.tools = tools
    return resp


def tools_id_get(id):  # noqa: E501
    """List one specific tool, acts as an anchor for self references

    This endpoint returns one specific tool (which has ToolVersions nested inside it). # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str

    :rtype: Tool
    """
    resp = tools_get_common(id="^" + id + "$")  # regex to search for exact id
    if resp is not None and resp.tools is not None and len(resp.tools) > 0:
        return resp.tools[0]

    return None


def tools_id_versions_get(id):  # noqa: E501
    """List versions of a tool

    Returns all versions of the specified tool. # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str

    :rtype: List[ToolVersion]
    """
    mongo_tool = MongoTool.get_tool_by_id(id)
    anchor_tools = MongoTool.get_tool_with_anchor_tool_field(id)
    tool_versions = []
    if mongo_tool is not None:
        mongo_tool_versions = mongo_tool.get_tool_versions()
        if (anchor_tools is not None) and (len(anchor_tools) > 0):
            for a_tool in anchor_tools:
                mongo_tool_versions.extend(a_tool.get_tool_versions())
        for mongo_tool_version in mongo_tool_versions:
            tool_versions.append(transform_tool_version(mongo_tool_version, mongo_tool.id))

    return tool_versions


def tools_id_versions_version_id_containerfile_get(id, version_id):  # noqa: E501
    """Get the container specification(s) for the specified image.

    Returns the container specifications(s) for the specified image. For example, a CWL CommandlineTool can be associated with one specification for a container, a CWL Workflow can be associated with multiple specifications for containers. # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;.
    :type version_id: str

    :rtype: List[FileWrapper]
    """
    return 'No yet implemented!'


def tools_id_versions_version_id_get(id, version_id):  # noqa: E501
    """List one specific tool version, acts as an anchor for self references

    This endpoint returns one specific tool version. # noqa: E501

    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param version_id: An identifier of the tool version, scoped to this registry, for example &#x60;v1&#x60;. We recommend that versions use semantic versioning https://semver.org/spec/v2.0.0.html  (For example, &#x60;1.0.0&#x60; instead of &#x60;develop&#x60;)
    :type version_id: str

    :rtype: ToolVersion
    """
    mongo_tool = MongoTool.get_tool_by_id(id)
    tool_versions = []
    if mongo_tool is not None:
        mongo_tool_versions = mongo_tool.get_tool_versions()
        for mongo_tool_version in mongo_tool_versions:
            tool_versions.append(transform_tool_version(mongo_tool_version, mongo_tool.id))

    for tool_version in tool_versions:
        if tool_version.id == version_id:
            return tool_version

    return None


def tools_id_versions_version_id_type_descriptor_get(type, id, version_id):  # noqa: E501
    """Get the tool descriptor for the specified tool

    Returns the descriptor for the specified tool (examples include CWL, WDL, Nextflow, or Galaxy documents). # noqa: E501

    :param type: The output type of the descriptor. Plain types return the bare descriptor while the \&quot;non-plain\&quot; types return a descriptor wrapped with metadata. Allowable values include \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;GALAXY\&quot;, \&quot;PLAIN_CWL\&quot;, \&quot;PLAIN_WDL\&quot;, \&quot;PLAIN_NFL\&quot;, \&quot;PLAIN_GALAXY\&quot;.
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param version_id: An identifier of the tool version, scoped to this registry, for example &#x60;v1&#x60;.
    :type version_id: str

    :rtype: FileWrapper
    """
    return 'Not yet Implemented!'


def tools_id_versions_version_id_type_descriptor_relative_path_get(type, id, version_id, relative_path):  # noqa: E501
    """Get additional tool descriptor files relative to the main file

    Descriptors can often include imports that refer to additional descriptors. This returns additional descriptors for the specified tool in the same or other directories that can be reached as a relative path. This endpoint can be useful for workflow engine implementations like cwltool to programmatically download all the descriptors for a tool and run it. This can optionally include other files described with FileWrappers such as test parameters and containerfiles. # noqa: E501

    :param type: The output type of the descriptor. If not specified, it is up to the underlying implementation to determine which output type to return. Plain types return the bare descriptor while the \&quot;non-plain\&quot; types return a descriptor wrapped with metadata. Allowable values are \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;GALAXY\&quot;, \&quot;PLAIN_CWL\&quot;, \&quot;PLAIN_WDL\&quot;, \&quot;PLAIN_NFL\&quot;, \&quot;PLAIN_GALAXY\&quot;.
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;.
    :type version_id: str
    :param relative_path: A relative path to the additional file (same directory or subdirectories), for example &#x27;foo.cwl&#x27; would return a &#x27;foo.cwl&#x27; from the same directory as the main descriptor. &#x27;nestedDirectory/foo.cwl&#x27; would return the file  from a nested subdirectory.  Unencoded paths such &#x27;sampleDirectory/foo.cwl&#x27; should also be allowed.
    :type relative_path: str

    :rtype: FileWrapper
    """
    return 'Not yet implemented!'


def tools_id_versions_version_id_type_files_get(type, id, version_id, format=None):  # noqa: E501
    """Get a list of objects that contain the relative path and file type

    Get a list of objects that contain the relative path and file type. The descriptors are intended for use with the /tools/{id}/versions/{version_id}/{type}/descriptor/{relative_path} endpoint. Returns a zip file of all files when format&#x3D;zip is specified. # noqa: E501

    :param type: The output type of the descriptor. Examples of allowable values are \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;GALAXY\&quot;.
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;.
    :type version_id: str
    :param format: Returns a zip file of all files when format&#x3D;zip is specified.
    :type format: str

    :rtype: List[ToolFile]
    """
    return 'Not Yet Implemented'


def tools_id_versions_version_id_type_tests_get(type, id, version_id):  # noqa: E501
    """Get a list of test JSONs

    Get a list of test JSONs (these allow you to execute the tool successfully) suitable for use with this descriptor type. # noqa: E501

    :param type: The type of the underlying descriptor. Allowable values include \&quot;CWL\&quot;, \&quot;WDL\&quot;, \&quot;NFL\&quot;, \&quot;GALAXY\&quot;, \&quot;PLAIN_CWL\&quot;, \&quot;PLAIN_WDL\&quot;, \&quot;PLAIN_NFL\&quot;, \&quot;PLAIN_GALAXY\&quot;. For example, \&quot;CWL\&quot; would return an list of ToolTests objects while \&quot;PLAIN_CWL\&quot; would return a bare JSON list with the content of the tests.
    :type type: str
    :param id: A unique identifier of the tool, scoped to this registry, for example &#x60;123456&#x60;.
    :type id: str
    :param version_id: An identifier of the tool version for this particular tool registry, for example &#x60;v1&#x60;.
    :type version_id: str

    :rtype: List[FileWrapper]
    """
    return 'Not Yet Implemented'


def stats():
    """
    This method returns a list of stats for the API
    :return:
    """

    tools = MongoTool.get_all_tools()

    stats = []
    stats.append(Stat('num_tools', str(len(tools))))

    tool_versions = MongoToolVersion.get_all_tool_versions()
    stats.append(Stat('num_versions', str(len(tool_versions))))

    num_containers = 0
    num_docker = 0
    num_conda = 0
    for key in tool_versions:
        num_containers = num_containers + len(key.image_containers)
        for container in key.image_containers:
            if (container.container_type == 'DOCKER'):
                num_docker = num_docker + 1
            elif container.container_type == 'CONDA':
                num_conda = num_conda + 1
    stats.append(Stat('num_containers', str(num_containers)))
    stats.append(Stat('num_conda_containers', str(num_conda)))
    stats.append(Stat('num_docker_containers', str(num_docker)))

    return stats


def tools_get_similars(id=None):
    similar_tool = SimilarTool.get_similars_by_id(id)
    ids = []
    for similar in similar_tool.similars:
        ids.append(similar.id)

    tools = MongoTool.get_all_tools_by_id(ids)
    result_tools = []
    if tools is not None:
        for mongo_tool in tools:
            if ('anchor_tool' in mongo_tool) and (len(mongo_tool.anchor_tool) > 0):
                continue  # don't include tools that have 'anchor_tool' field
            score = 0
            for similar in similar_tool.similars:
                if similar.id == mongo_tool.id:
                    score = similar.score
            tool = transform_mongo_tool(mongo_tool)
            tool.similar_score = score
            result_tools.append(tool)
    # If the checker is provided, we filter for checker tools.
    return result_tools


def wokflows_get(name=None, description=None, author=None, license=None, type=None, container=None,
                 offset=0, limit=1000, all_fields_search=None, sort_field='name', sort_order='asc'):
    """List all workflows

       This endpoint returns all workflows available or a filtered subset using metadata query parameters.

       :param name: The name of the workflow.
       :type name: str
       :param description: The description of the workflow.
       :type description: str
       :param author: The author of the workflow
       :type author: str
       :param license: license of the workflow
       :type license: str
       :param type: type of the workflow
       :type type: str
       :param container: container used by the workflow
       :type container: str
       :param offset: Start index of paging.
       :type offset: int
       :param limit: Amount of records to return in a given page.
       :type limit: int
       :param all_fields_search: Search by all fields.
       :param sort_field: field to sort the results
       :param sort_order: sort order, asc or desc
       :rtype: List[Worflow]
       """

    is_all_field_search = False

    if all_fields_search is not None:
        name = description = author = license = type = container = all_fields_search
        is_all_field_search = True

    resp = MongoWorkflow.get_workflows(name, description, author, license, type, container,
                                       offset, limit, is_all_field_search, sort_field, sort_order)

    if resp is None:
        return None

    tools = []
    if tools is not None:
        for tool in resp.tools:
            tool = Workflow.from_dict(tool)
            tools.append(tool)

    next_page = None
    if resp.next_offset is not None:
        args_next_page = request.args.copy()
        args_next_page['offset'] = resp.next_offset
        args_next_page['limit'] = limit
        next_page = '{}?{}'.format(request.base_url, url_encode(args_next_page))

    args_last_page = request.args.copy()
    args_last_page['offset'] = resp.last_page_offset
    args_last_page['limit'] = limit
    last_page = '{}?{}'.format(request.base_url, url_encode(args_last_page))

    return tools, 200, {'next_page': next_page, 'last_page': last_page,
                        'self_link': request.url, 'current_offset': offset,
                        'current_limit': limit}


def wokflow_post():
    request_dict = request.get_json()
    mongo_workflow = MongoWorkflow()
    mongo_workflow.name = request_dict["name"]
    mongo_workflow.git_repo = request_dict["git-repo"]
    mongo_workflow.description = request_dict.get("description")
    mongo_workflow.author = request_dict.get("author")
    mongo_workflow.license = request_dict.get("license")
    mongo_workflow.type = request_dict.get("type")
    mongo_workflow.containers = request_dict.get("containers")

    try:
        mongo_workflow.save()
    except DuplicateKeyError as error:
        return "Duplicate record: name or git-repo already exists", 409
    except Exception as e:
        return str(e), 400

    try:
        InsertContainers.annotate_workflow(mongo_workflow, "/tmp/bioconda-recipes/")
    except Exception as e:
        print("Error in getting containers from : " + mongo_workflow.git_repo)
        return "Failed to retrieve containers. But, Workflow registered successfully ", 201

    return "Workflow registered successfully", 201


def tools_container_type_container_tag_get(container_type, container_tag):
    """Get the container using container_type and container_tag.

    :param container_type: container_type, for example: conda, docker, singulariry etc.,
    :type container_type: str
    :param container_tag: container_tag, for example: im-pipelines:1.0.0--pyh9f0ad1d_0
    :type container_tag: str

    :rtype: string
    """

    tool_name = container_tag.split(":")[0]
    tool_version = container_tag.split(":")[1]
    tools_list = MongoToolVersion.get_tool_version_by_name(tool_name)
    if tools_list is None:
        return None

    container_type = container_type.upper()
    for tool in tools_list:
        containers = tool.image_containers
        for container in containers:
            if container.container_type == container_type:
                if container_type == "CONDA" and container.tag == "conda:" + tool_version:
                    return container.full_tag
                if container.tag == tool_version:  # this case works for quay images
                    return container.full_tag
                try:
                    tag_replace = container.tag.replace("'", '"')
                    tag_replace = tag_replace.replace("None", "null")
                    tag_replace = tag_replace.replace("True", "true")
                    tag_replace = tag_replace.replace("False", "false")
                    tag_obj = json.loads(tag_replace)  # this case works for docker images
                    if tag_obj['name'] == tool_version:
                        return container.full_tag
                except ValueError as e:
                    continue
