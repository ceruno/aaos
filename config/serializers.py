from encodings import utf_8
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from config.models import SentinelOneModel, ElasticModel, FreshServiceModel
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
        model = SentinelOneModel
        fields = ['url', 'console_url', 'token']

    def create(self, validated_data):
        validated_data['token'] = (f.encrypt(bytes(validated_data['token'], 'utf-8'))).decode()
        return SentinelOneModel.objects.create(**validated_data)

    # def to_representation(self, instance):
    #     return {
    #         'console_url': instance.console_url,
    #         'token': f.decrypt(instance.token)
    #     }

class ElasticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ElasticModel
        fields = ['url', 'elastic_url', 'user', 'password']

    def create(self, validated_data):
        validated_data['password'] = (f.encrypt(bytes(validated_data['password'], 'utf-8'))).decode()
        return ElasticModel.objects.create(**validated_data)

class FreshServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FreshServiceModel
        fields = ['url', 'service_url', 'api_key', 'group_id', 'requester_id', 'requester_email', 'requester_phone', 'ansprechperson']

    def create(self, validated_data):
        validated_data['api_key'] = (f.encrypt(bytes(validated_data['api_key'], 'utf-8'))).decode()
        return SentinelOneModel.objects.create(**validated_data)