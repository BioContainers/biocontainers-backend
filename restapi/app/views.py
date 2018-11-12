from __future__ import unicode_literals

from django.template.response import TemplateResponse

from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet

from app.serializers import *
from app.models import Tool, ToolVersion


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


class ToolViewSet(MongoModelViewSet):
    """
    Contains information about inputs/outputs of a single program
    that may be used in Universe workflows.
    """
    lookup_field = 'id'
    serializer_class = ToolSerializer

    def get_queryset(self):
        return Tool.objects.all()


class ToolVersionViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = ToolVersionSerializer

    def get_queryset(self):
        return ToolVersion.objects.all()



