#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 conf.py

 changelog
 2013-11-29[14:38:24]:created
 2013-11-30[15:39:31]:finished
 2013-12-01[19:23:17]:empty string supported

 @info yinyong,osx-x64,UTF-8,10.129.164.117,py,/Users/yinyong/work/ursa2
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
import os
import json
import re
import logging
from datetime import datetime
import time

logger = log = logging

#配置缓存
_last_read_time=0
_conf_cache={}

_MANIFEST_FILE='manifest.json'
#配置文件的缓存间隔，读取文件后此事件内不再读取,单位s
_MIN_CACHE_INTERVAL=1

_DEFAULT_TARGET='local'
#ursa2 Python源文件目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 

#默认配置选项
_DEFAULT_ITEMS={
    'encoding':'utf-8',
    'http_port':8000,#http 端口
    'log_level':'debug',#日子级别
    'timestamp_name':'t',#时间戳参数名
    'log_http_request':False,#是否打印HTTP请求日志
    'template_dir':'template',
    'data_dir':'_data',#JSON数据目录
    'module_dir':'_module',#under template_dir
    'common_dir':'_common',#under template_dir
    'static_dir':"static",#静态资源目录
    'css_dir':"css",#under static_dir
    'js_dir':"js",#under static_dir
    'build_dir':'build',
    'html_dir':'html',#under build_dir
    'template_ext':'tpl',
    'preview_ext':'ut',#实时访问渲染后模板的URL后缀
    'num':10,#随机变量的最大值
    'max_readable_filesize':1024*1024,
    'yuicompressor':'yuicompressor-2.4.8.jar',#yuicompressor的文件名，方便升降级
    'js_ascii_only':False#转义中文为ASCII
};


def _getConf():
    '''
    获取配置文件中整个json对象
    '''
    #缓存
    global _last_read_time,_MIN_CACHE_INTERVAL,_conf_cache
    now=time.time()
    if now-_last_read_time<_MIN_CACHE_INTERVAL:
        _last_read_time=now
        return _conf_cache

    ret=None
    try:
        path=os.getcwd()
        conffile = os.path.join(path , _MANIFEST_FILE)
        if os.path.exists(conffile):
            f = open(conffile)
            body = f.read()
            f.close()
            #去除/**/注释，支持多行
            #todo，字符串中应该予以保留
            ret=json.loads(re.sub('\/\*[\s\S]*?\*\/','',body))
        else:
            log.error("%s is required" % _MANIFEST_FILE)
    except Exception, e:
        log.error("%s" % e)
    _conf_cache=ret
    return ret

def C(key,target=None,default_val=None):
    '''
    获取指定key的配置值，顺序为{target:{}},{local:{}},{},_DEFAULT_ITEMS,_default_val
    '''
    global _DEFAULT_ITEMS,_DEFAULT_TARGET

    if type(key) not in (type(''),type(u'')):
        return None
    conf=_getConf()
    if conf is None:
        return _DEFAULT_ITEMS.get(key) or default_val

    k=target
    if target is None:
        k=_DEFAULT_TARGET

    dic=conf.get(k)
    #target 或local存在
    if type(dic)==type({}):
        if dic.get(key) is not None:
            return dic.get(key)
    if conf.get(key) is not None:
        return conf.get(key)
    else:
        return _DEFAULT_ITEMS.get(key) or default_val

#日子级别设置
__illegal_log_levels={'info':logger.INFO,'debug':logger.DEBUG,'warn':logger.WARNING,'error':logger.ERROR,'critical':logger.CRITICAL}
__log_level = C('log_level')
if __illegal_log_levels.get(__log_level) is not None:
    log.basicConfig(level=__illegal_log_levels.get(__log_level))
else:
    log.basicConfig(level=__illegal_log_levels.get('info'))

if __name__=='__main__':
    print C('template_dir');
