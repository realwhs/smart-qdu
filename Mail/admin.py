#coding:utf-8
from django.contrib import admin
from Mail.models import  Mail


class MailAdmin(admin.ModelAdmin):
    list_display = ("to_user", "from_user", "subject", "status")


admin.site.register(Mail, MailAdmin)