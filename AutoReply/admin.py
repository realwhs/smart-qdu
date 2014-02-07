#coding:utf-8

from django.contrib import admin
from AutoReply.models import *


class KeywordInline(admin.StackedInline):
    model = Keyword
    extra = 2


class ReplyAdmin(admin.ModelAdmin):
    inlines = [KeywordInline,]
    list_display = ("reply_text","reply_type","valid",)

	
class UnrecognizedWordAdmin(admin.ModelAdmin):
    list_display = ("content", "time", "dealt")
    list_filter = ("time",)
	

class UnrecognizedWordReplyAdmin(admin.ModelAdmin):
    list_display = ("reply_text", )
	
	
admin.site.register(Reply, ReplyAdmin)
admin.site.register(UnrecognizedWord, UnrecognizedWordAdmin)
admin.site.register(UnrecognizedWordReply, UnrecognizedWordReplyAdmin)



