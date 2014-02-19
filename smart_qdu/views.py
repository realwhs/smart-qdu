#coding:utf-8
import random
import time
import json
import sae.const
import sae.storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, Http404
from Mail.models import Mail
from DjangoCaptcha import Captcha


def index(request):
    return render(request, "index.html")


def server_error(request):
    return render(request, "500.html")


def about(request):
    return render(request, "About/about_index.html")


def contact(request):
    return render(request, "contact.html")


def get_verify_code(request):
    figures = [2, 3, 4, 5, 6, 7, 8, 9]
    ca = Captcha(request)
    ca.words = [''.join([str(random.sample(figures, 1)[0]) for i in range(0,4)])]
    ca.type = 'word'
    ca.img_width = 100
    ca.img_height = 30
    return ca.display()


def save_file(file_obj):
    #file_name = str(time.time()) + str(random.random()) + file_obj._get_name()
    url = ""
    domain_name = "image"
    s = sae.storage.Client()
    obj = sae.storage.Object(file_obj.read())
    url = s.put(domain_name, str(time.time()) + file_obj.name, obj)
    return url


@csrf_exempt
def upload(request):
    file = request.FILES.get("upload", None)
    if file:
        file_url = save_file(file)
        if file_url:
            response_json = {"status": "success", "content": "success"}
            return HttpResponse(json.dumps(response_json))
        else:
            raise Http404
    else:
        raise Http404