#coding:utf-8
from django.db import models


class Mail(models.Model):
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
    subject = models.CharField(max_length=40)
    content = models.TextField()
    #True是已经阅读了 False是还没读
    status = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s %s" % (self.from_user, self.to_user, self.subject)
