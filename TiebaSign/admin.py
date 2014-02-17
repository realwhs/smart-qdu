#coding:utf-8
from TiebaSign.models import TiebaAccount, SignStatus
from django.contrib import admin


class TiebaAccountAdmin(admin.ModelAdmin):
    list_display = ("user_name", "tieba_user_name", )


class SignStatusAdmin(admin.ModelAdmin):
    list_display = ("status", "tieba_name", )


admin.site.register(TiebaAccount, TiebaAccountAdmin)
admin.site.register(SignStatus, SignStatusAdmin)