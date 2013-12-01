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
import  logbook
from datetime import datetime
import time


logbook.set_datetime_format('local')
log=logbook.Logger('ursa2')

_last_read_time=0
_conf_cache={}
_MANIFEST_FILE='manifest.json'
#配置文件的缓存间隔，读取文件后此事件内不再读取,单位s
_MIN_CACHE_INTERVAL=1

_DEFAULT_PROJ='local'

_DEFAULT_ITEMS={
    'encoding':'utf-8',
    'timestamp_name':'t',
    'template_dir':'template',
    'data_dir':'_data',
    'module_dir':'_module',#under template_dir
    'common_dir':'_common',#under template_dir
    'build_dir':'build',
    'template_ext':'tpl',
    'preview_ext':'ut'
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
            log.error("%s is required" % _manifest_file)
    except Exception, e:
        log.error("%s" % e)
    _conf_cache=ret
    return ret

def C(key,proj=None,default_val=None):
    '''
    获取指定key的配置值，顺序为{proj:{}},{local:{}},{},_DEFAULT_ITEMS,_default_val
    '''
    global _DEFAULT_ITEMS,_DEFAULT_PROJ

    if type(key) not in (type(''),type(u'')):
        return None
    conf=_getConf()
    if conf is None:
        return None

    k=proj
    if proj is None:
        k=_DEFAULT_PROJ

    dic=conf.get(k)
    #proj 或local存在
    if type(dic)==type({}):
        if dic.get(key) is not None:
            return dic.get(key)
    if conf.get(key) is not None:
        return conf.get(key)
    else:
        return _DEFAULT_ITEMS.get(key) or default_val

if __name__=='__main__':
    print C('empty_prefix');
