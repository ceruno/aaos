from django.db import models


class SentinelOneModel(models.Model):
    sentinelone_url = models.URLField()
    token = models.TextField()


class ElasticModel(models.Model):
    elastic_cloud_id = models.CharField(max_length=200, blank=True)
    elastic_url = models.URLField(blank=True)
    tls_fingerprint = models.CharField(max_length=200, blank=True)
    user = models.CharField(max_length=200)
    password = models.TextField()


class FreshServiceModel(models.Model):
    fresh_url = models.URLField()
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


class LokiModel(models.Model):
    loki_url = models.URLField()
    user = models.CharField(max_length=200)
    token = models.TextField()


class DataSetModel(models.Model):
    dataset_url = models.URLField()
    token = models.TextField()


class PostgresModel(models.Model):
    host = models.CharField(max_length=200)
    port = models.BigIntegerField()
    db = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    password = models.TextField()
