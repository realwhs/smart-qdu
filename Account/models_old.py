#coding:utf-8

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#管理类
class PassportManager(BaseUserManager):
    #创建user
    def create_user(self, email, user_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
 
        user = self.model(
            email=PassportManager.normalize_email(email),
            user_name=user_name,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    #创建超级管理员
    def create_superuser(self, email, user_name, password):
        user = self.create_user(email, user_name=user_name, password=password,)
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


#通行证
class Passport(AbstractBaseUser):
    user_name = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=140, blank=True, null=True)
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']
    objects = PassportManager()

    def __unicode__(self):
        return "%s %s %s"%(self.user_name, self.email, self.password)