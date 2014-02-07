#coding:utf-8

import datetime
import json
from EmptyClassroom.models import EmptyClassroom
from EmptyClassroom.forms import EmptyClassroomQueryForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def get_day():
    day = datetime.datetime.now().weekday()
    #星期一是返回0  星期天返回6
    return day + 1


def get_week(): 
    term_begin = datetime.date(2013, 9, 2)
    now = datetime.date.today()
    #如果两个日期相同返回的是1  所以我们计算是第几天的时候就要加上1
    if ((now - term_begin).days + 1) % 7 == 0:
        return ((now - term_begin).days + 1) / 7
    else:
        return ((now - term_begin).days + 1) / 7 + 1


def get_class():
    hour_now = datetime.datetime.now().hour
    min_now = datetime.datetime.now().minute
    total_min = (hour_now - 8) * 60 + min_now
    if total_min <= 50:
        return 1
    elif 50 < total_min <= 110:
        return 2
    elif 110 < total_min <= 180:
        return 3
    elif 180 < total_min <= 240:
        return 4
    elif 240 < total_min <+ 380:
        return 5
    elif 380 < total_min <= 440:
        return 6
    elif 440 < total_min <= 500:
        return 7
    elif 500 < total_min <= 550:
        return 8
    elif 550 < total_min <= 680:
        return 9
    elif 680 < total_min <= 750:
        return 10
    else:
        return 11


def query_empty_classroom_weixin(building_name):
    #ManyToManyField的使用见https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/
    classroom = EmptyClassroom.objects.filter(building_name=building_name, week=get_week(), day=get_day)
    class_room_str = ""
    for item in classroom:
        status_list = item.classroom_status.split(",")
        if not int(status_list[get_class() - 1]):
            classroom_str = class_room_str + item.room_name + "\n"
    if len(class_room_str) == 0:
        reply_str = "%s在今天第%s节课的空教室信息为空，如果有什么疑问，请于我们联系" % (building_name, str(get_class()))
        return reply_str
    else:
        reply_str = "%s在今天第%s节课的空教室信息为%s" % (building_name, str(get_class()), classroom_str)
        return reply_str


def query_empty_classroom_web(request):
    if request.method == "POST":
        form = EmptyClassroomQueryForm(request.POST)
        if form.is_valid():
            building_name = form.cleaned_data["building_name"]
            week = form.cleaned_data["week"]
            day = form.cleaned_data["day"]
            class_order = form.cleaned_data["class_order"]
            classroom_info = EmptyClassroom.objects.filter(building_name=building_name, week=int(week), day=int(day))
            classroom = []
            for item in classroom_info:
                status_list = item.classroom_status.split(",")
                if not int(status_list[get_class() - 1]):
                    classroom.append(item.room_name)
            return render(request, "EmptyClassroom/query_result.html",
                          {"building_name": building_name,
                           "week": week, "day": day,
                           "class_order": class_order,
                           "result": classroom})
        else:
            return HttpResponse("invalid form data")
    else:
        #创建教学楼选择列表
        building_list = ["博知楼", "博远楼", "reserved", ]
        #创建class选择列表
        class_list = []
        for i in range(1, 12):
            class_list.append(str(i))
        #创建week选择列表
        week_list = []
        for i in range(1, 21):
            week_list.append(str(i))
        #创建day选择列表
        day_list = ["1", "2", "3", "4", "5", "6", "7"]

        #将week, day等信息也返回  改变网页显示的默认值
        return render(request, "EmptyClassroom/query_form.html", {"week_list": week_list,
                                                                  "week": str(get_week()),
                                                                  "day_list": day_list,
                                                                  "day": str(get_day()),
                                                                  "class_list": class_list,
                                                                  "class": str(get_class()),
                                                                  "building_list": building_list})


#下面的函数是从文件中导入教室信息
#文件格式是这样的
#building_name, room_name, week, day, class1_status, class2_status...一共是十一节课"""
def import_classroom_info(request):
    if request.user.is_staff:
        EmptyClassroom.objects.all().delete()

        f = open(r"classroom_info.csv", "r")
        for line in f.readlines():
            classroom_list = line.decode("GBK").split(",")
            status_str = ""
            for i in range(4, 14):
                status_str += (str(classroom_list[i]) + ",")
            status_str += str(classroom_list[-1])
            EmptyClassroom.objects.create(building_name=classroom_list[0], room_name=classroom_list[1],
                                          week=classroom_list[2], day=classroom_list[3], classroom_status=status_str)
        del f
        return render(request, "message.html", {"action": "alert alert-info", "info": "导入成功"})
    else:
        return HttpResponse("error forbidden")










































"""
def query_empty_classroom(building_name):
   class_num = get_class()
   statistics("empty_classroom_query")
   if class_num == 1:
       result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class1 = False)
   elif class_num == 2:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class2 = False)
   elif class_num == 3:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class3 = False)
   elif class_num == 4:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class4 = False)
   elif class_num == 5:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class5 = False)
   elif class_num == 6:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class6 = False)
   elif class_num == 7:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class7 = False)
   elif class_num == 8:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class8 = False)
   elif class_num == 9:
        result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class9 = False)
   elif class_num == 10:
       result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class10 = False)
   else:
       result = EmptyClassroom.objects.filter(building_name = building_name, week = get_week(), day = get_day(), class11 = False)
   return result


def query_empty_classroom_weixin(building_name):
    result = query_empty_classroom(building_name)
    if len(result) == 0:
        return "没有查询到空教室信息"
    else:
        reply_str = "%s 第%s周，星期%s, 第%s节课\n"%(building_name, str(get_week()), str(get_day()), str(get_class()))
        for item in result:
            reply_str = reply_str + item.room_name + "\n"
        return reply_str

def query_empty_classroom_web(request, building_name):
    result = query_empty_classroom(building_name)
    if len(result) == 0:
        return render(request, "message.html", {"message":"没有查询到空教室的信息"})
    else:
        return render(request, "empty_classroom_query/query_result.html", {"result":result, \
                                                            "class":str(get_class()),\
                                                            "week":str(get_week()),\
                                                            "day":str(get_day())})






def import_info(request):
    f = open(r"e:\boyuan.csv", "r")
    for line in f.readlines():
        list = line.decode("GBK").split(",")
        for i in range(1, 14):
            list[i] = int(list[i])
        EmptyClassroom.objects.create(building_id = "1956", building_name = "博远楼", room_id = list[0][3:6], \
                                      room_name = list[0], class1 = list[1], class2 = list[2], class3 = list[3], \
                                      class4 = list[4], class5 = list[5], class6 = list[6], class7 = list[7], \
                                      class8 = list[8], class9 = list[9], class10 = list[10], class11 = list[11], \
                                      week = list[12], day = list[13])


def query_empty_classroom_index(request):
    return render(request, "empty_classroom_query/index.html")

    """