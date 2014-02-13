#coding:utf-8
from django.contrib import admin
from OnlineShop.models import ItemInfo, Order


class ItemInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "number", "status", )


admin.site.register(ItemInfo, ItemInfoAdmin)
admin.site.register(Order, OrderAdmin)