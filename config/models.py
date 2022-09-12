from django.db import models

class SentinelOneModel(models.Model):
    console_url = models.URLField()
    token = models.CharField(max_length=400)

class ElasticModel(models.Model):
    elastic_url = models.URLField()
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class FreshServiceModel(models.Model):
    service_url = models.URLField()
    api_key = models.CharField(max_length=200)
    group_id = models.IntegerField()
    requester_id = models.IntegerField()
    requester_email = models.EmailField()
    requester_phone = models.CharField(max_length=200)
    ansprechperson = models.CharField(max_length=200)