#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# conf.py
#
# changelog
# 2013-11-29[14:38:24]:created
#
# @info yinyong,osx-x64,UTF-8,10.129.164.117,py,/Users/yinyong/work/ursa2
# @author yinyong#sogou-inc.com
# @version 0.0.1
# @since 0.0.1
#
import os
import json
import re

_last_read_time=0
_manifest_file='manifest.json'


_default_items={
    'encoding':'utf-8',
    'template':'./template'
};

def _getConf():
    '''
    获取配置文件中json对象
    '''
    ret={}
    try:
        path=os.getcwd()
        conffile = os.path.join(path , _manifest_file)
        if os.path.exists(conffile):
            f = open(conffile)
            body = f.read()
            f.close()
            ret=json.loads(re.sub('\/\*[\s\S]*?\*\/','',body))
        else:
            print "%s is required" % _manifest_file
    except ValueError,e:
        print "No valid JSON in %s" % _manifest_file
    except Exception, e:
        noop
    return ret

def get(key,proj,default_val=None):
    '''
    获取指定key的配置值，顺序为{proj:{}},{local:{}},{}
    '''

if __name__=='__main__':
    print _getConf();
