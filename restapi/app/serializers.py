from app.models import Tool, ToolVersion
from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers


class ToolSerializer(mongoserializers.DocumentSerializer):
    id = serializers.CharField(read_only=False)

    class Meta:
        model = Tool
        fields = '__all__'


class ToolVersionSerializer(mongoserializers.DocumentSerializer):
    id = serializers.CharField(read_only=False)

    class Meta:
        model = ToolVersion
        fields = '__all__'
