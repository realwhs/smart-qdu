#coding:utf-8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class PassportManager(BaseUserManager):
    def create_user(self, user_name, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_name=user_name,
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password, **extra_fields):
        user = self.create_user(user_name, email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# 在settings里面指定这个User类为AUTH_USER_MODEL
class Passport(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=15, unique=True, db_index=True)
    email = models.EmailField(verbose_name='email address', max_length=20)
    is_staff = models.BooleanField('staff status', default=False, help_text='flag for log into admin site.')
    is_active = models.BooleanField('active', default=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']
    objects = PassportManager()     # 在这里关联自定义的UserManager

    def get_full_name(self):
        return self.user_name

    def get_short_name(self):
        return self.user_name

    def __unicode__(self):
        return self.user_name
