#coding:utf-8
from django.db import models


class SignStatus(models.Model):
    tieba_name = models.CharField(max_length=30)
    status = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.tieba_name, self.status)


class TiebaAccount(models.Model):
    user_name = models.CharField(max_length=30)
    tieba_user_name = models.CharField(max_length=30)
    tieba_password = models.CharField(max_length=30)
    last_task_time = models.DateTimeField(auto_now=True)
    task_status = models.BooleanField()
    sign_status = models.ManyToManyField(SignStatus, blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.user_name, self.tieba_user_name, self.task_status, self.last_task_time)
