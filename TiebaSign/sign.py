#coding:utf-8
import urllib2
import urllib
import cookielib
import re
import json
import time

URL_BAIDU_INDEX = u'http://www.baidu.com/'
#https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true 也可以用这个
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login'
URL_TIEBA_SIGN = "http://tieba.baidu.com/sign/add"


def get_token():
    response = urllib2.urlopen(URL_BAIDU_TOKEN)
    match_val = re.search(u'"token" : "(?P<token_val>.*?)"', response.read())
    token_val = match_val.group('token_val')
    return token_val


def post_request(url, data):
    request = urllib2.Request(url, data)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.add_header('Accept-Encoding', 'gzip, deflate')
    request.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    return response


def get_tbs():
    tbs_url = 'http://tieba.baidu.com/dc/common/tbs'
    tbs_resp = urllib2.urlopen(tbs_url).read()
    return json.loads(tbs_resp)["tbs"]


def check_login(cookie_name_list, cookieJar):
    cookies_dict = {}
    for cookie in cookie_name_list:
        cookies_dict[cookie] = False
    all_cookie_found = True
    for cookie in cookieJar:
        if cookie.name in cookies_dict:
            cookies_dict[cookie.name] = True
    for eachCookie in cookies_dict.keys():
        if not cookies_dict[eachCookie]:
            all_cookie_found = False
            break
    return all_cookie_found


def login(user_name, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    urllib2.urlopen(URL_BAIDU_INDEX)

    token_val = get_token()

    #构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求
    login_data = {
        'username': user_name,
        'password': password,
        'u': 'https://passport.baidu.com/',
        'tpl': 'pp',
        'token': token_val,
        'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
        'isPhone': 'false',
        'charset': 'UTF-8',
        'callback': 'parent.bd__pcbs__ra48vi'
    }
    login_data = urllib.urlencode(login_data)

    post_request(URL_BAIDU_LOGIN, login_data).read()

    cookies_to_check = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
    login_status = check_login(cookies_to_check, cj)
    if login_status:
        #print "login success"
        return True
    else:
        #print 'login failed'
        return False


def auto_sign(user_name, password):
    if not login(user_name, password):
        return {"status": False, "content": "Login Failed"}
    #http://tieba.baidu.com/home/main?un=XXXX&fr=index 这个是贴吧个人主页，各项信息都可以在此找到链接
    page_count = 1
    like_tieba_list = []
    #喜爱贴吧可能有多页，循环获取
    while 1:
        like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
        resp = urllib2.urlopen(like_tieba_url).read()
        resp = resp.decode('gbk').encode('utf8')
        re_like_tieba = '<td><a href="\/f\?kw=.*?" title="(.*?)">.+?<\/a><\/td><td><a class="cur_exp" target="_blank".*?'
        temp_like_tieba = re.findall(re_like_tieba, resp)
        if len(temp_like_tieba) == 0:
            break
        like_tieba_list += temp_like_tieba
        page_count += 1

    #这样就获取到了所有贴吧的名字列表
    info_list = []
    #print like_tieba_list
    for elem in like_tieba_list:
        tmp_dic = {}
        tmp_dic["name"] = elem
        #print tmp_dic["name"]
        i = 3
        while i:
            i -= 1
            time.sleep(1)
            sign_data = {
                "ie": "utf-8",
                "kw": tmp_dic["name"],
                "tbs": get_tbs()
            }
            sign_data = urllib.urlencode(sign_data)

            sign_request = urllib2.Request(URL_TIEBA_SIGN, sign_data)
            sign_response = urllib2.urlopen(sign_request)

            response = json.loads(sign_response.read())

            if response["error"] == "" or response["error"] == u"亲，你之前已经签过了":
                tmp_dic["status"] = True
                break
            else:
                tmp_dic["status"] = False
        info_list.append(tmp_dic)
    return {"status": True, "result": info_list}

