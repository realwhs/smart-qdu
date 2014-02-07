#coding:utf-8
import base64
from Weixin.forms import BindJwForm
from Weixin.models import BindJwInfo
from Weixin.encrypt import encrypt, decrypt
from django.shortcuts import render
from django.http import Http404


def bind_jw(request, weixin_id):
    if request.method == "POST":
        form = BindJwForm(request.POST)
        if form.is_valid():
            jw_account = form.cleaned_data["jw_account"]
            jw_password = form.cleaned_data["jw_password"]
            #BindJwInfo.objects.create(weixin_id=weixin_id, jw_account=encrypt(jw_account),
                                      #jw_password=encrypt(jw_password))
            try:
                BindJwInfo.objects.get(weixin_id=weixin_id)
            except BindJwInfo.DoesNotExist:
                #BindJwInfo.objects.create(weixin_id=weixin_id, jw_account=jw_account,
                                          #jw_password=jw_password)
                BindJwInfo.objects.create(weixin_id=weixin_id, jw_account=base64.b64encode(encrypt(jw_account)),
                                          jw_password=base64.b64encode(encrypt(jw_password)))
                return render(request, "message.html", {"action": "alert alert-info", "info": jw_account + u"绑定教务成功，您可以回复“成绩”查询"})
            return render(request, "message.html", {"action": "alert alert-info",
                                                    "info": u"每个微信账号只能绑定一个教务账号，您已经绑定了" + jw_account + u'，解除绑定请点击http://smartqdu.sinaapp.com/unbind_jw/%s/' % weixin_id})
        else:
            return render(request, "message.html", {"action": "alert alert-info", "info": "表单数据错误"})
    else:
        return render(request, "Weixin/bind_jw.html", {"weixin_id": weixin_id})


def unbind_jw(request, weixin_id):
    try:
        info = BindJwInfo.objects.get(weixin_id=weixin_id)
    except BindJwInfo.DoesNotExist:
        return render(request, "message.html", {"action": "alert alert-info", "info": "该微信账号没有绑定教务账号"})
    info.delete()
    return render(request, "message.html", {"action": "alert alert-info", "info": "账号解绑成功"})