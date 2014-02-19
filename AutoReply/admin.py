#coding:utf-8

from django.contrib import admin
from AutoReply.models import *


class KeywordInline(admin.StackedInline):
    model = Keyword
    extra = 2


class ReplyAdmin(admin.ModelAdmin):
    inlines = [KeywordInline,]
    list_display = ("reply_text","reply_type","valid",)


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", )


class UnrecognizedWordAdmin(admin.ModelAdmin):
    list_display = ("content", "time", "dealt")
    list_filter = ("time",)


class UnrecognizedWordReplyAdmin(admin.ModelAdmin):
    list_display = ("reply_text", )


class UserStatusAdmin(admin.ModelAdmin):
    list_display = ("weixin_id", )


admin.site.register(Reply, ReplyAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(UnrecognizedWord, UnrecognizedWordAdmin)
admin.site.register(UnrecognizedWordReply, UnrecognizedWordReplyAdmin)
admin.site.register(UserStatus, UserStatusAdmin)