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
# @todo https support,proxy support
#

from  BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from http import Request,Response
from route import Route
from conf import C,log
from handler import static,index,tpl,so

ursa_router=Route()
ursa_router.get(r'^/$',index)
ursa_router.get(r'\.%s$'%C('preview_ext'),tpl)
ursa_router.post(r'\.so$',so)
ursa_router.get(r'.*',static)

class UrsaHTTPRequestHandler(BaseHTTPRequestHandler):
    '''
    HTTP请求处理器
    '''

    def do_GET(self):
        '''
        处理GET请求
        '''
        ursa_router.distribute_request(self)

    def do_POST(self):
        '''
        todo:处理POST请求
        '''
        ursa_router.distribute_request(self)

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
    try:
        httpd=HTTPServer(server_addr,UrsaHTTPRequestHandler)
        log.info("Server listen on %d" %  port)
        httpd.serve_forever()
    except (KeyboardInterrupt , SystemExit):
        log.info("^C received, shutting down")
        httpd.socket.close()
    except socket.error:
        log.error('Maybe port ' + str(port) + ' already in use')
        log.error('You can try another port by use "ursa start 8234"')
        sys.exit(1)


if __name__ == '__main__':
    run()