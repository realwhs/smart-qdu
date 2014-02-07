#coding:utf-8
from django.db import models
"""
关于这个的数据库模型设计我就不想说太多了，太乱了。以前使用的是比较原始的方法，每一节课的状态都是一个字段，导致的就是
查询语句重复麻烦，一大坨。现在改成这样的了，明显的就是数据库成了以前的10倍大，没用的数据太多了。但是查询语句什么的很好写。
算了，就这样吧，，，到时候看看性能再说吧，现在也懒得测试了
"""

"""
class ClassroomStatus(models.Model):
    class_order = models.IntegerField()
    status = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.class_order, self.status)


class EmptyClassroom(models.Model):
    building_name = models.CharField(max_length=20)
    room_name = models.CharField(max_length=30)
    week = models.IntegerField()
    day = models.IntegerField()
    classroom_status = models.ManyToManyField(ClassroomStatus)

    def __unicode__(self):
        return "%s %s %s %s %s " % (self.building_name, self.room_name, self.week, self.day, self.classroom_status)

"""


#Update at 20140205
class EmptyClassroom(models.Model):
    building_name = models.CharField(max_length=20)
    room_name = models.CharField(max_length=30)
    week = models.IntegerField()
    day = models.IntegerField()
    #参见  http://www.cnblogs.com/virusdefender/p/3538513.html
    classroom_status = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s %s %s %s %s " % (self.building_name, self.room_name, self.week, self.day, self.classroom_status)




