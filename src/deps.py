#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 deps.py

 changelog
 2013-12-02[15:48:27]:created

 @info yinyong,osx-x64,UTF-8,10.129.173.95,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
import re
import utils
import os
from conf import C,log

class DepsFinder(object):
    '''
    '''
    @classmethod
    def __init__(self,tpl):
        '''
        tpl:模板，相对于template_dir目录
        '''
        self._result=[]
        #x=>x.tpl
        if not tpl.endswith('.%s'%C('template_ext')):
            tpl+='.%s'%C('template_ext')
        self._tpl=tpl
        self._history={};
        self._pattern=re.compile(r'\{%\s*(include|extends)\s+([\'"])([\w\/\\\.-]+\.tpl)\2\s*%\}',re.I|re.M)

    @classmethod
    def _search(self,tpl):
        '''
        递归搜索
        '''
        try:
            #/x.tpl=>x.tpl
            if tpl.startswith('/'):
                tpl=tpl[1:]
            abspath=utils.abspath(os.path.join(C('template_dir'),tpl))
            
            if self._history.get(abspath) is not None:
                return
            else:
                self._result.append(tpl)
                self._history[abspath]=1


            content=utils.readfile(abspath)
            iters=re.finditer(self._pattern,content)

            for i in reversed(list(iters)):
                self._search(i.group(3))


        except Exception, e:
            log.error(e)

    @classmethod
    def find(self):
        '''
        获取依赖的接口
        '''
        self._search(self._tpl)
        return self._result;

    @classmethod
    def get_tpl():
        '''
        '''
        return self._tpl

if __name__ == '__main__':
    df=DepsFinder(u'/test/index')
    print df.find()
