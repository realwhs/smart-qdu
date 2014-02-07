#coding:utf-8
from django.db import models


class Statistics(models.Model):
    date = models.DateField(auto_now_add = True)
    message_received_number = models.IntegerField()
    empty_classroom_query_number = models.IntegerField()
    auto_reply_number = models.IntegerField()
    subscribe_number = models.IntegerField()
    unsubscribe_number = models.IntegerField()
    menu_click = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Statistics'

    def __unicode__(self):
        return "%s %s %s %s %s" % (self.date, self.empty_classroom_query_number,
                                       self.message_received_number, self.auto_reply_number,
                                       self.menu_click)



