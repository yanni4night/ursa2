#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 route.py

 changelog
 2013-11-30[18:52:47]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
from http import Request,Response
import re
from urlparse import urlparse

class Route(object):
    '''
    路由器
    '''
    handlers=[];

    @classmethod
    def distribute_request(self,http_req_handler):
        '''
        根据URL匹配规则路由请求到相应地处理器
        '''
        path=urlparse(http_req_handler.path).path
        for h in self.handlers:
            if 'ALL' == h.get('method') or h.get('method') == http_req_handler.command and re.findall(h.get('pattern'),path):
                ret=(h.get('handler'))(Request(http_req_handler),Response(http_req_handler))
                if True == ret:
                    continue
                else:
                    break


    @classmethod
    def get(self,pattern,handler):
        '''
        注册GET请求处理器
        '''
        self._register(pattern,handler,'GET')

    @classmethod
    def post(self,pattern,handler):
        '''
        注册POST请求处理器
        '''
        self._register(pattern,handler,'POST')

    @classmethod
    def all(self,pattern,handler):
        '''
        同时注册POST与GET请求处理器
        '''
        self._register(pattern,handler,'ALL')

    @classmethod
    def _register(self,pattern,handler,method):
        '''
        注册路由控制器
        '''
        self.handlers.append({'pattern':pattern,'handler':handler,'method':method})