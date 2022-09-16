from django.db import models

class SentinelOneModel(models.Model):
    console_url = models.URLField()
    token = models.TextField()

class ElasticModel(models.Model):
    elastic_url = models.URLField()
    user = models.CharField(max_length=200)
    password = models.TextField()

class FreshServiceModel(models.Model):
    service_url = models.URLField()
    api_key = models.TextField()
    group_id = models.BigIntegerField()
    requester_id = models.BigIntegerField()
    requester_email = models.EmailField()
    requester_phone = models.CharField(max_length=200)
    ansprechperson = models.CharField(max_length=200)

class BexioModel(models.Model):
    bexio_url = models.URLField()
    api_key = models.TextField()

class SharePointModel(models.Model):
    sharepoint_url = models.URLField()
    sharepoint_site = models.URLField()
    user = models.CharField(max_length=200)
    password = models.TextField()