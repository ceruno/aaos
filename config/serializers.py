from encodings import utf_8
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from config.models import (
    SentinelOneModel,
    ElasticModel,
    FreshServiceModel,
    BexioModel,
    SharePointModel,
)
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), "utf-8")
f = Fernet(key)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class SentinelOneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SentinelOneModel
        fields = ["url", "sentinelone_url", "token"]

    def create(self, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        return SentinelOneModel.objects.create(**validated_data)

    # def to_representation(self, instance):
    #     return {
    #         'sentinelone_url': instance.sentinelone_url,
    #         'token': f.decrypt(instance.token)
    #     }


class ElasticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ElasticModel
        fields = ["url", "elastic_cloud_id", "elastic_url", "tls_fingerprint", "user", "password"]

    def create(self, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        return ElasticModel.objects.create(**validated_data)


class FreshServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FreshServiceModel
        fields = [
            "url",
            "fresh_url",
            "api_key",
            "group_id",
            "requester_id",
            "requester_email",
            "requester_phone",
            "ansprechperson",
        ]

    def create(self, validated_data):
        validated_data["api_key"] = (
            f.encrypt(bytes(validated_data["api_key"], "utf-8"))
        ).decode()
        return FreshServiceModel.objects.create(**validated_data)


class BexioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BexioModel
        fields = ["url", "bexio_url", "api_key"]

    def create(self, validated_data):
        validated_data["api_key"] = (
            f.encrypt(bytes(validated_data["api_key"], "utf-8"))
        ).decode()
        return BexioModel.objects.create(**validated_data)


class SharePointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SharePointModel
        fields = ["url", "sharepoint_url", "sharepoint_site", "user", "password"]

    def create(self, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        return SharePointModel.objects.create(**validated_data)


class CrontabScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = "__all__"


class IntervalScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"


class PeriodicTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = "__all__"
