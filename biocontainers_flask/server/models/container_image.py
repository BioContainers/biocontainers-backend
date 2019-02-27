
from __future__ import absolute_import

from typing import List  # noqa: F401

from biocontainers_flask.server import util
from biocontainers_flask.server.models.base_model_ import Model

class ContainerImage(Model):

    def __init__(self, full_tag: str = None, container_type: str = None, recipe_url: str = None, size: str = None,
                 downloads: str = None, last_updated: str = None):

        self.swagger_types = {
            'full_tag': str,
            'container_type': str,
            'recipe_url': str,
            'size': str,
            'downloads': str,
            'last_updated': str
        }

        self.attribute_map = {
            'full_tag': 'full_tag',
            'container_type': 'container_type',
            'recipe_url': 'recipe_url',
            'registry_url': 'registry_url',
            'size': 'size',
            'downloads': 'downloads',
            'last_updated': 'last_updated'
        }

        self._full_tag = full_tag
        self._container_type = container_type
        self._recipe_url = recipe_url
        self._size = size
        self._downloads = downloads
        self._last_updated = last_updated

    @classmethod
    def from_dict(cls, dikt) -> 'ContainerImage':
        return util.deserialize_model(dikt, cls)

    @property
    def full_tag(self) -> str:
        return self._full_tag

    @full_tag.setter
    def full_tag(self, full_tag: str):
        self._full_tag = full_tag

    @property
    def container_type(self) -> str:
        return self._container_type

    @container_type.setter
    def container_type(self, container_type: str):
        self._container_type = container_type

    @property
    def recipe_url(self) -> str:
        return self._recipe_url

    @recipe_url.setter
    def recipe_url(self, recipe_url: str):
        self._recipe_url = recipe_url

    @property
    def registry_url(self) -> str:
        return self._registry_url

    @registry_url.setter
    def registry_url(self, registry_url: str):
        self._registry_url = registry_url

    @property
    def size(self) -> str:
        return self._size

    @size.setter
    def size(self, size: str):
        self._size = size

    @property
    def downloads(self) -> str:
        return self._downloads

    @downloads.setter
    def downloads(self, downloads):
        self._downloads = downloads

    @property
    def last_updated(self) -> str:
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated: str):
        self._last_updated = last_updated


