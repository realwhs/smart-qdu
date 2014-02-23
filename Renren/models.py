#coding:utf-8
from django.db import models


class Content(models.Model):
    content = models.CharField(max_length=130)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.create_time, self.status)
