#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
'''
 handler.py

 changelog
 2013-11-30[22:32:36]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
import utils
import mimetypes
from urlparse import urlparse
import os
import sys
import re
from conf import C,log
from render import render,render_file

mimetypes.init()
path=os.getcwd()

def index(req,res):
    '''
    模板列表
    '''
    tpl_dir=C('template_dir')
    tpls=utils.FileSearcher(r'\.%s$'%C('template_ext'),tpl_dir).search()
    _tpls=[];
    for e in tpls:
        if e.endswith('.'+C('template_ext')):
            e=re.sub(r'\.%s'%C('template_ext'),'',e)
        _tpls.append(e)
    index_path=utils.abspath(os.path.join(os.path.dirname(sys.argv[0]),'../tpl','index.html'))
    html=render_file(index_path,{"tpls":_tpls},noEnvironment=True)
    res.send(html)
def tpl(req,res):
    '''
    模板
    '''
    tpl_token=re.sub(r'\.%s$'%C('preview_ext'),'',req.path)
    if tpl_token.startswith(os.path.sep):
        tpl_token=tpl_token[1:]
    html=render(tpl_token)
    res.send(html)

def so(req,res):
    '''
    保存json数据
    todo
    '''
    res.redirect('/')

def static(req,res):
    '''
    静态资源
    '''
    o=urlparse(req.path)
    fd=os.path.join(path,o.path[1:])
    if os.path.isfile(fd):
        mime=mimetypes.guess_type(fd,False)
        try:
            #静态资源一律使用rb读取
            f=open(fd,'rb')
            content=f.read()
            headers={}
            if mime[0] is not None:
                headers['Content-Type']=mime[0]
            if mime[1] is not None:
                headers['Encoding']=mime[1]
            res.send(content=content,headers=headers)
        except Exception, e:
            res.send(code=500,content='Server Failed')
    else:
        res.send(code=404,content="%s not found"%req.path)