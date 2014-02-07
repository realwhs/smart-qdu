#coding:utf-8

from django.contrib import admin
from EmptyClassroom.models import EmptyClassroom


class EmptyClassroomAdmin(admin.ModelAdmin):
    list_display = ("building_name", "room_name", "week", "day", )



admin.site.register(EmptyClassroom, EmptyClassroomAdmin)
