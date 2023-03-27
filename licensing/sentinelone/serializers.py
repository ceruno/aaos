from .requests import Export
from rest_framework import serializers


class ExportSerializer(serializers.Serializer):
    item = serializers.CharField(max_length=200)
    target = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Export(**validated_data)
