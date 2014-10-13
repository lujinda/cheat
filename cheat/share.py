#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-13 21:54:19
# Filename        : cheat/share.py
# Description     : 
from cmd import Cmd
from cheat.utils import warn
import sys
from cheat.online import OnLine
from verify import check_permissions, login_user, read_user_token


class ShareClient(Cmd):
    prompt = '> '
    def __init__(self):
        if not check_permissions():
            login_user()
        self.online = OnLine(*read_user_token())
        Cmd.__init__(self)

    def do_update(self, sheet):
        """提交命令笔记"""
        if not self.online.update_sheet(sheet):
            warn('updated faile')

    def do_exit(self, arg):
        """退出程序"""
        print 
        sys.exit()

    def do_help(self, arg):
        """显示这个帮助"""
        for obj in dir(self):
            if not obj.startswith('do_'):
                continue
            func = getattr(self, obj, None)
            if callable(func):
                print obj[3:] + ':\t\t' + func.__doc__
    
def start_share():
    share_client = ShareClient()
    share_client.cmdloop()
    
