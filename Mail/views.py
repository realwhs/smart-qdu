#coding:utf-8

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from Account.models import Passport
from Mail.forms import MailForm
from Mail.models import Mail


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
            except Passport.DoseNotExist:
                response_json = {"status": "error", "content": "收件人账号不存在！"}
                return HttpResponse(json.dumps(response_json))
            Mail.objects.create(to_user=to_user, from_user=request.user.user_name, subject=subject, content=content)
            response_json = {"status": "success", "redirect": "/mail/"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": "表单数据错误！"}
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
    return render(request, "Mail/mail_index.html", {"received": received, "sent": sent})


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