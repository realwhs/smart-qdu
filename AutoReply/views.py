#coding:utf-8
import datetime
import time
import json
import urllib2
from smart_qdu.const import WEIXIN_ID, WEIXIN_NAME
from AutoReply.models import Keyword, UnrecognizedWord, UnrecognizedWordReply
from EmptyClassroom.views import query_empty_classroom_weixin
from Vote.views import vote_reply
from Weixin.get_score import get_score


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
    return u"青岛：" + day1 + "\n" + day2 + "\n" + day3


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


def news_reply_xml(to_user_name, title, description, pic_url, url):
    xml = """
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>1</ArticleCount>
            <Articles>
            <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>
            </Articles>
            </xml> """ % (to_user_name, WEIXIN_ID, str(int(time.time())), title, description, pic_url, url)
    return xml


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


def auto_reply(to_username, content, msg_type):
    if msg_type == "text":
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
            else:
                UnrecognizedWord.objects.create(content=content, time=datetime.datetime.now())
        #如果存在这个关键词 但是不是执行动作 就应该按照设置回复  其中回复分为纯文本回复和图文消息回复
        #先判断这是的回复类型是什么
        elif re.reply.reply_type == "text" and re.reply.valid is True:
            #statistics("auto_reply")
            return text_msg_reply_xml(to_username, re.reply.reply_text)
        elif re.reply.reply_type == "news" and re.reply.valid is True:
            #statistics("auto_reply")
            #print news_reply_xml(to_username, re.reply.title, re.reply.description, re.reply.pic_url, re.reply.url)
            return news_reply_xml(to_username, re.reply.title, re.reply.description, re.reply.pic_url, re.reply.url)
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














