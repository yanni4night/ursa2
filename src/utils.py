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

import time
import os
import re
import codecs
from conf import C,log


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

def abspath(path):
    '''
    返回相对于当前目录的目录文件的绝对路径
    '''
    return os.path.abspath(os.path.join(os.getcwd(),path))

def readfile(filename  , mode='r'):
    '''
    '''
    try:
        if 'b' in mode:#Binary file
            f = open( filename , mode )
        else:
            f = codecs.open(filename , mode ,C('encoding'))
    
        body = f.read()
        f.close()
        return body
    except Exception,e:
        raise

def writefile(filename , content):
    '''
    '''
    try:
        f = codecs.open(filename , 'w' , C('encoding'))
        f.write(content)
        f.close()
    except:
        log.error("write to %s failed" % filename)
        raise

class FileSearcher(object):
    '''
    搜索一个目录下所有符合规定文件名的文件,
    默认返回相对于初始目录的相对路径
    '''
    @classmethod
    def __init__(self, pattern=r'.+', start_dir='.',relative=True,traverse=True):
        '''
        pattern:文件名的正则过滤表达式;
        start_dir:搜索目录;
        relative:是否输出相对目录;
        traverse:是否遍历目录搜索
        '''
        self.regexp = re.compile(pattern)
        self.start_dir = start_dir
        self.result=[]
        self.relative=relative
        self.traverse=traverse
    @classmethod
    def search(self):
        '''
        执行搜索输出
        '''
        if os.path.isdir(self.start_dir):
            os.path.walk(self.start_dir,self._visit,None)
        else:
            log.warn('you are walking a non-dir %s'%self.start_dir)

        return self.result

    @classmethod
    def _visit(self,argv, directoryName,filesInDirectory):
        '''
        '''
        for fname in filesInDirectory:                   
            fpath = os.path.join(directoryName, fname)
            if os.path.isfile(fpath) and self.regexp.findall(fpath):
                if self.relative:
                    fpath=os.path.relpath(fpath,self.start_dir)
                self.result.append(fpath)
            elif os.path.isdir(fpath) and self.traverse:
                os.path.walk(fpath,self._visit,None)

if __name__ == '__main__':
    fs=FileSearcher(r'java$','/Users/yinyong/work/src/main/java/')
    print fs.search()