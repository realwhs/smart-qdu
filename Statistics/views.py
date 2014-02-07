#coding:utf-8
import datetime
from Statistics.models import Statistics


def statistics(type):
    try:
        Statistics.objects.get(date=datetime.date.today)
    except Statistics.DoesNotExist:
        Statistics.objects.create(date=datetime.date.today, empty_classroom_query_number=0, message_received_number=0, \
                                  auto_reply_number=0, subscribe_number=0, unsubscribe_number=0)
        
    s = Statistics.objects.get(date=datetime.date.today)
    if type == "empty_classroom_query":
        s.empty_classroom_query_number += 1
        s.save()
    elif type == "message_received":
        s.message_received_number += 1
        s.save()
    elif type == "subscribe":
        s.subscribe_number += 1
        s.save()
    elif type == "unsubscribe":
        s.unsubscribe_number += 1
        s.save()
    elif type == "menu_click":
        s.menu_click += 1
        s.save()
    else:
        s.auto_reply_number += 1
        s.save()

        
