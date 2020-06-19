# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from biocontainers_flask.server.models.base_model_ import Model
from biocontainers_flask.server.models.checksum import Checksum  # noqa: F401,E501
from biocontainers_flask.server.models.image_type import ImageType  # noqa: F401,E501
from biocontainers_flask.server import util


class ImageData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, registry_host: str=None, image_name: str=None, size: int=None, updated: str=None, checksum: List[Checksum]=None, image_type: ImageType=None):  # noqa: E501
        """ImageData - a model defined in Swagger

        :param registry_host: The registry_host of this ImageData.  # noqa: E501
        :type registry_host: str
        :param image_name: The image_name of this ImageData.  # noqa: E501
        :type image_name: str
        :param size: The size of this ImageData.  # noqa: E501
        :type size: int
        :param updated: The updated of this ImageData.  # noqa: E501
        :type updated: str
        :param checksum: The checksum of this ImageData.  # noqa: E501
        :type checksum: List[Checksum]
        :param image_type: The image_type of this ImageData.  # noqa: E501
        :type image_type: ImageType
        """
        self.swagger_types = {
            'registry_host': str,
            'image_name': str,
            'size': int,
            'updated': str,
            'checksum': List[Checksum],
            'image_type': ImageType,
            'downloads': int
        }

        self.attribute_map = {
            'registry_host': 'registry_host',
            'image_name': 'image_name',
            'size': 'size',
            'updated': 'updated',
            'checksum': 'checksum',
            'image_type': 'image_type',
            'downloads': 'downloads'
        }
        self._registry_host = registry_host
        self._image_name = image_name
        self._size = size
        self._updated = updated
        self._checksum = checksum
        self._image_type = image_type

    @classmethod
    def from_dict(cls, dikt) -> 'ImageData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ImageData of this ImageData.  # noqa: E501
        :rtype: ImageData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def registry_host(self) -> str:
        """Gets the registry_host of this ImageData.

        A docker registry or a URL to a Singularity registry. Used along with image_name to locate a specific image.  # noqa: E501

        :return: The registry_host of this ImageData.
        :rtype: str
        """
        return self._registry_host

    @registry_host.setter
    def registry_host(self, registry_host: str):
        """Sets the registry_host of this ImageData.

        A docker registry or a URL to a Singularity registry. Used along with image_name to locate a specific image.  # noqa: E501

        :param registry_host: The registry_host of this ImageData.
        :type registry_host: str
        """

        self._registry_host = registry_host

    @property
    def image_name(self) -> str:
        """Gets the image_name of this ImageData.

        Used in conjunction with a registry_url if provided to locate images.  # noqa: E501

        :return: The image_name of this ImageData.
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name: str):
        """Sets the image_name of this ImageData.

        Used in conjunction with a registry_url if provided to locate images.  # noqa: E501

        :param image_name: The image_name of this ImageData.
        :type image_name: str
        """

        self._image_name = image_name

    @property
    def size(self) -> int:
        """Gets the size of this ImageData.

        Size of the container in bytes.  # noqa: E501

        :return: The size of this ImageData.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size: int):
        """Sets the size of this ImageData.

        Size of the container in bytes.  # noqa: E501

        :param size: The size of this ImageData.
        :type size: int
        """

        self._size = size

    @property
    def updated(self) -> str:
        """Gets the updated of this ImageData.

        Last time the container was updated.  # noqa: E501

        :return: The updated of this ImageData.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated: str):
        """Sets the updated of this ImageData.

        Last time the container was updated.  # noqa: E501

        :param updated: The updated of this ImageData.
        :type updated: str
        """

        self._updated = updated

    @property
    def checksum(self) -> List[Checksum]:
        """Gets the checksum of this ImageData.

        A production (immutable) tool version is required to have a hashcode. Not required otherwise, but might be useful to detect changes.  This exposes the hashcode for specific image versions to verify that the container version pulled is actually the version that was indexed by the registry.  # noqa: E501

        :return: The checksum of this ImageData.
        :rtype: List[Checksum]
        """
        return self._checksum

    @checksum.setter
    def checksum(self, checksum: List[Checksum]):
        """Sets the checksum of this ImageData.

        A production (immutable) tool version is required to have a hashcode. Not required otherwise, but might be useful to detect changes.  This exposes the hashcode for specific image versions to verify that the container version pulled is actually the version that was indexed by the registry.  # noqa: E501

        :param checksum: The checksum of this ImageData.
        :type checksum: List[Checksum]
        """

        self._checksum = checksum

    @property
    def image_type(self) -> ImageType:
        """Gets the image_type of this ImageData.


        :return: The image_type of this ImageData.
        :rtype: ImageType
        """
        return self._image_type

    @image_type.setter
    def image_type(self, image_type: ImageType):
        """Sets the image_type of this ImageData.


        :param image_type: The image_type of this ImageData.
        :type image_type: ImageType
        """

        self._image_type = image_type

    @property
    def downloads(self) -> str:
        """Gets the updated of this ImageData.

        Last time the container was updated.  # noqa: E501

        :return: The updated of this ImageData.
        :rtype: str
        """
        return self._downloads

    @downloads.setter
    def downloads(self, downloads: str):
        """Sets the updated of this ImageData.

        Last time the container was updated.  # noqa: E501

        :param updated: The updated of this ImageData.
        :type updated: str
        """

        self._downloads = downloads