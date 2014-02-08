#coding:utf-8
from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.name, self.title)
