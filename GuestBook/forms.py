#coding:utf-8
from django import forms


class MessageForm(forms.Form):
    name = forms.CharField(max_length=10, required=False)
    email = forms.EmailField(required=False)
    title = forms.CharField(max_length=30)
    content = forms.TextField()
