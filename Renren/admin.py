#coding:utf-8
from django.contrib import admin
from Renren.models import Content


class ContentAdmin(admin.ModelAdmin):
    list_dislay = ("create_time", "status")


admin.site.register(Content, ContentAdmin)