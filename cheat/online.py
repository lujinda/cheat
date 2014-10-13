#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-13 21:56:47
# Filename        : cheat/online.py
# Description     : 

from cheat.sheet import read
from cheat.utils import die
import urllib2, urllib
import urlparse
from config import host
import json

class OnLine:
    def __init__(self, user, token):
        self.user = user
        self.token = token

    def update_sheet(self, sheet):
        url = urlparse.urljoin(host, 'update_sheet')
        content  = read(sheet, is_share=True)
        if not content:
            return 

        post_data = dict(sheet=sheet, token=self.token,
                content=content, user=self.user)
        req = urllib2.Request(url, urllib.urlencode(post_data))
        try:
            result = urllib2.urlopen(req).read()
            result = json.loads(result)
            if int(result['code']) % 2 == 1:
                die(result['mess'])
            return result 
        except Exception, e:
            return None

        
