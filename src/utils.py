#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 utils.py

 changelog
 2013-11-30[14:36:11]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''

import time
import os
import json
import re
import hashlib
import codecs
from conf import C,log

BINARY_CONTENT_TYPE_KEYWORDS=r'(image|video|flash|audio|powerpoint|msword)'

def isInt(v):
    '''
    type int
    '''
    return type(v) == type(1)

def isStr(s):
    '''
    type string
    '''
    return type(s) in (type(u''),type(''))

def isDict(d):
    '''
    type dict
    '''
    return type(d) == type({})

def isList(d):
    '''
    type list
    '''
    return type(d) == type([])

def isTuple(t):
    '''
    type tuple
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
    get the absolute path of a file/directory in the current working directory
    '''
    if not isStr(path):
        raise TypeError('path must be a string')
    if os.path.isabs(path):
        path=path[1:]
    return os.path.abspath(os.path.join(os.getcwd(),path))

def readfile(filename  , mode='r'):
    '''
    get the content of a file
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
    write conent to a file
    '''
    try:
        f = codecs.open(filename , 'w' , C('encoding'))
        f.write(content)
        f.close()
    except:
        log.error("write to %s failed" % filename)
        raise

def writeJSON(filename,data):
    '''
    write file in JSON
    '''
    writefile(filename, json.dumps(data , sort_keys = True , indent = 4, separators = ( ',' , ': ')) )

def dorepeat(data):
    '''
    to be checked
    '''
    if type(data)==type({}):
        for item in data.keys():
            dorepeat(data[item])
            if re.search( '@\d+$' , item ):
                name = item.split('@')[0]
                times = item.split('@')[1]
                
                if int(times):
                    for time in range(int(times)):
                        if not data.get(name):
                            data[name] = []
                        data[name].append(data[item])
def md5toInt(md5):
    """将md5得到的字符串变化为6位数字传回。
    基本算法是将得到的32位字符串切分成两部分，每部分按16进制得整数后除997，求得的余数相加
    最终得到6位
    
    Arguments:
    - `md5`:
    """
    md5 = [ md5[:16] , md5[16:] ]
    result = ''
    for item in md5:
        num = str( int( item , 16 ) % 997 ).zfill(3)
        result = result+num
        
    return result

def getFileTimeStamp(fpath):
    '''
    绝对路径
    '''
    try:
        f = readfile(fpath , 'rb')
        m = hashlib.md5()
        m.update(f)
        md5 = md5toInt(m.hexdigest())
        return md5
    except Exception,e:
        log.error('[TimeStamp]%s'%e)
    return ''

def getDate():
    '''
    to be checked
    '''
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

class FileSearcher(object):
    '''
    搜索一个目录下所有符合规定文件名的文件,
    默认返回相对于初始目录的相对路径
    '''
    result=[]
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
            if os.path.isfile(fpath) and self.regexp.findall(fname):
                if self.relative:
                    fpath=os.path.relpath(fpath,self.start_dir)
                self.result.append(fpath)

if __name__ == '__main__':
    print FileSearcher(r'.+','build/server',relative=False).search()