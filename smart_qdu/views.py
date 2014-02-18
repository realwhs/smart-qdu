#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from Mail.models import Mail


def index(request):
    return render(request, "index.html")


def server_error(request):
    return render(request, "500.html")


def about(request):
    return render(request, "About/about_index.html")


def contact(request):
    return render(request, "contact.html")


def verify(request):
    return HttpResponse("efb54a79260d496bd26b852fd78ae089")