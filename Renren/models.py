#coding:utf-8
from django.db import models


class RenrenOauth(models.Model):
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)