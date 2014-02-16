#coding:utf-8
#import urllib, urllib2
import json
from Account.models import Passport
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from Account.forms import RegisterForm, LoginForm, ChangePswForm
from OnlineShop.models import Order
from LostAndFound.models import InfoDetail
from Mail.models import Mail


def create_user(user_name, email, password):
    Passport.objects.create_user(user_name, email, password)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            password1 = form.cleaned_data["password1"]
            #password2 = form.cleaned_data["password2"]
            #注意  这个地方是简化注册步骤  只输入一个密码即可  兼容以前的设计
            password2 = password1
            email = form.cleaned_data["email"]
            try:
                Passport.objects.get(user_name=user_name)
            except Passport.DoesNotExist:
                try:
                    Passport.objects.get(email=email)
                except Passport.DoesNotExist:
                    if password1 == password2:
                        create_user(user_name, email, password1)
                        #注册成功自动登陆
                        user = auth.authenticate(username=user_name, password=password1)
                        if user is not None and user.is_active:
                            auth.logout(request)
                            auth.login(request, user)
                        #跳转
                        next = request.POST.get("next", "/")
                        response_json = {"status": "success", "redirect": next}
                        return HttpResponse(json.dumps(response_json))
                    else:
                        response_json = {"status": "error", "content": "密码不匹配！"}
                        return HttpResponse(json.dumps(response_json))
                response_json = {"status": "error", "content": "email已经存在"}
                return HttpResponse(json.dumps(response_json))
            response_json = {"status": "error", "content": "用户名已经存在！"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "表单数据错误！"}
            return HttpResponse(json.dumps(response_json))
    else:
        next = request.GET.get("next", "/")
        return render(request, "Account/register_form.html", {"next": next})


def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(username=user_name, password=password)
            if user is not None and user.is_active:
                auth.logout(request)
                auth.login(request, user)
                next = request.POST.get("next", "/")
                #if next == "" or "/register/":
                    #next = "/"
                response_json = {"status": "success", "redirect": next}
                return HttpResponse(json.dumps(response_json))
            else:
                response_json = {"status": "error", "content": "用户名或密码错误"}
                return HttpResponse(json.dumps(response_json))
        response_json = {"status": "error", "content": "表单数据错误"}
        return HttpResponse(json.dumps(response_json))
    else:
        next = request.GET.get("next", "/")
        return render(request, "Account/login_form.html", {"next": next})


def logout(request):
    auth.logout(request)
    return render(request, "message.html", {"action": "alert alert-info", "info": "已经退出登录"})


@login_required(login_url="/login/")
def change_password(request):
    if request.method == "POST":
        form = ChangePswForm(request.POST)
        if form.is_valid():
            user_name = request.user.user_name
            old_password = form.cleaned_data["old_password"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if password1 == password2:
                if auth.authenticate(username=user_name, password=old_password):
                    user = Passport.objects.get(user_name=user_name)
                    user.set_password(password1)
                    user.save()
                    auth.logout(request)
                    return HttpResponseRedirect("/login/")
                else:
                    response_json = {"status": "error", "content": "old password error"}
                return HttpResponse(json.dumps(response_json))
            else:
                response_json = {"status": "error", "content": "passwords not matching"}
                return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "form data error"}
            return HttpResponse(json.dumps(response_json))
    else:
        return render(request, "Account/change_password.html")


@login_required(login_url="/login/")
def user_profile(request):
    mail = Mail.objects.filter(to_user=request.user.user_name, status=False)
    if len(mail):
        new_message = True
    else:
        new_message = False
    info = InfoDetail.objects.filter(user_name=request.user.user_name)
    order = Order.objects.filter(user_name=request.user.user_name)
    return render(request, "Account/user_profile.html", {'lost_and_found_info': info, "order": order, "new_message": new_message})












