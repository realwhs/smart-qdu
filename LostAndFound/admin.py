#coding:utf-8
from django.contrib import admin
from LostAndFound.models import InfoDetail, Comment


class InfoDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "info_type", "item_type", "item_name", "user_name", "time", "status")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content",)


admin.site.register(InfoDetail, InfoDetailAdmin)
admin.site.register(Comment, CommentAdmin)

