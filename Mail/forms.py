#coding:utf-8
from django import forms


class MailForm(forms.Form):
    to_user = forms.CharField(max_length=30)
    subject = forms.CharField(max_length=40)
    content = forms.CharField(max_length=1000)
