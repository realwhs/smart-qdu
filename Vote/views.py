#coding:utf-8
import json
from django.shortcuts import render
from django.http import Http404, HttpResponse
from Vote.models import Voter, VoteInfo, Option


def vote_reply(vote_id, weixin_id):
    reply_str = "参加投票 请点击http://smartqdu.sinaapp.com/vote/%s/%s" % (str(vote_id), weixin_id)
    #把这个微信 id和投票绑定一起来  添加进来
    #如果没有这个人的绑定记录
    try:
        VoteInfo.objects.get(id=vote_id, voter__weixin_id=weixin_id)
    except VoteInfo.DoesNotExist:
        vote_info = VoteInfo.objects.get(id=vote_id)
        voter = Voter.objects.create(weixin_id=weixin_id)
        vote_info.voter.add(voter)
        return reply_str
    return "您已经投票或者上次的投票链接还没有使用，谢谢！"


def vote(request, vote_id, weixin_id, option=None):
    #option是choice的id
    try:
        vote_info = VoteInfo.objects.get(id=vote_id, voter__weixin_id=weixin_id)
    except VoteInfo.DoesNotExist:
        response_json = {"status": "error",
                         "content": "出现错误，可能的原因是(1) 投票不存在 ；(2) 您没有在微信中回复 直接点击的网址"}
        return HttpResponse(json.dumps(response_json))

    voter_info = Voter.objects.get(weixin_id=weixin_id, voteinfo__id=vote_id)
    if voter_info.status is False:
        response_json = {"status": "error", "content": "您已经投过票了"}
        return HttpResponse(json.dumps(response_json))
    if request.method == "GET":
        #get 显示这个投票页面  url类似/vote/vote_id/weixin_id
        choice = vote_info.option.all()
        #raise ValueError("error")
        return render(request, "Vote/vote_page.html", {"weixin_id": weixin_id, "choice": choice})
    else:
        #参考http://blog.csdn.net/zhucanxiang/article/details/9472799
        #url类似/vote/vote_id/weixin_id
        option_id = request.POST.get("option_id", None)
        if not option_id:
            response_json = {"status": "error", "content": "选项数据不存在"}
            return HttpResponse(json.dumps(response_json))
        try:
            #判断这个choice是不是这个投票的
            vote_info = VoteInfo.objects.get(id=vote_id, option__id=int(option_id))
        except VoteInfo.DoesNotExist:
            response_json = {"status": "error", "content": "choice不存在"}
            return HttpResponse(json.dumps(response_json))
        #如果进行到这里 说明没有异常  投票数加1
        option = Option.objects.get(id=option_id)
        option.update(num=option.num + 1)
        #标记用户状态
        voter = Voter.objects.get(weixin_id=weixin_id)
        voter.update(status=False)
        response_json = {"status": "success", "content": "投票成功"}
        return HttpResponse(json.dumps(response_json))




