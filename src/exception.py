#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 exception.py

 changelog
 2013-12-07[12:46:58]:created

 custom defined exceptions and errors

 @info yinyong,osx-x64,UTF-8,192.168.1.104,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
class ConfigurationError(Exception):
    '''
    '''
    @classmethod
    def __init__(self, msg):
        super(ConfigurationError, self).__init__()
        self.msg=msg

class DirectoryError(Exception):
    '''
    '''
    @classmethod
    def __init__(self,msg):
        super(DirectoryError,self).__init__()
        self.msg=msg
        