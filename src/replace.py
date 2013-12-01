#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 replace.py

 changelog
 2013-12-01[11:42:20]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''

from conf import C,log
import re
import utils

def replace(content,proj=None):
    '''
    替换@@变量
    '''
    TM_TOKEN = '@tm:(.*?)@'
    DATE_TOKEN = '@date@';
    COMMON_TOKEN = r'@([\w\-\/\\]+?)@'
    

    iters = re.finditer( TM_TOKEN , content )
    for i in reversed(list(iters)):
        content = content[0:i.start(0)] + utils.getFileTimeStamp(i.group(1) , filepath) + content[i.end(0):]

    iters = re.finditer( DATE_TOKEN , content )
    for i in reversed(list(iters)):
        content = content[0:i.start(0)] + utils.getDate()  + content[i.end(0):]

    iters = re.finditer( COMMON_TOKEN , content )

    for i in reversed(list(iters)):
        #config = conf.getConfig()
        name = i.group(1)
        value = C(name,proj)
        if value:
            if value.find('{num}') != -1:
                num = C('num',proj) or '10'
                num = range(num+1)
                substr100 = content[i.end(0):i.end(0)+100]
                istimestamp = substr100.find('t=')
                if istimestamp != -1:#has timestamp
                    try:
                        tm = int(substr100[istimestamp+2:istimestamp+3])
                    except ValueError:
                        continue
                    if tm >= len(num):
                        tm = tm - len(num)
                    value = value.replace( '{num}' , str(tm) )
                else:
                    global range_item
                    value = value.replace( '{num}' , str(num[range_item]) )
                    range_item = range_item + 1
                    if range_item >= len(num):
                        range_item = 0
            content = content[0:i.start(0)] + value + content[i.end(0):]
    return content