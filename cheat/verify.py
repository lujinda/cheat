#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-12 20:43:58
# Filename        : verify.py
# Description     : 

import urlparse
from sheets import default_path
from config import host
from os.path import join
from utils import die
import urllib2
import json
import urllib

def save_user_token(user, token):
    path = join(default_path(), '.cheat_token')
    with open(path, 'w')  as fd_token:
        fd_token.write(user + '\n' + token)

def read_user_token():
    path = join(default_path(), '.cheat_token')
    with open(path, 'r') as fd_token:
        user, token = fd_token.readlines()
    return user.strip(), token.strip()

def user_pwd_is_true(user, pwd):
    url = urlparse.urljoin(host, 'login')
    post_data = dict(user=user, pwd=pwd) 
    req = urllib2.Request(url, 
            urllib.urlencode(post_data))
    try:
        request = urllib2.urlopen(req).read()
        return json.loads(request)
    except Exception,e :
        return None

def login_user():
    print 'Welcome to use the shared features, such as no account, please go to %s Register' % host
    user = raw_input('Please enter your username: ').strip()
    from getpass import getpass
    pwd = getpass().strip()
    request = user_pwd_is_true(user, pwd)
    if request['code'] ==0 and request['token']:
        save_user_token(user, request['token'])
    else:
        die(request['mess'])

def verify_user_token():
    try:
        user, token = read_user_token()
        url = urlparse.urljoin(host, 'verify_user_token')
        post_data = dict(user=user, token=token)
        req = urllib2.Request(url, urllib.urlencode(post_data))
        request = json.loads(urllib2.urlopen(req).read())
        if request['code'] == 0:
            return True
        print request['mess']
        return False
    except Exception, e:
        return False

def check_permissions():
    if not verify_user_token():
        return False
    return True

