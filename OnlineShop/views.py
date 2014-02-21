#coding:utf-8
import json
#from sae.mail import EmailMessage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from Mail.models import Mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from OnlineShop.forms import ItemNumberForm, OrderForm
from OnlineShop.models import ItemInfo, Order, AddressInfo, STATUS_CHOICES


def create_order(request, item_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/?next=" + request.META.get('HTTP_REFERER', "/"))
    if request.method == "POST":
        try:
            item = ItemInfo.objects.get(id=item_id, status=True)
        except ItemInfo.DoesNotExist:
            raise Http404
        form = ItemNumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data["number"]
            if number > item.store_num or number <= 0:
                return render(request, "message.html", {"action": "alert alert-info", "info": "购买数量错误"})
            history_order = Order.objects.filter(user_name=request.user.user_name).order_by("-create_time")
            name = phone = address = ""
            if len(history_order):
                name = history_order[0].address_info.name
                phone = history_order[0].address_info.phone
                address = history_order[0].address_info.address
            return render(request, "OnlineShop/confirm_order.html", {"info": item,
                                                                     "number": number,
                                                                     "price": item.price * number,
                                                                     "name": name,
                                                                     "phone":phone,
                                                                     "address": address})
        else:
            return render(request, "message.html", {"action": "alert alert-info", "info": "请填写数量"})

    else:
        return HttpResponseRedirect("/online_shop/item/%s/" % item_id)


def submit_order(request, item_id, number):
    if not request.user.is_authenticated():
        response_json = {"status": "error", "content": "请先登录！"}
        return HttpResponse(json.dumps(response_json))
    if request.method == "POST":
        try:
            item = ItemInfo.objects.get(id=item_id, status=True)
        except ItemInfo.DoesNotExist:
            raise Http404
        form = OrderForm(request.POST)
        if form.is_valid():
            if int(number) > item.store_num or int(number) < 0:
                response_json = {"status": "error", "content": "购买数量错误！"}
                return HttpResponse(json.dumps(response_json))
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            remark = form.cleaned_data["remark"]
            #TO DO:
            #严格的验证手机号码和email
            if len(phone) != 11:
                response_json = {"status": "error", "content": "手机号码长度错误"}
                return HttpResponse(json.dumps(response_json))
            address_info = AddressInfo.objects.create(name=name, phone=phone, email=email, address=address)
            order = Order.objects.create(item_id=item_id, number=number, total_price=int(number) * item.price,
                                         user_name=request.user.user_name,
                                         address_info=address_info, remark=remark, status="-1")
            item.store_num -= int(number)
            item.save()
            '''
            m = EmailMessage()
            m.to = request.user.email
            m.subject = "提交订单成功！"
            m.html = "<p>尊敬的用户，您好！</p>您的订单我们已经收到，正在处理中。\
            详情请点击<a href='http://smartqdu.sinaapp.com/online_shop/order/%s/'>订单详情</a>。有问题可以直接回复。谢谢</p><p>感谢您的支持！</p>" % order.id
            m.smtp = ("smtp.sina.cn", 25, "smartqdu@sina.cn", "092122302asdf", False)
            m.send()
            '''
            content = "您好！您的订单我们已经收到，正在处理中。\
            详情请点击http://smartqdu.sinaapp.com/online_shop/order/%s/。开学后，我们会联系您。有问题可以直接回复。感谢您的支持！" % order.id
            Mail.objects.create(to_user=request.user.user_name, from_user="root", subject="您的订单提交成功", content=content)
            response_json = {"status": "success", "redirect": "/online_shop/order/success/"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "表单数据错误，请检查所有填写项目！"}
            return HttpResponse(json.dumps(response_json))
    else:
        raise Http404


def submit_order_success(request):
    return render(request, "message.html", {"action": "alert alert-info",
                                            "info": "提交订单成功，请等待处理！您可以到个人资料页查看。"})


def item_page(request, item_id):
    try:
        info = ItemInfo.objects.get(id=item_id)
    except ItemInfo.DoesNotExist:
        raise Http404
    if int(item_id) == 2:
        origin_price = 5
        number = 500
    if int(item_id) == 3:
        origin_price = 8
        number = 200
    return render(request, "OnlineShop/item_page.html", {"info": info, "origin_price": origin_price, "number": number})


@login_required(login_url="/login/")
def order_info(request, order_id):
    if request.user.is_staff is True:
        try:
            order_info = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404
    else:
        try:
            order_info = Order.objects.get(user_name=request.user.user_name, id=order_id)
        except Order.DoesNotExist:
            raise Http404
    item_info = ItemInfo.objects.get(id=order_info.item_id)
    for choice in STATUS_CHOICES:
        if order_info.status == choice[0]:
            order_info.status = choice[1]
    return render(request, "OnlineShop/order_info.html", {"order_info": order_info, "item_info": item_info})


def shop_index(request):
    return render(request, "OnlineShop/shop_index.html")


@login_required(login_url="/login/")
def order_management(request, page_num):
    if request.user.is_staff is True:
        order_info = Order.objects.order_by("-create_time")
        page_info = Paginator(order_info, 15)
        total_page = page_info.num_pages
        if int(page_num) > total_page:
            raise Http404
        order_list = []
        info = page_info.page(page_num)
        for item in info:
            order = {}
            item_info = ItemInfo.objects.get(id=item.item_id)
            for choice in STATUS_CHOICES:
                if item.status == choice[0]:
                    item.status = choice[1]
            order["item_name"] = item_info.name
            order['order_info'] = item
            order_list.append(order)
        return render(request, "OnlineShop/order_management.html", {"order": order_list,
                                                                    "page_num": str(page_num),
                                                                    "pre_page": str(int(page_num) - 1),
                                                                    "next_page": str(int(page_num) + 1),
                                                                    "total_page": str(total_page)})
    else:
        raise Http404


