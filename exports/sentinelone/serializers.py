from .requests import Export
from rest_framework import serializers

class ExportSerializer(serializers.Serializer):
    item = serializers.CharField(max_length=200)
    index = serializers.CharField(max_length=200)
    pipeline = serializers.CharField(max_length=200)
    limit = serializers.CharField(max_length=200)
    timedelta = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Export(**validated_data)