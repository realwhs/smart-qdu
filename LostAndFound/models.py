#coding:utf-8
from django.db import models

INFO_TYPE_CHOICE = ((u"lost", u"lost"), (u"found", u"found"))

ITEM_TYPE_CHOICE = ((u"书籍资料", u"书籍资料"), (u"衣物饰品", u"衣物饰品"), (u"交通工具", u"交通工具"),
      (u"随身物品", u"随身物品"), (u"电子数码", u"电子数码"), (u"卡类证件", u"卡类证件"),
      (u"其他物品", u"其他物品"), )


class Comment(models.Model):
    author = models.CharField(max_length=15)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return "%s %s" % (self.author, self.content)


class InfoDetail(models.Model):
    user_name = models.CharField(max_length=15)
    info_type = models.CharField(max_length=20, choices=INFO_TYPE_CHOICE)
    item_type = models.CharField(max_length=30, choices=ITEM_TYPE_CHOICE)
    item_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    image_url = models.URLField(blank=True, null=True)
    time = models.DateField()
    content = models.TextField()
    #联系方式
    name = models.CharField(max_length=15)
    phone = models.CharField(max_length=11)
    qq = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    #status状态  如果找到了就把status改为false
    status = models.BooleanField(default=True)
    comment = models.ManyToManyField(Comment, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s %s %s" % (self.user_name, self.info_type, self.item_type, self.item_name)


