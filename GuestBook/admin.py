#coding:utf-8
from django.contrib import admin
from GuestBook.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", )


admin.site.register(Message, MessageAdmin)