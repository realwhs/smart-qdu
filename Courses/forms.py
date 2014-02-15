#coding:utf-8
from django import forms


class CommentForm(forms.Form):
    is_anonymous = forms.Checkbox()
    score = forms.IntegerField()
    content = forms.CharField(max_length=1000)