from django.contrib.auth.models import User, Group
from rest_framework import serializers
from configuration.models import SentinelOne


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
        fields = ['url', 'token']