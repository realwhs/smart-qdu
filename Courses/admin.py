#coding:utf-8
from django.contrib import admin
from Courses.models import CourseInfo, Comment


class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "content", )


admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(Comment, CommentAdmin)