#coding:utf-8
from django import forms


class ItemNumberForm(forms.Form):
    number = forms.IntegerField()


class OrderForm(forms.Form):
    #item_number = forms.IntegerField()
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=11)
    email = forms.EmailField()
    address = forms.CharField(max_length=100)
    remark = forms.CharField(max_length=100, required=False)
