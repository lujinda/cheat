#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-17 12:08:00
# Filename        : cheat/share.py
# Description     : 
from cmd import Cmd
import sys
from cheat.online import OnLine
from cheat.utils import die, colorize
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
        result = self.online.update_sheet(sheet)
        if result:
            print result['mess']
        
    def do_exit(self, arg):
        """退出程序"""
        print 
        sys.exit()

    def do_list(self, arg):
        """list [user] 列出某个用户分享的笔记列表"""
        user = arg or self.online.user
        self.__list_user_sheets(user)

    def do_remove(self, sheet):
        """remove sheet 取消指定的共享命令笔记"""
        result = self.online.remove_user_sheet(sheet)
        if result:
            print result['mess']

    def do_search(self, arg):
        """search sheet [num] 搜索命令的相关笔记， num指定结果数，最大不允许超过3"""
        sheet, num = (arg.split(' ', 1) + ['1'])[:2]
        if not sheet or not num.isdigit() \
                or int(num) >3:
            self.do_help(sheet)
            return None
        
        result = self.online.search_other_sheets(sheet, num)
        if result:
            print '\n\n*******next******\n\n'.join(result['mess'])


    def do_read(self, arg):
        """read [user] sheet 查看某个用户的某个命令笔记"""
        if not arg:
            self.do_help(arg)
            return None

        user, sheet = (arg.split(' ', 1) + [''])[:2]
        if not sheet: # 如果只输入了一个参数，则表示是要查看自己的sheet，则把第一个参数当sheet
            user, sheet = self.online.user, user
        self.__read_user_sheet(user, sheet)

    def __list_user_sheets(self, user=''):
        result = self.online.list_user_sheets(user)
        for i, sheet in enumerate(result['mess']):
            print sheet + '\t',
            if (i+1) % 3 ==0:
                print
        print 

    def __read_user_sheet(self,user='' ,sheet=''):
        result = self.online.read_user_sheet(user, sheet)
        if not result:
            return
        print colorize(result['mess'])
    
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
    
