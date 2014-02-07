#coding:utf-8
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OnlineShop.forms import ItemNumberForm, OrderForm
from OnlineShop.models import ItemInfo, Order, AddressInfo


def create_order(request, item_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    if request.method == "POST":
        try:
            item = ItemInfo.objects.get(id=item_id, status=True)
        except ItemInfo.DoesNotExist:
            raise Http404
        form = ItemNumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data["number"]
            if number > item.store_num or number < 0:
                return render(request, "message.html", {"action": "alert alert-info", "info": "购买数量错误"})
            return render(request, "OnlineShop/confirm_order.html", {"info": item,
                                                                     "number": number,
                                                                     "price": item.price * number})
        else:
            return render(request, "message.html", {"action": "alert alert-info", "info": "请填写数量"})

    else:
        raise Http404


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
            address_info = AddressInfo.objects.create(name=name, phone=phone, email=email, address=address)
            order = Order.objects.create(item_id=item_id, number=number, total_price=int(number) * item.price, user_name=request.user.user_name,
                                         address_info=address_info, remark=remark, status="-1")
            item.store_num -= int(number)
            item.save()
            response_json = {"status": "success", "redirect": "/online_shop/order/" + str(order.id)}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "表单数据错误，请检查所有填写项目！"}
            return HttpResponse(json.dumps(response_json))
    else:
        raise Http404


def item_page(request, item_id):
    try:
        info = ItemInfo.objects.get(id=item_id)
    except ItemInfo.DoesNotExist:
        raise Http404
    return render(request, "OnlineShop/item_page.html", {"info": info})


def order_info(request, order_id):
    try:
        info = Order.objects.get(user_name=request.user.user_name, id=order_id)
    except Order.DoesNotExist:
        raise Http404
    item_info = ItemInfo.objects.get(id=info.item_id)
    return render(request, "OnlineShop/order_info.html", {"order_info": order_info, "item_info": item_info})


def shop_index(request):
    return render(request, "OnlineShop/shop_index.html")

'''
@login_required(login_url="/login/")
def get_order(request):
    order = Order.objects.filter(user_name=request.user.user_name)
    return order


@login_required(login_url="/login/")
def order_management_index(request, status="all"):
    if not request.user.is_staff():
        return HttpResponse("权限错误")
    if status == "all":
        order = Order.objects.all()
        return order
    else:
        if not(status == "-1" or status == "0" or status == "1" or status == "2"):
            return HttpResponse("order status error")
        order = Order.objects.filter(status=status)
        return order


@login_required(login_url="/login/")
def order_status_management(request, order_id, status):
    try:
        order = Order.objects.get(id=int(order_id))
    except Order.DoesNotExist:
        raise Http404
    if not(status == "-1" or status == "0" or status == "1" or status == "2"):
        return HttpResponse("order status error")
    order.status = status
    order.save()
    ####################
    return HttpResponseRedirect("")

'''



