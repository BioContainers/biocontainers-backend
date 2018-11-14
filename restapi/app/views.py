from __future__ import unicode_literals

from app.models import Tool, ToolVersion
from app.serializers import *
from django.template.response import TemplateResponse
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


class ToolViewSet(MongoModelViewSet):
    """
    retrieve: Return an specific Tool by Identifier id
    list: Retrieve all the tools in the registry.
    """
    lookup_field = 'id'
    serializer_class = ToolSerializer

    http_method_names = ['list', 'get', 'head']

    def get_queryset(self):
        return Tool.objects.all()


class ToolVersionViewSet(MongoModelViewSet):
    """
        retrieve: Return an specific Tool Version by Identifier id
        list: Retrieve all the tool Versions in the registry.
        """
    lookup_field = 'id'

    serializer_class = ToolVersionSerializer
    http_method_names = ['list', 'get', 'head']

    def get_queryset(self):
        return ToolVersion.objects.all()
