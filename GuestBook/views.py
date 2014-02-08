#coding:utf-8
import json
from django.shortcuts import render
from GuestBook.models import Message
from GuestBook.forms import MessageForm
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse


def guest_book_page(request, page_num):
    message = Message.objects.all()
    page_info = Paginator(message, 30)
    total_page = page_info.num_pages
    if int(page_num) > total_page:
        raise Http404
    return render(request, "GuestBook/page.html", {"info": page_info.page(page_num),
                                                   "current_page_num": str(page_num),
                                                   "prev_page_num": str(page_num - 1),
                                                   "next_page_num": str(page_num + 1)})


def leave_message(request):
    if request.Method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            Message.objects.create(name=name, email=email, title=title, content=content)
            response_json = {"status": "success", "content": "发表成功"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "表单数据错误"}
            return HttpResponse(json.dumps(response_json))
    else:
        raise Http404