#coding:utf-8

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from Account.models import Passport
from Mail.forms import MailForm
from Mail.models import Mail
from django.core.paginator import Paginator


def send_mail(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/?next=" + request.META.get('HTTP_REFERER', "/"))
    if request.method == "POST":
        form = MailForm(request.POST)
        if form.is_valid():
            to_user = form.cleaned_data["to_user"]
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            try:
                Passport.objects.get(user_name=to_user)
            except Passport.DoesNotExist:
                response_json = {"status": "error", "content": "收件人账号不存在啊，这个发给谁呢~~"}
                return HttpResponse(json.dumps(response_json))
            Mail.objects.create(to_user=to_user, from_user=request.user.user_name, subject=subject, content=content)
            response_json = {"status": "success", "redirect": "/mail/"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "表单数据错误，看看你是不是全填上了~"}
            return HttpResponse(json.dumps(response_json))
    else:
        raise Http404


@login_required(login_url="/login/")
def read_mail(request, mail_id):
    try:
        received_msg = Mail.objects.get(id=mail_id, to_user=request.user.user_name)
    except Mail.DoesNotExist:
        try:
            sent_msg = Mail.objects.get(id=mail_id, from_user=request.user.user_name)
        except Mail.DoesNotExist:
            raise Http404
        msg_type = "sent"
        return render(request, "Mail/mail_detail.html", {"type": msg_type, "info": sent_msg})
    msg_type = "received"
    received_msg.status = True
    received_msg.save()
    return render(request, "Mail/mail_detail.html", {"type": msg_type, "info": received_msg})


@login_required(login_url="/login/")
def mail_index(request):
    received = Mail.objects.filter(to_user=request.user.user_name).order_by("-create_time")
    sent = Mail.objects.filter(from_user=request.user.user_name).order_by("-create_time")
    return render(request, "Mail/mail_index.html", {"received": received[0:15], "sent": sent[0:10]})


@login_required(login_url="/login/")
def mail_page(request, mail_type, page_num):
    if not(mail_type == "received" or mail_type == "sent"):
        raise Http404
    if mail_type == "received":
        received = Mail.objects.filter(to_user=request.user.user_name).order_by("-create_time")
        page_info = Paginator(received, 15)
        total_page = page_info.num_pages
        if int(page_num) > total_page:
            raise Http404
        return render(request, "Mail/mail_page.html", {"type": "received",
                                                       "info": page_info.page(page_num),
                                                       "total_page": str(total_page),
                                                       "pre_page": str(int(page_num) - 1),
                                                       "page_num": str(page_num),
                                                       "next_page": str(int(page_num) + 1)})
    else:
        sent = Mail.objects.filter(from_user=request.user.user_name).order_by("-create_time")
        page_info = Paginator(sent, 15)
        total_page = page_info.num_pages
        if int(page_num) > total_page:
            raise Http404
        return render(request, "Mail/mail_page.html", {"type": "sent",
                                                       "info": page_info.page(page_num),
                                                       "total_page": str(total_page),
                                                       "pre_page": str(int(page_num) - 1),
                                                       "page_num": str(page_num),
                                                       "next_page": str(int(page_num) + 1)})


@login_required(login_url="/login/")
def send_mail_index(request):
    to_user = request.GET.get("to_user", "")
    reply = request.GET.get("reply", "")
    return render(request, "Mail/send_mail.html", {"to_user": to_user, "reply": reply})


def get_mail_status(request):
    if request.user.is_authenticated():
        mail = Mail.objects.filter(to_user=request.user.user_name, status=False)
        if len(mail):
            response_json = {"status": "new_mail"}
        else:
            response_json = {"status": "no_new_mail"}
    else:
        response_json = {"status": "no_new_mail"}
    return HttpResponse(json.dumps(response_json))