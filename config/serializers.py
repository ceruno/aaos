from encodings import utf_8
from django.contrib.auth.models import User, Group
import pytz
from rest_framework import serializers
from config.models import (
    SentinelOneModel,
    ElasticModel,
    FreshServiceModel,
    BexioModel,
    SharePointModel,
    LokiModel,
    DataSetModel,
    PostgresModel,
    JiraModel,
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

    def update(self, instance, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        instance.token = validated_data["token"]
        instance.save()
        return instance

    # def to_representation(self, instance):
    #     return {
    #         'sentinelone_url': instance.sentinelone_url,
    #         'token': f.decrypt(instance.token)
    #     }


class ElasticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ElasticModel
        fields = [
            "url",
            "elastic_cloud_id",
            "elastic_url",
            "tls_fingerprint",
            "user",
            "password",
        ]

    def create(self, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        return ElasticModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        instance.password = validated_data["password"]
        instance.save()
        return instance


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

    def update(self, instance, validated_data):
        validated_data["api_key"] = (
            f.encrypt(bytes(validated_data["api_key"], "utf-8"))
        ).decode()
        instance.api_key = validated_data["api_key"]
        instance.save()
        return instance


class BexioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BexioModel
        fields = ["url", "bexio_url", "api_key"]

    def create(self, validated_data):
        validated_data["api_key"] = (
            f.encrypt(bytes(validated_data["api_key"], "utf-8"))
        ).decode()
        return BexioModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["api_key"] = (
            f.encrypt(bytes(validated_data["api_key"], "utf-8"))
        ).decode()
        instance.api_key = validated_data["api_key"]
        instance.save()
        return instance


class SharePointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SharePointModel
        fields = ["url", "sharepoint_url", "sharepoint_site", "user", "password"]

    def create(self, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        return SharePointModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        instance.password = validated_data["password"]
        instance.save()
        return instance


class LokiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LokiModel
        fields = ["url", "loki_url", "user", "token"]

    def create(self, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        return LokiModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        instance.token = validated_data["token"]
        instance.save()
        return instance


class DataSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSetModel
        fields = ["url", "dataset_url", "token"]

    def create(self, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        return DataSetModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        instance.token = validated_data["token"]
        instance.save()
        return instance


class PostgresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostgresModel
        fields = [
            "url",
            "host",
            "port",
            "db",
            "user",
            "password",
        ]

    def create(self, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        return PostgresModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["password"] = (
            f.encrypt(bytes(validated_data["password"], "utf-8"))
        ).decode()
        instance.password = validated_data["password"]
        instance.save()
        return instance


class JiraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JiraModel
        fields = ["url", "jira_url", "user", "token"]

    def create(self, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        return JiraModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["token"] = (
            f.encrypt(bytes(validated_data["token"], "utf-8"))
        ).decode()
        instance.token = validated_data["token"]
        instance.save()
        return instance


class CrontabScheduleSerializer(serializers.HyperlinkedModelSerializer):
    timezone = serializers.ChoiceField(choices=pytz.all_timezones)

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
