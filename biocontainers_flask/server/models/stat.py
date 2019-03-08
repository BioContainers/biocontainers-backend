
from __future__ import absolute_import

from biocontainers_flask.server import util
from biocontainers_flask.server.models.base_model_ import Model


class Stat(Model):

    def __init__(self, name: str=None, value: str=None):

        self.swagger_types = {
            'name': str,
            'value': str
        }

        self.attribute_map = {
            'name': 'name',
            'value': 'value'
        }

        self._name = name
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Stat':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Tool of this Tool.  # noqa: E501
        :rtype: Tool
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def url(self, name: str):
        self._name = name

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value
