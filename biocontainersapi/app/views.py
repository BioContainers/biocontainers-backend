from __future__ import unicode_literals

from django.template.response import TemplateResponse
from pymodm_rest import viewsets

from biocontainers.common.models import MongoTool, MongoToolVersion
from biocontainersapi.app.serializers import ToolSerializer, ToolVersionSerializer


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


class ToolViewSet(viewsets.ModelViewSet):
    """
    retrieve: Return an specific Tool by Identifier id
    list: Retrieve all the tools in the registry.
    """
    lookup_field = 'id'
    serializer_class = ToolSerializer

    http_method_names = ['list', 'get', 'head']

    def get_queryset(self):
        return MongoTool.get_all_tools()


class ToolVersionViewSet(viewsets.ModelViewSet):
    """
        retrieve: Return an specific Tool Version by Identifier id
        list: Retrieve all the tool Versions in the registry.
        """
    lookup_field = 'id'

    serializer_class = ToolVersionSerializer
    http_method_names = ['list', 'get', 'head']

    def get_queryset(self):
        return MongoToolVersion.get_all_tool_versions()
