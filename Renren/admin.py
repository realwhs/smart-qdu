#coding:utf-8
from django.contrib import admin
from Renren.models import RenrenOauth

class RenrenOauthAdmin(admin.ModelAdmin):
    list_display = ("access_token", "date")


admin.site.register(RenrenOauth, RenrenOauthAdmin)