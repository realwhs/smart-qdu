#coding:utf-8
import datetime
import time
import json
import urllib2
from django.utils.timezone import utc
from smart_qdu.const import WEIXIN_ID, WEIXIN_NAME
from AutoReply.models import Keyword, UnrecognizedWord, UnrecognizedWordReply, UserStatus
from EmptyClassroom.views import query_empty_classroom_weixin
from Vote.views import vote_reply
from Weixin.get_score import get_score


#获取空气质量状况
def get_air_quality():
    req = urllib2.Request("http://www.pm25.in/api/querys/pm2_5.json?city=qingdao&token=5TpZRDLoXrsxAnZWUhnR&stations=no")
    response = urllib2.urlopen(req).read()
    response = json.loads(response)[0]
    return u"实时空气质量：" + response["quality"] + u"，pm2.5：" + str(response["pm2_5"])


#获取天气http://developer.baidu.com/map/carapi-7.htm
def get_weather(city="青岛"):
    url = "http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=bldsc4KQ5dvqj1T1YDxIDCmz" % city
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = json.loads(response.read())
    weather_list = content["results"][0]["weather_data"]
    day1 = weather_list[0]["date"] + u"，" + weather_list[0]["weather"] + u"，" + weather_list[0]["wind"] + u"，" + \
        weather_list[0]["temperature"]
    day2 = weather_list[1]["date"] + u"，" + weather_list[1]["weather"] + u"，" + weather_list[0]["wind"] + u"，" + \
        weather_list[1]["temperature"]
    day3 = weather_list[2]["date"] + u"，" + weather_list[2]["weather"] + u"，" + weather_list[0]["wind"] + u"，" + \
        weather_list[2]["temperature"]
    return u"青岛：" + day1 + "\n" + day2 + "\n" + day3 + "\n" + get_air_quality()


def text_msg_reply_xml(to_user_name, message):
    #根据传进来的参数  回复http响应  回复text消息
    xml = """
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>""" % (to_user_name, WEIXIN_ID, str(int(time.time())), message)
    return xml


def build_news_xml(to_user_name, item_num):
    news_xml = """
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>%s</ArticleCount>
            <Articles>
            """ % (to_user_name, WEIXIN_ID, str(int(time.time())), item_num)
    return news_xml


def build_article_xml(title, description, pic_url, url):
    item_xml = """
            <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>
            """ % (title, description, pic_url, url)
    return item_xml


def news_reply_xml(to_user_name, news_reply):
    item_num = len(news_reply)
    first_xml = build_news_xml(to_user_name, item_num)
    for news in news_reply:
        first_xml += build_article_xml(news.title, news.description, news.pic_url, news.url)
    end_xml = """
            </Articles>
            </xml> """
    return first_xml + end_xml


def music_reply_xml(to_user_name, title, description, music_url, hq_music_url):
    xml = """
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[music]]></MsgType>
            <Music>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <MusicUrl><![CDATA[%s]]></MusicUrl>
            <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
            </Music>
            </xml>
            """ % (to_user_name, WEIXIN_ID, str(int(time.time())), title, description, music_url, hq_music_url)
    return xml


#refer:http://my.oschina.net/yangyanxing/blog/197998
def chat(ask):
    ask = ask.encode('UTF-8')
    enask = urllib2.quote(ask)
    baseurl = r'http://www.simsimi.com/func/req?msg='
    url = baseurl+enask+'&lc=ch&ft=0.0'
    try:
        resp = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return "小黄鸡都被你们玩坏了，歇歇吧"
    reson = json.loads(resp.read())
    if reson["msg"] == "OK.":
        if reson["response"].find(u"微信") == -1:
            return reson["response"]
    return "小黄鸡都被你们玩坏了，歇歇吧"


def check_user_status(weixin_id, content):
    try:
        r = UserStatus.objects.get(weixin_id=weixin_id)
    except UserStatus.DoesNotExist:
        return None
    if r.status == "simsimi":
        #如果这个用户的状态创建已经超过一个小时或者停止聊天指令   这个状态就会被删除  否则就接入聊天
        if (datetime.datetime.utcnow().replace(tzinfo=utc) - r.create_time).seconds >= 1800:
            r.delete()
        elif content == u"停止聊天":
            r.delete()
            return "已经退出聊天状态"
        else:
            return chat(content)
    else:
        return None


def auto_reply(to_username, content, msg_type):
    if msg_type == "text":
        r = check_user_status(to_username, content)
        #如果r有返回值  说明聊天中或者其他状态（待开发)  没有的话 就忽略
        if r:
            return text_msg_reply_xml(to_username, r)
        try:
            re = Keyword.objects.get(keyword_text=content)
        except Keyword.DoesNotExist:
            UnrecognizedWord.objects.create(content=content, time=datetime.datetime.now())
            #如果运行到这里 说明没有命中我们的关键词回复  所以在数据库中查询这种情况下怎么回
            unrecognized_reply = UnrecognizedWordReply.objects.all()
            return text_msg_reply_xml(to_username, unrecognized_reply[0].reply_text)
        #如果存在这个关键词 而且是设置为执行动作 就先判断动作 然后执行
        if re.reply.reply_type == "action" and re.reply.valid is True:
            if re.reply.action == "EmptyClassroomQuery":
                result = query_empty_classroom_weixin(re.reply.parameter)
                return text_msg_reply_xml(to_username, result)
            elif re.reply.action == "Weather":
                result = get_weather()
                return text_msg_reply_xml(to_username, result)
            elif re.reply.action == "score":
                result = get_score(to_username)
                return text_msg_reply_xml(to_username, result)
            elif re.reply.action == "vote":
                result = vote_reply(re.reply.parameter, to_username)
                return text_msg_reply_xml(to_username, result)
            elif re.reply.action == "create_chat_status":
                UserStatus.objects.create(weixin_id=to_username, status="simsimi")
                return text_msg_reply_xml(to_username, "你已经进入聊天状态了！开始吧！回复“停止聊天”即可退出")
            elif re.reply.action == "delete_chat_status":
                try:
                    UserStatus.objects.get(weixin_id=to_username)
                except UserStatus.DoesNotExist:
                    return text_msg_reply_xml(to_username, "您没有进入聊天状态")
                return text_msg_reply_xml(to_username, "已经恢复正常状态！")
            else:
                UnrecognizedWord.objects.create(content=content, time=datetime.datetime.now())
        #如果存在这个关键词 但是不是执行动作 就应该按照设置回复  其中回复分为纯文本回复和图文消息回复
        #先判断这是的回复类型是什么
        elif re.reply.reply_type == "text" and re.reply.valid is True:
            #statistics("auto_reply")
            return text_msg_reply_xml(to_username, re.reply.reply_text)
        elif re.reply.reply_type == "news" and re.reply.valid is True:
            news_reply = re.reply.news_reply.all()
            #news_num = len(news_reply)
            return news_reply_xml(to_username, news_reply)
        elif re.reply.reply_type == "music" and re.reply.valid is True:
            return music_reply_xml(to_username, re.reply.music_title, re.reply.music_description,
                                   re.reply.music_url, re.reply.music_hq_url)
        #这个就是存在这个关键词和对应的回复 但是被标记为无效的  所有还是无法识别
        else:
            UnrecognizedWord.objects.create(content=content, time=datetime.datetime.now())
            unrecognized_reply = UnrecognizedWordReply.objects.all()
            return text_msg_reply_xml(to_username, unrecognized_reply[0].reply_text)
    else:
        #如果不是文本消息暂时无法有效的处理
        unrecognized_reply = UnrecognizedWordReply.objects.all()
        return text_msg_reply_xml(to_username, unrecognized_reply[0].reply_text)














