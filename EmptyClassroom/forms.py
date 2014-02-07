#coding:utf-8
from django import forms


class EmptyClassroomQueryForm(forms.Form):
    building_name = forms.CharField(max_length=15)
    week = forms.CharField(max_length=5)
    day = forms.CharField(max_length=5)
    class_order = forms.CharField(max_length=5)
