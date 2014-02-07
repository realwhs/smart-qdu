#coding:utf-8
import base64
from lxml import etree
from django.http import HttpResponse
import urllib2, cookielib
from Weixin.models import BindJwInfo
from Weixin.encrypt import decrypt
cookie = cookielib.CookieJar()


def visit(url):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322)')]
    f = opener.open(url)
    s = f.read()
    f.close()
    return s


def get_score(weixin_id):
    try:
        jw_info = BindJwInfo.objects.get(weixin_id=weixin_id)
    except BindJwInfo.DoesNotExist:
        return '您还没有绑定教务账号, 点击<a href="http://smartqdu.sinaapp.com/bind_jw/%s/">here</a>, \
        如果要解除绑定，请点击<a href="http://smartqdu.sinaapp.com/unbind_jw/%s/">here</a>' % (weixin_id, weixin_id)
    jw_account = decrypt(base64.b64decode(jw_info.jw_account))
    jw_password = decrypt(base64.b64decode(jw_info.jw_password))
    url = "http://jw.qdu.edu.cn/academic/j_acegi_security_check?j_password=" \
          + jw_password + "&j_username=" + jw_account + "&login=%E7%99%BB%E5%BD%95&password=&username="
    s1 = visit(str(url))
    s2 = visit("http://jw.qdu.edu.cn/academic/manager/score/studentOwnScore.do?groupId=&moduleId=2021")
    page = etree.HTML(s2.decode("utf-8").replace("nbsp;", "-"))
    text = page.xpath(u"//td")[5:]
    info_list = []
    count = 0
    for item in text:
        info_list.append(str(item.text.encode("utf-8")))
        count += 1
    info_list1 = []
    for i in range(0, count / 15):
        tmp_list = []
        for j in range(15 * i, 15 * i + 15):
            tmp_list.append(info_list[j])
        info_list1.append(tmp_list)

    reply_str = ""
    for item in info_list1:
        reply_str = reply_str + item[3] + item[5] + item[-1] + "\n"
    if len(reply_str) == 0:
        return "查询失败 可能是教务账号密码错误或者网络问题"
    return reply_str