# -*- coding=UTF-8 -*-
# Created at May 26 10:07 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')

import os
import httplib2
import requests
from BeautifulSoup import BeautifulSoup
from smart_qdu.const import RENREN_BASE_URL



class RenRen:
    def __init__(self):
        self.session = requests.Session()
        #cookie = open(COOKIR_PATH).read()
        #cookie = [x.strip() for x in cookie.split(';') if x]
        #cookie = map(lambda x: x.split('=', 1), cookie)
        #cookie = dict(cookie)
        cookie = None
        self.session.cookies = requests.utils.cookiejar_from_dict(cookie)

    def postStatus(self, text):
        soup = BeautifulSoup(self.session.get(RENREN_BASE_URL).content)
        form = soup.find('form')
        assert(form is not None)
        values = map(lambda x: (x['name'], x['value']), form.findAll('input', type='hidden'))
        data = {'status': text}
        data.update(dict(values))
        req = self.session.post(form['action'], data)
        return req

#renren = RenRen()
#renren.postStatus("Hello world,jisuhide a  hahahahahah ")