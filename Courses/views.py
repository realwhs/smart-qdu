#coding:utf-8
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render
from Courses.models import CourseInfo, Comment
from django.core.paginator import Paginator
#from Courses.forms import CommentForm


def courses_index(request):
    comment = Comment.objects.order_by("-publish_time")[0:10]
    comment_list = []
    for item in comment:
        tmp_dic = {}
        info = CourseInfo.objects.get(comment__id=item.id)
        if item.is_anonymous:
            tmp_dic["user_name"] = "匿名用户"
        else:
            tmp_dic["user_name"] = item.user_name
        tmp_dic["course_name"] = info.name
        tmp_dic["course_id"] = info.id
        tmp_dic["teacher_name"] = info.teacher_name
        tmp_dic["time"] = item.publish_time
        if len(item.content) >= 30:
            tmp_dic["content"] = item.content[0:27] + u"。。。"
        else:
            tmp_dic["content"] = item.content
        comment_list.append(tmp_dic)
    return render(request, "Courses/index.html", {"comment_list": comment_list})


def course_info(request, course_id):
    try:
        info = CourseInfo.objects.get(id=int(course_id))
    except CourseInfo.DoesNotExist:
        raise Http404
    day = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天",)
    info.day = day[info.day - 1]
    c = info.comment.all()
    return render(request, "Courses/course_info.html", {"info": info, "comment": c})


def post_comment(request, course_id):
    if not request.user.is_authenticated():
        response_json = {"status": "not_login", "redirect": "/login/?next=" + request.META.get('HTTP_REFERER', "/")}
        return HttpResponse(json.dumps(response_json))

    try:
        info = CourseInfo.objects.get(id=int(course_id))
    except CourseInfo.DoesNotExist:
        raise Http404
    if request.method == "POST":
        is_anonymous = request.POST.get("is_anonymous", False)
        score = request.POST.get("score", 6)
        if score == 6:
            response_json = {"status": "error", "content": "请不要忘了评分啊"}
            return HttpResponse(json.dumps(response_json))
        content = request.POST.get("comment", "")
        if len(content) < 5:
            response_json = {"status": "error", "content": "你写这么几个字给谁看啊，多写点呗~~"}
            return HttpResponse(json.dumps(response_json))
        comment = Comment.objects.create(user_name=request.user.user_name, is_anonymous=is_anonymous,
                                         score=score, content=content)
        info.comment.add(comment)
        response_json = {"status": "success"}
        return HttpResponse(json.dumps(response_json))
    else:
        raise Http404


def search(request):
    if request.method == "POST":
        key_word = request.POST.get("key_word", "")
        if len(key_word) == 0:
            return render(request, "message.html", {"action": "alert alert-info", "info": "你不输关键词搜啥啊~~"})
        info = CourseInfo.objects.all()
        tmp_list = []
        for item in info:
            if key_word in item.teacher_name or key_word in item.name:
                tmp_list.append(item)
        return render(request, "Courses/search_result.html", {"result": tmp_list, "number": len(tmp_list)})
    else:
        raise Http404


def show_all_courses(request, page_num):
    info_all = CourseInfo.objects.all()
    page_info = Paginator(info_all, 30)
    total_page = page_info.num_pages
    if int(page_num) > total_page:
        raise Http404
    return render(request, "Courses/all_courses.html", {"info": page_info.page(page_num), "page_num": str(page_num),
                                                        "total_page": str(total_page), "next_page": str(int(page_num) + 1)})


def import_info(request):
    f = open("class_list.csv", "r")
    for line in f.readlines():
        tmp_list = line.decode("GBK").split(",")
        CourseInfo.objects.create(campus=tmp_list[0], course_id=tmp_list[1], name=tmp_list[2], teacher_name=tmp_list[3], day=int(tmp_list[4]), classroom=tmp_list[5], term=tmp_list[6], status=False)
    return HttpResponse("success")