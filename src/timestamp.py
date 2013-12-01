#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 timestamp.py

 changelog
 2013-12-01[15:59:50]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
from conf import C,log
import re
import utils
import os
from replace import replace
from urlparse import urlparse,parse_qs

def _addtimestamp(content,reg,base_dir):
    '''
    '''
    iters=re.finditer(reg,content)
    t=C('timestamp_name')
    for it in reversed(list(iters)):
        start = content[0:it.start(1)]
        url = it.group(3)
        end = content[it.end(1):]
        local_url = replace(url)
        parsed_url = urlparse(local_url,False)
        parsed_query = parse_qs(parsed_url.query)
        #已经有时间戳的不再添加
        #带协议的不再添加
        if parsed_query.get(t):
            log.warn("%s has a timestamp"%local_url)
            continue
        elif parsed_url.scheme  or local_url.startswith('//'):
            log.warn("%s has a scheme"%local_url)
            continue

        timestamp=utils.getFileTimeStamp(os.path.join(base_dir,parsed_url.path[1:]))

        new_query=parsed_url.query
        if '' == new_query:
            new_query=t+"="+timestamp
        else:
            new_query+='&%s=%s'%(t,timestamp)
        if '' == parsed_url.fragment:
            new_fragment=''
        else:
            new_fragment='#'+parsed_url.fragment

        if not parsed_url.scheme:
            new_scheme = ''
        else:
            new_scheme=parsed_url.scheme+"://"

        new_url=new_scheme+parsed_url.netloc+parsed_url.path+'?'+new_query+new_fragment
        content=start+'"'+new_url+'"'+end

    return content

def html_link(content,base_dir):
    '''
    '''
    return _addtimestamp(content,r'<link.* href=(([\'"])(.*?\.css.*?)\2)',base_dir)

def html_script(content,base_dir):
    '''
    '''
    #return re.sub(r'<script.* src=([\'"])(.*?\.js.*?)\1',_addtimestamp,content)
    return _addtimestamp(content,r'<script.* src=(([\'"])(.*?\.js.*?)\2)',base_dir)

def all_url(content,base_dir):
    '''
    '''
    return _addtimestamp(content,r'url\((([\'"])?(.*?)\2?)\)',base_dir)