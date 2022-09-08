from encodings import utf_8
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from configuration.models import SentinelOne, Elastic, FreshService
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class SentinelOneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SentinelOne
        fields = ['url', 'console_url', 'token']

    def create(self, validated_data):
        validated_data['token'] = (f.encrypt(bytes(validated_data['token'], 'utf-8'))).decode()
        return SentinelOne.objects.create(**validated_data)

    # def to_representation(self, instance):
    #     return {
    #         'console_url': instance.console_url,
    #         'token': f.decrypt(instance.token)
    #     }

class ElasticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Elastic
        fields = ['url', 'elastic_url', 'user', 'password']

    def create(self, validated_data):
        validated_data['password'] = f.encrypt(bytes(validated_data['password'], 'utf-8'))
        return Elastic.objects.create(**validated_data)

class FreshServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FreshService
        fields = ['url', 'service_url', 'api_key', 'group_id', 'requester_id', 'requester_email', 'requester_phone', 'ansprechperson']

    def create(self, validated_data):
        validated_data['api_key'] = f.encrypt(bytes(validated_data['api_key'], 'utf-8'))
        return SentinelOne.objects.create(**validated_data)