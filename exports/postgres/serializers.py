from .requests import Export
from rest_framework import serializers


class ExportSerializer(serializers.Serializer):
    item = serializers.CharField(max_length=200)
    query = serializers.CharField(max_length=1000)
    index = serializers.CharField(max_length=200)
    pipeline = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Export(**validated_data)
