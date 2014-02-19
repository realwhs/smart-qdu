#coding:utf-8
#import random
#import sae.const
#import sae.storage
import json
import time
import sae.const
import sae.storage
import os.path
from DjangoCaptcha import Captcha
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from LostAndFound.models import InfoDetail, ITEM_TYPE_CHOICE, Comment
from django.contrib.auth.decorators import login_required
from LostAndFound.forms import PostInfoForm, CommentForm


def save_file(file_obj):
    #file_name = str(time.time()) + str(random.random()) + file_obj._get_name()
    domain_name = "image"
    s = sae.storage.Client()
    obj = sae.storage.Object(file_obj.read())
    url = s.put(domain_name, str(time.time()) + file_obj.name, obj)
    return url


def index_page(request):
    info_all = InfoDetail.objects.filter(status=True).order_by("-id")[0:10]
    return render(request, "LostAndFound/index_page.html", {"info": info_all})


#构造这样的url   /post_info/lost(found)
@login_required(login_url="/login/")
def post_info(request, info_type="lost"):
    if request.method == "POST":
        if not (info_type == "lost" or info_type == "found"):
            raise Http404

        form = PostInfoForm(request.POST)
        #return HttpResponse(form)
        if form.is_valid():
            item_name = form.cleaned_data["item_name"]
            item_type = form.cleaned_data["item_type"]
            location = form.cleaned_data["location"]
            time = form.cleaned_data["time"]
            content = form.cleaned_data["content"]
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            qq = form.cleaned_data["qq"]
            email = form.cleaned_data["email"]
            #image = form.cleaned_data["image"]
            #return HttpResponse(request.FILES['image'])
            try:
                image = request.FILES["image"]
                if not (os.path.splitext(image.name)[-1] == ".jpg"
                        or os.path.splitext(image.name)[-1] == ".png"
                        or os.path.splitext(image.name)[-1] == ".bmp"):
                    return render(request, "message.html", {"action": "alert alert-info", "info": "文件拓展名错误！"})
                image_url = save_file(image)
            except KeyError:
                image_url = None
            info = InfoDetail.objects.create(user_name=request.user.user_name, info_type=info_type,
                                             item_name=item_name, item_type=item_type, image_url=image_url,
                                             content=content, location=location, time=time,
                                             name=name, phone=phone, qq=qq, email=email, status=True)
            #response_json = {"status": "success", "redirect": "/lost_and_found/info/" + str(info.id)}
            #return HttpResponse(json.dumps(response_json))
            return HttpResponseRedirect("/lost_and_found/info/" + str(info.id))
        else:
            return render(request, "message.html", {"action": "alert alert-info", "info": "表单数据错误！请检查填写！"})
    else:
        if info_type == "lost":
            return render(request, "LostAndFound/post_info_form.html", {"item_type": ITEM_TYPE_CHOICE,
                                                                        "info_type": info_type})
        elif info_type == "found":
            return render(request, "LostAndFound/post_info_form.html", {"item_type": ITEM_TYPE_CHOICE,
                                                                        "info_type": info_type})
        else:
            raise Http404


def show_info_detail(request, info_id):
    try:
        info = InfoDetail.objects.get(id=info_id)
    except InfoDetail.DoesNotExist:
        raise Http404
    return render(request, "LostAndFound/info_page.html",
                  {"info": info, "comment": info.comment.all(), "info_id": info_id})


def get_contact(request, info_id):
    try:
        info = InfoDetail.objects.get(id=info_id)
    except InfoDetail.DoesNotExist:
        raise Http404
    _code = request.POST.get('verify_code', " ")
    ca = Captcha(request)
    if not ca.check(_code):
        response_json = {"status": "error", "content": "验证码错误"}
        return HttpResponse(json.dumps(response_json))
    else:
        response_str = u""
        if info.phone:
            response_str += (u"手机：" + info.phone + u"；")
        if info.email:
            response_str += (u"邮箱：" + info.email + u"；")
        if info.qq:
            response_str += (u"qq：" + info.qq + u"；")
        response_json = {"status": "success", "content": response_str}
        return HttpResponse(json.dumps(response_json))


#@login_required(login_url="/login/")
def post_comment(request, info_id):
    if request.method == "POST":
        if not request.user.is_authenticated():
            response_json = {"status": "not_login"}
            return HttpResponse(json.dumps(response_json))
        try:
            info = InfoDetail.objects.get(id=info_id)
        except InfoDetail.DoesNotExist:
            raise Http404
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["comment"]
            comment = Comment.objects.create(author=request.user.user_name, content=content)
            info.comment.add(comment)
            #return HttpResponseRedirect("/lost_and_found/info/" + info_id)
            response_json = {"status": "success"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "内容为空，请重新填写！"}
            return HttpResponse(json.dumps(response_json))
    else:
        return HttpResponseRedirect("/lost_and_found/info/" + info_id)


@login_required(login_url="/login/")
def mark_item_status(request, info_id):
    try:
        info = InfoDetail.objects.get(user_name=request.user.user_name, id=info_id)
    except InfoDetail.DoesNotExist:
        raise Http404
    info.status = False
    info.save()
    return HttpResponseRedirect("/lost_and_found/info/" + str(info.id))


def show_info_list(request, page_num):
    info_all = InfoDetail.objects.filter(status=True).order_by("-id")
    page_info = Paginator(info_all, 5)
    total_page = page_info.num_pages
    if int(page_num) > total_page:
        raise Http404
    return render(request, "LostAndFound/info_list.html", {"info": page_info.page(page_num),
                                                           "page_num": str(page_num),
                                                           "total_page": str(total_page),
                                                           "next_page": str(int(page_num) + 1),
                                                           "pre_page": str(int(page_num) - 1)})

