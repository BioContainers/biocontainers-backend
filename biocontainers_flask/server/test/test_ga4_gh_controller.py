# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from biocontainers_flask_server.models.error import Error  # noqa: E501
from biocontainers_flask_server.models.file_wrapper import FileWrapper  # noqa: E501
from biocontainers_flask_server.models.metadata import Metadata  # noqa: E501
from biocontainers_flask_server.models.tool import Tool  # noqa: E501
from biocontainers_flask_server.models.tool_class import ToolClass  # noqa: E501
from biocontainers_flask_server.models.tool_file import ToolFile  # noqa: E501
from biocontainers_flask_server.models.tool_version import ToolVersion  # noqa: E501
from biocontainers_flask_server.test import BaseTestCase


class TestGA4GHController(BaseTestCase):
    """GA4GHController integration test stubs"""

    def test_metadata_get(self):
        """Test case for metadata_get

        Return some metadata that is useful for describing this registry
        """
        response = self.client.open(
            '/api/ga4gh/v2/metadata',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tool_classes_get(self):
        """Test case for tool_classes_get

        List all tool types
        """
        response = self.client.open(
            '/api/ga4gh/v2/toolClasses',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_get(self):
        """Test case for tools_get

        List all tools
        """
        query_string = [('id', 'id_example'),
                        ('alias', 'alias_example'),
                        ('registry', 'registry_example'),
                        ('organization', 'organization_example'),
                        ('name', 'name_example'),
                        ('toolname', 'toolname_example'),
                        ('description', 'description_example'),
                        ('author', 'author_example'),
                        ('checker', true),
                        ('offset', 'offset_example'),
                        ('limit', 1000)]
        response = self.client.open(
            '/api/ga4gh/v2/tools',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_get(self):
        """Test case for tools_id_get

        List one specific tool, acts as an anchor for self references
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_get(self):
        """Test case for tools_id_versions_get

        List versions of a tool
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_version_id_containerfile_get(self):
        """Test case for tools_id_versions_version_id_containerfile_get

        Get the container specification(s) for the specified image.
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions/{version_id}/containerfile'.format(id='id_example', version_id='version_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_version_id_get(self):
        """Test case for tools_id_versions_version_id_get

        List one specific tool version, acts as an anchor for self references
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions/{version_id}'.format(id='id_example', version_id='version_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_version_id_type_descriptor_get(self):
        """Test case for tools_id_versions_version_id_type_descriptor_get

        Get the tool descriptor for the specified tool
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions/{version_id}/{type}/descriptor'.format(type='type_example', id='id_example', version_id='version_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_version_id_type_descriptor_relative_path_get(self):
        """Test case for tools_id_versions_version_id_type_descriptor_relative_path_get

        Get additional tool descriptor files relative to the main file
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions/{version_id}/{type}/descriptor/{relative_path}'.format(type='type_example', id='id_example', version_id='version_id_example', relative_path='relative_path_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_version_id_type_files_get(self):
        """Test case for tools_id_versions_version_id_type_files_get

        Get a list of objects that contain the relative path and file type
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions/{version_id}/{type}/files'.format(type='type_example', id='id_example', version_id='version_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tools_id_versions_version_id_type_tests_get(self):
        """Test case for tools_id_versions_version_id_type_tests_get

        Get a list of test JSONs
        """
        response = self.client.open(
            '/api/ga4gh/v2/tools/{id}/versions/{version_id}/{type}/tests'.format(type='type_example', id='id_example', version_id='version_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
