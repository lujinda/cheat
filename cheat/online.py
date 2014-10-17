#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-16 19:19:57
# Filename        : cheat/online.py
# Description     : 

from cheat.sheet import read
from cheat.utils import die, warn
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
        
        return self.__request_post(url, post_data)
        

    def list_user_sheets(self, user):
        url = urlparse.urljoin(host, 'list_user_sheets') + '?user=%s' % user
        return self.__request_get(url)

    def __request_post(self, url, post_data):
        req = urllib2.Request(url, urllib.urlencode(post_data))
        try:
            result = urllib2.urlopen(req).read()
            result = json.loads(result)
            code = int(result['code'])
            if code % 2 == 1 and code >= 500:
                die(result['mess'])
            return result 
        except Exception, e:
            warn('modify fails')
            return None


    def __request_get(self, url):
        req = urllib2.Request(url)
        try:
            result = urllib2.urlopen(req).read()
            result = json.loads(result)
            return result
        except Exception, e:
            warn('get fails')
            return None
            
    def read_user_sheet(self, user, sheet):
        url = urlparse.urljoin(host, 'read_user_sheet') + '?' + \
                urllib.urlencode(dict(user=user, sheet=sheet))
        return self.__request_get(url)

    def remove_user_sheet(self, sheet):
        url = urlparse.urljoin(host, 'remove_user_sheet')
        post_data = dict(user=self.user, sheet=sheet, 
                token=self.token)
        return self.__request_post(url, post_data)

    def search_other_sheets(self, sheet, num=1):
        url = urlparse.urljoin(host, 
                'search_other_sheets') + '?' + \
                urllib.urlencode(dict(user=self.user, sheet=sheet, num=num))
        return self.__request_get(url)
        
