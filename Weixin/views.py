#coding:utf-8
import hashlib
import json
import urllib, urllib2
from smart_qdu.const import WEIXIN_TOKEN
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from lxml import etree
from smart_qdu.const import WEIXIN_APPID, WEIXIN_APPSECRET
from AutoReply.views import auto_reply
#from Statistics.views import statistics


@csrf_exempt
def weixin_main(request):
    #如果是get  就应该是直接打开的这个url  如果是微信的服务器校验  就返回校验结果  如果没有检验参数就返回没有响应
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        #refer : http://mp.weixin.qq.com/wiki/index.php?title=%E6%8E%A5%E6%94%B6%E6%99%AE%E9%80%9A%E6%B6%88%E6%81%AF
        xml_str = smart_str(request.body)
        xml = etree.fromstring(xml_str)
        msg_type = xml.find("MsgType").text
        from_user_name = xml.find("FromUserName").text
        #暂时只支持文本消息的获取 而且各种消息的xml结构不一样  先判断消息类型
        if msg_type == "text":
            #纯文本消息
            #statistics("message_received")
            content = xml.find("Content").text
            return HttpResponse(auto_reply(from_user_name, content, msg_type))
        elif msg_type == "event":
            event = xml.find("Event").text
            #用户关注事件
            if event == "subscribe":
                #statistics("subscribe")
                return HttpResponse(auto_reply(from_user_name, "用户关注事件", "text"))
            elif event == "unsubscribe":
                print "用户取消关注"
            elif event == "CLICK":
                event_key = xml.find("EventKey").text
                return HttpResponse(auto_reply(from_user_name, event_key, "text"))
            else:
                print "error"
        else:
            #不支持的消息类型
            return HttpResponse(auto_reply(from_user_name, "不支持的消息类型", "text"))


def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (WEIXIN_APPID, WEIXIN_APPSECRET)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = json.loads(response.read())
    return content["access_token"]


@login_required(login_url="/login/")
def access_token(request):
    if not request.user.is_staff:
        return HttpResponse("权限错误")
        #貌似是python      urlencode的问题  http://www.the5fire.com/urllib-urlencode-extend.html
    return render(request, "Weixin/access_token.html", {"access_token": get_access_token()})




