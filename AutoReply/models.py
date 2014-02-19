#coding:utf-8
from django.db import models


#用于图文回复的
class News(models.Model):
    title = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    #图片链接，支持JPG、PNG格式，较好的效果为大图360*200，小图200*200
    pic_url = models.URLField(blank=True)
    #点击图文消息跳转链接
    url = models.URLField(blank=True)

    def __unicode__(self):
        return "%s" % (self.title, )


class Reply(models.Model):
    valid = models.BooleanField("有效？", default=True)
    reply_type_choice = (("text", "text"), ("news", "news"), ("music", "music"), ("action", "action"), )
    reply_type = models.CharField("回复类型", max_length=10, choices=reply_type_choice)
    ########################
    #reply_text用于纯文本回复
    reply_text = models.TextField(blank=True)
    ########################
    #下面的用于图文回复
    news_reply = models.ManyToManyField(News, blank=True)
    ########################
    #下面是回复音乐
    music_title = models.CharField(max_length=30, blank=True)
    music_description = models.CharField(max_length=40, blank=True)
    music_url = models.URLField(blank=True)
    music_hq_url = models.URLField(blank=True)
    ########################
    #下面是使用action回复的
    action = models.CharField(max_length=30, blank=True)
    parameter = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return "%s" % (self.reply_type, )


class Keyword(models.Model):
    keyword_text = models.CharField(max_length=20)
    reply = models.ForeignKey(Reply)

    def __unicode__(self):
        return "%s %s" % (self.keyword_text, self.reply,)


class UnrecognizedWord(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    dealt = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.content, self.time)


class UnrecognizedWordReply(models.Model):
    #如果发过来的消息没有办法自动回复 就回复这个里面指定的内容
    reply_text = models.TextField()

    def __unicode__(self):
        return "%s"%self.reply_text


class UserStatus(models.Model):
    weixin_id = models.CharField(max_length=50)
    STATUS_CHOICES = (("wechat_wall", "wechat_wall"), ("simsimi", "simsimi"), )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    create_time = models.DateTimeField(auto_now_add=True)