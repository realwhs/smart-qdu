#coding:utf-8
from django.contrib import admin
from Vote.models import VoteInfo, Option, Voter


class VoteInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", )


class OptionAdmin(admin.ModelAdmin):
    list_display = ("choice", )


class VoterAdmin(admin.ModelAdmin):
    list_display = ("weixin_id", )

admin.site.register(VoteInfo, VoteInfoAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Voter, VoterAdmin)