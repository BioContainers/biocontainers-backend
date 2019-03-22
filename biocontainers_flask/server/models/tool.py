# coding: utf-8

from __future__ import absolute_import

from typing import List  # noqa: F401

from biocontainers_flask.server import util
from biocontainers_flask.server.models.base_model_ import Model
from biocontainers_flask.server.models.tool_class import ToolClass  # noqa: F401,E501
from biocontainers_flask.server.models.tool_version import ToolVersion  # noqa: F401,E501


class Tool(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, url: str=None, id: str=None, aliases: List[str]=None, organization: str=None, toolname: str=None, toolclass: ToolClass=None, description: str=None, author: str=None, meta_version: str=None, contains: List[str]=None, has_checker: bool=None,
                 checker_url: str=None, verified: bool=None, verified_source: str=None, signed: bool=None, versions: List[ToolVersion]=None, license: str=None, similar_score: float = None, pulls : int = None):  # noqa: E501
        """Tool - a model defined in Swagger

        :param url: The url of this Tool.  # noqa: E501
        :type url: str
        :param id: The id of this Tool.  # noqa: E501
        :type id: str
        :param aliases: The aliases of this Tool.  # noqa: E501
        :type aliases: List[str]
        :param organization: The organization of this Tool.  # noqa: E501
        :type organization: str
        :param toolname: The toolname of this Tool.  # noqa: E501
        :type toolname: str
        :param toolclass: The toolclass of this Tool.  # noqa: E501
        :type toolclass: ToolClass
        :param description: The description of this Tool.  # noqa: E501
        :type description: str
        :param author: The author of this Tool.  # noqa: E501
        :type author: str
        :param meta_version: The meta_version of this Tool.  # noqa: E501
        :type meta_version: str
        :param contains: The contains of this Tool.  # noqa: E501
        :type contains: List[str]
        :param has_checker: The has_checker of this Tool.  # noqa: E501
        :type has_checker: bool
        :param checker_url: The checker_url of this Tool.  # noqa: E501
        :type checker_url: str
        :param verified: The verified of this Tool.  # noqa: E501
        :type verified: bool
        :param verified_source: The verified_source of this Tool.  # noqa: E501
        :type verified_source: str
        :param signed: The signed of this Tool.  # noqa: E501
        :type signed: bool
        :param versions: The versions of this Tool.  # noqa: E501
        :type versions: List[ToolVersion]
        """
        self.swagger_types = {
            'url': str,
            'id': str,
            'aliases': List[str],
            'organization': str,
            'toolname': str,
            'toolclass': ToolClass,
            'description': str,
            'author': str,
            'meta_version': str,
            'contains': List[str],
            'has_checker': bool,
            'checker_url': str,
            'verified': bool,
            'verified_source': str,
            'signed': bool,
            'versions': List[ToolVersion],
            'license' : str,
            'similar_score' : float,
            'pulls' : int
        }

        self.attribute_map = {
            'url': 'url',
            'id': 'id',
            'aliases': 'aliases',
            'organization': 'organization',
            'toolname': 'toolname',
            'toolclass': 'toolclass',
            'description': 'description',
            'author': 'author',
            'meta_version': 'meta_version',
            'contains': 'contains',
            'has_checker': 'has_checker',
            'checker_url': 'checker_url',
            'verified': 'verified',
            'verified_source': 'verified_source',
            'signed': 'signed',
            'versions': 'versions',
            'license':'license',
            'similar_score': 'similar_score',
            'pulls': 'pulls'
        }

        self._url = url
        self._id = id
        self._aliases = aliases
        self._organization = organization
        self._toolname = toolname
        self._toolclass = toolclass
        self._description = description
        self._author = author
        self._meta_version = meta_version
        self._contains = contains
        self._has_checker = has_checker
        self._checker_url = checker_url
        self._verified = verified
        self._verified_source = verified_source
        self._signed = signed
        self._versions = versions
        self._license = license
        self._similar_score = similar_score
        self._pulls = pulls

    @classmethod
    def from_dict(cls, dikt) -> 'Tool':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Tool of this Tool.  # noqa: E501
        :rtype: Tool
        """
        return util.deserialize_model(dikt, cls)

    @property
    def url(self) -> str:
        """Gets the url of this Tool.

        The URL for this tool in this registry  # noqa: E501

        :return: The url of this Tool.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this Tool.

        The URL for this tool in this registry  # noqa: E501

        :param url: The url of this Tool.
        :type url: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def id(self) -> str:
        """Gets the id of this Tool.

        A unique identifier of the tool, scoped to this registry  # noqa: E501

        :return: The id of this Tool.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Tool.

        A unique identifier of the tool, scoped to this registry  # noqa: E501

        :param id: The id of this Tool.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def aliases(self) -> List[str]:
        """Gets the aliases of this Tool.

        OPTIONAL A list of strings that can be used to identify this tool. This can be used to expose alternative ids (such as GUIDs) for a tool for registries. Can be used to match tools across registries.  # noqa: E501

        :return: The aliases of this Tool.
        :rtype: List[str]
        """
        return self._aliases

    @aliases.setter
    def aliases(self, aliases: List[str]):
        """Sets the aliases of this Tool.

        OPTIONAL A list of strings that can be used to identify this tool. This can be used to expose alternative ids (such as GUIDs) for a tool for registries. Can be used to match tools across registries.  # noqa: E501

        :param aliases: The aliases of this Tool.
        :type aliases: List[str]
        """

        self._aliases = aliases

    @property
    def organization(self) -> str:
        """Gets the organization of this Tool.

        The organization that published the image.  # noqa: E501

        :return: The organization of this Tool.
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization: str):
        """Sets the organization of this Tool.

        The organization that published the image.  # noqa: E501

        :param organization: The organization of this Tool.
        :type organization: str
        """
        if organization is None:
            raise ValueError("Invalid value for `organization`, must not be `None`")  # noqa: E501

        self._organization = organization

    @property
    def toolname(self) -> str:
        """Gets the toolname of this Tool.

        The name of the tool.  # noqa: E501

        :return: The toolname of this Tool.
        :rtype: str
        """
        return self._toolname

    @toolname.setter
    def toolname(self, toolname: str):
        """Sets the toolname of this Tool.

        The name of the tool.  # noqa: E501

        :param toolname: The toolname of this Tool.
        :type toolname: str
        """

        self._toolname = toolname

    @property
    def toolclass(self) -> ToolClass:
        """Gets the toolclass of this Tool.


        :return: The toolclass of this Tool.
        :rtype: ToolClass
        """
        return self._toolclass

    @toolclass.setter
    def toolclass(self, toolclass: ToolClass):
        """Sets the toolclass of this Tool.


        :param toolclass: The toolclass of this Tool.
        :type toolclass: ToolClass
        """
        if toolclass is None:
            raise ValueError("Invalid value for `toolclass`, must not be `None`")  # noqa: E501

        self._toolclass = toolclass

    @property
    def description(self) -> str:
        """Gets the description of this Tool.

        The description of the tool.  # noqa: E501

        :return: The description of this Tool.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Tool.

        The description of the tool.  # noqa: E501

        :param description: The description of this Tool.
        :type description: str
        """

        self._description = description

    @property
    def author(self) -> str:
        """Gets the author of this Tool.

        Contact information for the author of this tool entry in the registry. (More complex authorship information is handled by the descriptor)  # noqa: E501

        :return: The author of this Tool.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author: str):
        """Sets the author of this Tool.

        Contact information for the author of this tool entry in the registry. (More complex authorship information is handled by the descriptor)  # noqa: E501

        :param author: The author of this Tool.
        :type author: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def meta_version(self) -> str:
        """Gets the meta_version of this Tool.

        The version of this tool in the registry. Iterates when fields like the description, author, etc. are updated.  # noqa: E501

        :return: The meta_version of this Tool.
        :rtype: str
        """
        return self._meta_version

    @meta_version.setter
    def meta_version(self, meta_version: str):
        """Sets the meta_version of this Tool.

        The version of this tool in the registry. Iterates when fields like the description, author, etc. are updated.  # noqa: E501

        :param meta_version: The meta_version of this Tool.
        :type meta_version: str
        """

        self._meta_version = meta_version

    @property
    def contains(self) -> List[str]:
        """Gets the contains of this Tool.

        An array of IDs for the applications that are stored inside this tool  # noqa: E501

        :return: The contains of this Tool.
        :rtype: List[str]
        """
        return self._contains

    @contains.setter
    def contains(self, contains: List[str]):
        """Sets the contains of this Tool.

        An array of IDs for the applications that are stored inside this tool  # noqa: E501

        :param contains: The contains of this Tool.
        :type contains: List[str]
        """

        self._contains = contains

    @property
    def has_checker(self) -> bool:
        """Gets the has_checker of this Tool.

        Whether this tool has a checker tool associated with it  # noqa: E501

        :return: The has_checker of this Tool.
        :rtype: bool
        """
        return self._has_checker

    @has_checker.setter
    def has_checker(self, has_checker: bool):
        """Sets the has_checker of this Tool.

        Whether this tool has a checker tool associated with it  # noqa: E501

        :param has_checker: The has_checker of this Tool.
        :type has_checker: bool
        """

        self._has_checker = has_checker

    @property
    def checker_url(self) -> str:
        """Gets the checker_url of this Tool.

        Optional url to the checker tool that will exit successfully if this tool produced the expected result given test data.  # noqa: E501

        :return: The checker_url of this Tool.
        :rtype: str
        """
        return self._checker_url

    @checker_url.setter
    def checker_url(self, checker_url: str):
        """Sets the checker_url of this Tool.

        Optional url to the checker tool that will exit successfully if this tool produced the expected result given test data.  # noqa: E501

        :param checker_url: The checker_url of this Tool.
        :type checker_url: str
        """

        self._checker_url = checker_url

    @property
    def verified(self) -> bool:
        """Gets the verified of this Tool.

        Reports whether this tool has been verified by a specific organization or individual  # noqa: E501

        :return: The verified of this Tool.
        :rtype: bool
        """
        return self._verified

    @verified.setter
    def verified(self, verified: bool):
        """Sets the verified of this Tool.

        Reports whether this tool has been verified by a specific organization or individual  # noqa: E501

        :param verified: The verified of this Tool.
        :type verified: bool
        """

        self._verified = verified

    @property
    def verified_source(self) -> str:
        """Gets the verified_source of this Tool.

        Source of metadata that can support a verified tool, such as an email or URL  # noqa: E501

        :return: The verified_source of this Tool.
        :rtype: str
        """
        return self._verified_source

    @verified_source.setter
    def verified_source(self, verified_source: str):
        """Sets the verified_source of this Tool.

        Source of metadata that can support a verified tool, such as an email or URL  # noqa: E501

        :param verified_source: The verified_source of this Tool.
        :type verified_source: str
        """

        self._verified_source = verified_source

    @property
    def signed(self) -> bool:
        """Gets the signed of this Tool.

        Reports whether this tool has been signed.  # noqa: E501

        :return: The signed of this Tool.
        :rtype: bool
        """
        return self._signed

    @signed.setter
    def signed(self, signed: bool):
        """Sets the signed of this Tool.

        Reports whether this tool has been signed.  # noqa: E501

        :param signed: The signed of this Tool.
        :type signed: bool
        """

        self._signed = signed

    @property
    def versions(self) -> List[ToolVersion]:
        """Gets the versions of this Tool.

        A list of versions for this tool  # noqa: E501

        :return: The versions of this Tool.
        :rtype: List[ToolVersion]
        """
        return self._versions

    @versions.setter
    def versions(self, versions: List[ToolVersion]):
        """Sets the versions of this Tool.

        A list of versions for this tool  # noqa: E501

        :param versions: The versions of this Tool.
        :type versions: List[ToolVersion]
        """
        if versions is None:
            raise ValueError("Invalid value for `versions`, must not be `None`")  # noqa: E501

        self._versions = versions

    @property
    def license(self) -> str:
        """Gets the versions of this Tool.

        A list of versions for this tool  # noqa: E501

        :return: The versions of this Tool.
        :rtype: List[ToolVersion]
        """
        return self._license

    @license.setter
    def license(self, license: str):
        self._license = license

    @property
    def similar_score(self) -> float:
        return self._similar_score

    @similar_score.setter
    def similar_score(self, similar_score: float):
        self._similar_score = similar_score

    @property
    def pulls(self) -> int:
        return self._pulls

    @pulls.setter
    def pulls(self, pulls: int):
        self._pulls = pulls