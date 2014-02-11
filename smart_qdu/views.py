#coding:utf-8
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def server_error(request):
    return render(request, "500.html")


def about(request):
    return render(request, "About/about_index.html")


def contact(request):
    return render(request, "contact.html")