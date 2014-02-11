#coding:utf-8
import json
import random
from django.shortcuts import render
from django.http import Http404, HttpResponse
from Vote.models import VoteInfo, Prize, LotteryResult, Voter


def rand_operation(total_num, tmp_list):
    prize_id = -1
    flag = False
    #在1-total_num中产生一个随机数
    rand = random.randint(1, total_num)
    #判断这个随机数在哪个范围内  因为1-10代表是一等奖  以此类推
    for i in range(0, len(tmp_list) - 1):
        if tmp_list[i] <= rand <= tmp_list[i + 1]:
            #prize id代表几等奖
            prize_id = i + 1
            flag = True
            break
    return {"prize_id": prize_id, "flag": flag}


def lottery(request, vote_id, weixin_id):
    try:
        vote_info = VoteInfo.objects.get(id=vote_id)
    except VoteInfo.DoesNotExist:
        raise Http404
    #已经抽奖的用户判断
    try:
        Voter.objects.get(weixin_id=weixin_id, lottery_status=True, voteinfo__id=vote_id)
    except Voter.DoesNotExist:
        response_json = {"status": "error", "content": "1 weixin_id或者vote_id错误 2您已经抽过奖了"}
        return HttpResponse(json.dumps(response_json))

    prize = vote_info.prize.all()
    tmp_list = []
    #获取各种奖项的礼品数量列表  然后叠加
    #比如一等奖10个  二等奖40个  三等奖 50个
    #叠加后就变成[10, 50, 100]
    for i in range(0, len(prize)):
        if i == 0:
            tmp_list.append(prize[i].total_num)
        else:
            tmp_list.append(prize[i].total_num + tmp_list[i - 1])
    total_num = prize[0].total_num / prize[0].probability
    while True:
        result = rand_operation(total_num, tmp_list)
        #如果抽到了奖品 而且对应的奖品为0
        if result["flag"] and prize[result["prize_id - 1"]] == 0:
            continue
        else:
            break
    #现在肯定是获奖了而且有奖品或者没有中奖
    #先更新用户抽奖状态
    voter = Voter.objects.get(weixin_id=weixin_id, voteinfo__id=vote_id)
    voter.update(lottery_status=False)

    if result["flag"] is False:
        #返回前端网页
        return render(request, "Vote/lottery/lottery.html",
                      {"status": "False", "action": "alert('很遗憾没有中奖')", "redirect": "..", "animate_to": 1000})
        #print "没有中奖"
    else:
        #奖品数量减1
        p = Prize.objects.get(voteinfo__id=vote_id, level=result["prize_id"])
        p.update(current_num=p.current_num - 1)
        #中奖信息入库
        LotteryResult.objects.create(weixin_id=weixin_id, vote_id=vote_info.id, vote_title=vote_info.title, prize_name=p.name)
        #返回前端网页
        return render(request, "Vote/lottery/lottery.html",
                      {"status": "True", "action": "alert('恭喜你中奖了')", "redirect": "..", "animate_to": 1000})


def get_info(request, weixin_id, vote_id):
    #bug  可能存在同一个weixin_id没有兑奖之前填写多个资料的问题
    try:
        r = LotteryResult.objects.get(weixin_id=weixin_id, vote_id=vote_id, status=False)
    except LotteryResult.DoesNotExist:
        response_json = {"status": "error", "content": "1 您没有中奖 2 您已经兑奖 3 weixin id或者vote_id错误"}
        return HttpResponse(json.dumps(response_json))
    if request.method == "POST":
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        r.update(name=name, phone=phone)
        response_json = {"status": "success", "content": "登记成功"}
        return HttpResponse(json.dumps(response_json))
    else:
        return render(request, "Vote/lottery/get_info.html", {"weixin_id": weixin_id, "vote_id": vote_id})















