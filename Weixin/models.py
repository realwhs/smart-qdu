#coding:utf-8
from django.db import models


class BindJwInfo(models.Model):
    weixin_id = models.CharField(max_length=30)
    jw_account = models.CharField(max_length=100)
    jw_password = models.CharField(max_length=100)
