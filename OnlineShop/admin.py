#coding:utf-8
from django.contrib import admin
from OnlineShop.models import ItemInfo, Order, AddressInfo


class ItemInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "number", "status", )


class AddressInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "address", "email")


admin.site.register(ItemInfo, ItemInfoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(AddressInfo, AddressInfoAdmin)