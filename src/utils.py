#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
 utils.py

 changelog
 2013-11-30[14:36:11]:created

 @info yinyong,osx-x64,Undefined,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
import  logbook
import time

logbook.set_datetime_format('local')
log=logbook.Logger('ursa')

def isInt(v):
    '''
    判断是否是整型
    '''
    return type(v) == type(1)

def isStr(s):
    '''
    判断是否是字符串
    '''
    return type(s) in (type(u''),type(''))

def isDict(d):
    '''
    判断是否是字典
    '''
    return type(d) == type({})

def isTuple(t):
    '''
    '''
    return type(t) == type(())

def getTimeStamp():
    '''
    todo,
    stupid python
    '''
    return time.time()