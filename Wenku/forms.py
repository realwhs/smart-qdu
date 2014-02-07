#coding:utf-8
from django import forms


class FileUploadForm(forms.Form):
    title = forms.CharField(max_length=30)
    simple_introduction = forms.CharField(max_length=80)
