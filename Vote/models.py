#coding:utf-8
from django.db import models


class Option(models.Model):
    choice = models.CharField(max_length=30)
    num = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.choice, self.num)


class Voter(models.Model):
    weixin_id = models.CharField(max_length=30)
    vote_status = models.BooleanField(default=True)
    #True是可以抽奖 False是已经抽奖了
    lottery_status = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s" % (self.vote_status, self.lottery_status)


class Prize(models.Model):
    #level是数字
    level = models.SmallIntegerField()
    #概率
    probability = models.FloatField()
    name = models.CharField(max_length=20)
    total_num = models.IntegerField()
    current_num = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.name, self.current_num)


class VoteInfo(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    option = models.ManyToManyField(Option)
    voter = models.ManyToManyField(Voter, blank=True)
    prize = models.ManyToManyField(Prize)

    def __unicode__(self):
        return "%s %s %s %s" % (self.id, self.title, self.start_time, self.end_time)


class LotteryResult(models.Model):
    weixin_id = models.CharField(max_length=30)
    vote_id = models.IntegerField()
    #这个是VoteInfo中的title
    vote_title = models.CharField(max_length=30)
    prize_name = models.CharField(max_length=20)
    name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    #False表示没有兑奖
    status = models.BooleanField(default=False)
