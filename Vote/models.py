from django.db import models


class Option(models.Model):
    choice = models.CharField(max_length=30)
    num = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.choice, self.num)


class Voter(models.Model):
    weixin_id = models.CharField(max_length=30)
    status = models.BooleanField(default=True)


class VoteInfo(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    option = models.ManyToManyField(Option)
    voter = models.ManyToManyField(Voter, blank=True)

    def __unicode__(self):
        return "%s %s %s %s" % (self.id, self.title, self.start_time, self.end_time)


