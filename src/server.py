#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# server.py
#
# changelog
# 2013-11-30[17:37:42]:created
#
# @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
# @author yinyong@sogou-inc.com
# @version 0.0.1
# @since 0.0.1
#

from  BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from urlparse import urlparse
import os
import mimetypes

from utils import log

mimetypes.init()
path=os.getcwd()

class UrsaHTTPRequestHandler(BaseHTTPRequestHandler):
    '''
    HTTP请求处理器
    '''
    def do_GET(self):
        '''
        处理GET请求
        '''
        o=urlparse(self.path)
        fd=os.path.join(path,o.path[1:])

        if os.path.isfile(fd):
            mime=mimetypes.guess_type(fd,False)
            mode='rb'
            if mime[1] is not None or 'text' in mime[0]:
                mode='r'
            try:
                f=open(fd,mode)
                content=f.read()
                self.send_response(200)
                if mime[0] is not None:
                    self.send_header('Content-Type',mime[0])
                if mime[1] is not None:
                    self.send_header('Encoding',mime[1])
                self.end_headers()

                self.wfile.write(content)
                self.wfile.close()
            except Exception, e:
                self.send_response(500)
        else:
            self.send_response(404,"%s"%fd)

    def do_POST(self):
        '''
        todo:处理POST请求
        '''
        noop()

    @classmethod
    def version_string(self):
        '''
        服务器名字
        '''
        return 'Ursa2'


def run(port=8000):
    '''
    服务器启动入口
    '''
    server_addr=('',port);
    s=HTTPServer(server_addr,UrsaHTTPRequestHandler)
    log.info("Server listen on %d" %  port)
    s.serve_forever()


if __name__ == '__main__':
    run()