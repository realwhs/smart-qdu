#coding:utf-8
from django.db import models


class Comment(models.Model):
    item_id = models.IntegerField()
    author = models.CharField(max_length=15)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return "%s %s %s" % (self.item_id, self.author, self.content)


class ItemInfo(models.Model):
    classification = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    simple_introduction = models.CharField(max_length=200)
    price = models.FloatField()
    preview_pic_url = models.URLField()
    model = models.TextField()
    total_num = models.IntegerField()
    store_num = models.IntegerField()
    publish_time = models.DateTimeField(auto_now_add=True)
    introduction = models.TextField()
    status = models.BooleanField(default=True)
    comment = models.ManyToManyField(Comment, blank=True, null=True)


class AddressInfo(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    address = models.TextField()

    def __unicode__(self):
        return "%s %s %s %s" % (self.name, self.phone, self.email, self.address)


STATUS_CHOICES = (("-1", "订单已经提交，请等待处理"), ("0", "订单确认，正在处理"),
                  ("1", "订单完成"), ("2", "订单已经取消"), ("3", "订单状态异常"))


class Order(models.Model):
    item_id = models.IntegerField()
    number = models.IntegerField()
    total_price = models.FloatField()
    user_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    address_info = models.ForeignKey(AddressInfo)
    remark = models.TextField(null=True, blank=True)
    #status暂时设计为订单提交状态后为-1，提交后但是没有处理；状态为0的话，就是后台已经受理，订单确认；
    # 状态为1的话，订单完成；状态为2就是取消的订单
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)












