#coding:utf-8
import json
import datetime
import urllib, urllib2
from django.http import HttpResponse
from renren import APIClient
from Renren.models import RenrenOauth
from smart_qdu.const import RENREN_API_KEY, RENREN_CALL_URL, RENREN_SECRET_KEY, RENREN_PAGE_ID



def renren_oauth(request):
    client = APIClient(app_key=RENREN_API_KEY, app_secret=RENREN_SECRET_KEY, redirect_uri=RENREN_CALL_URL)
    url = client.get_authorize_url()
    return HttpResponse("<a href=%s>点击这里进行OAuth授权</a>" % url)


def get_access_token(request):
    code = request.GET.get("code", None)
    if not code:
        return HttpResponse("get请求中没有code参数")
    client = APIClient(app_key=RENREN_API_KEY, app_secret=RENREN_SECRET_KEY, redirect_uri=RENREN_CALL_URL)
    r = client.request_access_token(code)
    access_token = r["access_token"]
    refresh_token = r["refresh_token"]
    RenrenOauth.objects.all().delete()
    RenrenOauth.objects.create(access_token=access_token, refresh_token=refresh_token)
    return HttpResponse("获取AccessToken成功")


def post_info(status):
    r = RenrenOauth.objects.all()
    #access token是一个月的有效期 这里先判断access token是否要过期
    if (datetime.date.today() - r[0].date).days > 25:
        client = APIClient(app_key=RENREN_API_KEY, app_secret=RENREN_SECRET_KEY, redirect_uri=RENREN_CALL_URL)
        r = client.refresh_token(r[0]["refresh_token"])
        access_token = r["access_token"]
        refresh_token = r["refresh_token"]
        RenrenOauth.objects.all().delete()
        RenrenOauth.objects.create(access_token=access_token, refresh_token=refresh_token)

    access_token = r[0].access_token
    api_method = 'status.set'

    api_body = urllib.urlencode({
        "v": "1.0",
        "format": "json",
        "method": api_method,
        "access_token": access_token,
        "status": status,
        "page_id": RENREN_PAGE_ID
    })
    req = urllib2.Request("https://api.renren.com/restserver.do", api_body)
    res = urllib2.urlopen(req)
    s = json.loads(res.read())
    if str(s["result"]) == "1":
        return True
    else:
        return False


def post_test(request):
    status = request.GET.get("status", "Hello world")
    post_info(status)
    return HttpResponse("Hello world")
    #----------------------------
    #Thanks:
    #https://github.com/rellik6/renrenpy
    #http://kymowind.blog.163.com/blog/static/18422229720134127505671/
    #https://github.com/mrluanma/renren_oauth_demo_django