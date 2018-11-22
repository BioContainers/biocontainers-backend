from pymodm_rest import viewsets
from rest_framework import serializers

from biocontainers.common.models import MongoTool, MongoToolVersion


class ToolSerializer(viewsets.ModelViewSet):
    id = serializers.CharField(read_only=False)

    class Meta:
        model = MongoTool
        fields = '__all__'


class ToolVersionSerializer(viewsets.ModelViewSet):
    id = serializers.CharField(read_only=False)

    class Meta:
        model = MongoToolVersion
        fields = '__all__'
