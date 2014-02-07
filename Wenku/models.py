#coding:utf-8
from django.db import models


class Comment(models.Model):
    author = models.CharField(max_length=15)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return "%s %s" % (self.author, self.content)


class Paper(models.Model):
    user_name = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    simple_introduction = models.CharField(max_length=80)
    file_url = models.URLField()
    download_number = models.IntegerField()
    status = models.BooleanField(default=False)
    comment = models.ManyToManyField(Comment)

    def __unicode__(self):
        return "%s %s %s" % (self.user_name, self.time, self.title)