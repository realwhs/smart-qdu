#coding:utf-8

from django.contrib import admin
from Statistics.models import *

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ("date", "message_received_number","empty_classroom_query_number", "auto_reply_number",\
                    "subscribe_number", "unsubscribe_number",)
    list_filter = ("date",)

admin.site.register(Statistics, StatisticsAdmin)
