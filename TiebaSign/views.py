#coding:utf-8

import json
import base64
from sae.taskqueue import Task, TaskQueue
from TiebaSign.sign import auto_sign, login
from TiebaSign.models import TiebaAccount, SignStatus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Weixin.encrypt import encrypt, decrypt


@login_required(login_url="/login/")
def add_account(request):
    if request.method == "POST":

        tieba_user_name = request.POST.get("tieba_user_name", " ")
        tieba_password = request.POST.get("tieba_password", " ")
        #return HttpResponse(login(tieba_user_name, tieba_password))
        if login(tieba_user_name, tieba_password):
            TiebaAccount.objects.create(user_name=request.user.user_name, tieba_user_name=tieba_user_name,
                                        tieba_password=base64.b64encode(encrypt(tieba_password)), task_status=False)
            response_json = {"status": "success"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error",
                             "content": "登录失败，请检查账号密码；有时候登录出现验证码也导致失败！"}
            return HttpResponse(json.dumps(response_json))
    else:
        raise Http404


@login_required(login_url="/login/")
def sign_management(request):
    try:
        info = TiebaAccount.objects.get(user_name=request.user.user_name)
    except TiebaAccount.DoesNotExist:
        return render(request, "TiebaSign/add_tieba_account.html")
    return render(request, "TiebaSign/sign_management.html", {"info": info})


def sign_operation(request):
    tieba_user_name = request.GET.get("user_name", "")
    try:
        account = TiebaAccount.objects.get(tieba_user_name=tieba_user_name)
    except TiebaAccount.DoesNotExist:
        raise Http404
    result = auto_sign(tieba_user_name, decrypt(base64.b64decode(account.tieba_password)))
    if result["status"]:
        account.sign_status.all().delete()
        account.update(task_tatus=True)
        for item in request["result"]:
            sign_status = SignStatus.objects.create(tieba_name=item["name"], status=item["status"])
            account.add(sign_status)
        return HttpResponseRedirect("/sign/management/")
    else:
        account.update(task_status=False)
        return HttpResponseRedirect("/sign/management/")


def sign_all(request):
    account = TiebaAccount.objects.all()
    for item in account:
        queue = TaskQueue("TiebaSign")
        queue.add(Task("/sign/?user_name=" + item.tieba_user_name))
    return HttpResponse("all task added")






