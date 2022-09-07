from django.db import models

class SentinelOne(models.Model):
    url = models.CharField(max_length=200)
    token = models.CharField(max_length=200)

class Elastic(models.Model):
    url = models.URLField
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class FreshService(models.Model):
    url = models.URLField
    api_key = models.CharField(max_length=200)
    group_id = models.IntegerField
    requester_id = models.IntegerField
    requester_email = models.EmailField
    requester_phone = models.CharField(max_length=200)
    ansprechperson = models.CharField(max_length=200)