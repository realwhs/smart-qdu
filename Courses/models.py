#coding:utf-8
from django.db import models


class Comment(models.Model):
    user_name = models.CharField(max_length=30)
    is_anonymous = models.BooleanField(default=False)
    score = models.SmallIntegerField()
    #homework = models.TextField(blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    at_top = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s" % (self.user_name, self.content)


class CourseInfo(models.Model):
    name = models.CharField(max_length=30)
    course_id = models.CharField(max_length=30)
    teacher_name = models.CharField(max_length=10)
    day = models.SmallIntegerField()
    term = models.CharField(max_length=10)
    campus = models.CharField(max_length=20)
    classroom = models.CharField(max_length=20)
    comment = models.ManyToManyField(Comment, blank=True)
    #状态       如果是现在正在上的课  就True  如果是以前学期的课  就是False
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s %s %s %s" % (self.name, self.teacher_name, self.campus, self.day, self.classroom)
