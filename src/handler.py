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
import json
from conf import C,log
from render import render,render_file
from replace import replace
from timestamp import html_link,html_script,all_url

mimetypes.init()
path=os.getcwd()


def _token(path):
    '''
    去除后缀，取得相对于模板目录的相对无扩展名路径
    '''
    tpl_token=re.sub(r'\.(%s|%s|%s)$'%(C('preview_ext'),'m',C('template_ext')),'',path)
    if tpl_token.startswith(os.path.sep):
        tpl_token=tpl_token[1:]
    return tpl_token


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
    tpl_token=_token(req.path)
    html=render(tpl_token)
    html=replace(html)
    html=html_script(html,'.')
    html=html_link(html,'.')
    html=all_url(html,'.')
    res.send(html)

def m(req,res):
    '''
    输出对应json数据
    '''
    tpl_token=_token(req.path)
    data=''
    json_path=os.path.join(C('data_dir'),tpl_token+".json")
    try:
        data=utils.readfile(json_path)
    except Exception, e:
        log.error('%s:%s'%(json_path,e))
    mgr_path=utils.abspath(os.path.join(os.path.dirname(sys.argv[0]),'../tpl','mgr.html'))
    html=render_file(mgr_path,{"name":tpl_token,"data":data},noEnvironment=True)
    res.send(html)

def so(req,res):
    '''
    保存json数据
    todo
    '''
    tpl_token=_token(req.param('tpl'))
    json_str=req.param('data')
    try:
        json_obj = json.loads(json_str)
        json_path = os.path.join(C('data_dir'),tpl_token+".json")
        utils.writeJSON(json_path,json_obj)
        res.redirect('/%s.%s'%(tpl_token,C('preview_ext')))
    except ValueError, e:
        res.send('<html><head>Error</head><body><pre>%s</pre><br/>is not a JSON,<a href="%s.m">rewrite</a></body></html>'%(json_str,tpl_token))
    except Exception,e:
        log.error('%s'%e)
        res.redirect('/%s.%s'%(tpl_token,C('preview_ext')))
    

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