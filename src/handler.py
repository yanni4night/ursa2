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
from build import UrsaBuilder

mimetypes.init()

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
    tpl_ext=C('template_ext')
    tpls=utils.FileSearcher(r'\.%s$'%tpl_ext,tpl_dir).search()
    _tpls=[];

    try:
        visible_prog=re.compile(r"%s"%C('visible_tpls'))
    except Exception, e:
        log.error('[visible_tpls]%s'%e)
        visible_prog=None

    #下面循环用于去除扩展名
    #todo优化
    for e in tpls:
        if e.endswith('.'+tpl_ext):
            e=re.sub(r'\.%s'%tpl_ext,'',e)
        if visible_prog:
            if visible_prog.match(e):
                _tpls.append(e)
        else:
            _tpls.append(e);

    index_path=os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),'../tpl','index.html'))
    html=render_file(index_path,{"tpls":_tpls},noEnvironment=True)
    res.send(html)
def tpl(req,res):
    '''
    模板
    '''
    tpl_token=_token(req.path)
    html=render(tpl_token)
    if C('server_add_timestamp'):
        base_dir=os.path.join('.',os.path.dirname(req.path))
        html=html_script(html,base_dir)
        html=html_link(html,base_dir)
        html=all_url(html,base_dir)
    html=replace(html)
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
        res.send('<html><head><meta charset="'+C('encoding')+'"/><title>JSON Error</title></head><body><pre>%s</pre><br/>is not a JSON,<a href="%s.m">rewrite</a></body></html>'%(json_str,tpl_token))
    except Exception,e:
        log.error('%s'%e)
        res.redirect('/%s.%s'%(tpl_token,C('preview_ext')))
    

def static(req,res):
    '''
    static resource
    '''
    req.path=re.sub(r'^/+','/',req.path)
    o=urlparse(req.path)
    #取得绝对路径
    fd=utils.abspath(o.path)
    if os.path.isfile(fd):
        mime=mimetypes.guess_type(fd,False)
        content_type=mime[0] or 'text/plain'#default text
        try:
            headers={}
            #todo  custom defined
            if not re.match(utils.BINARY_CONTENT_TYPE_KEYWORDS,content_type,re.IGNORECASE):
                content=utils.readfile(fd)
                content=replace(content)
                #server_mode build css files in {static_dir}
                if C('server_mode') and fd.endswith('.css') and req.path.startswith('/'+C('static_dir')):
                    tmpfile=os.path.dirname(fd)+"/%s-%s"%(utils.getDate(),os.path.basename(fd))
                    try:
                        builder=UrsaBuilder(C('server_mode_compress'),False)
                        builder.build_css(fd,tmpfile)
                        content=utils.readfile(tmpfile)
                        content=replace(content)
                    except Exception, e:
                        log.error('[server_mode]%s'%e)
                    finally:
                        os.unlink(tmpfile)
                 #server_mode build js files in {static_dir}
                elif C('server_mode') and fd.endswith('.js') and req.path.startswith('/'+C('static_dir')):
                    tmpfile=os.path.dirname(fd)+"/%s-%s"%(utils.getDate(),os.path.basename(fd))
                    try:
                        builder=UrsaBuilder(C('server_mode_compress'),False)
                        builder.build_js(fd,tmpfile,os.path.join(C('static_dir'),C('js_dir')))
                        content=utils.readfile(tmpfile)
                    except Exception, e:
                        log.error('[server_mode]%s'%e)
                    finally:
                        os.unlink(tmpfile)
                elif C('server_add_timestamp') :
                    base_dir=os.path.dirname(fd)
                    content=html_link(content,base_dir)
                    content=html_script(content,base_dir)
                    content=all_url(content,base_dir)
                #http encoding header
                headers['Encoding']=C('encoding')
                headers['Cache-Control']='nocache'
            else:
                #binary files
                content=utils.readfile(fd,'rb')

            headers['Content-Type']=content_type
            res.send(content=content,headers=headers)
        except Exception, e:
            res.send(code=500,content='%s'%e)
            log.error(e)
    else:
        if os.path.exists(fd):
            res.send(code=403,content='Access %s is forbidden'%req.path)
        else:
            res.send(code=404,content="%s not found"%req.path)