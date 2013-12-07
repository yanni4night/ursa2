#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 main.py

 changelog
 2013-11-30[00:21:29]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/bin
 @author yinyong#sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''

from conf  import log,C
from docopt import docopt
from __init__ import __version__ as version
import sys,os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def run():
    '''
    ursa2

    Usage:
        ursa2 init
        ursa2 start [<port>]
        ursa2 build [<target>] [-ch]
        ursa2 help
        ursa2 (-v | --version)
    
    Options:
        -c --compress    compress js and css when building.
        -h --html            creating HTML when building.
        -v --version        show version.
    '''
    argv=docopt(run.__doc__,version=version)
    if argv.get('init'):
        #todo
        print 'coming'
    elif argv.get('start'):
        server=__import__('server')
        server.run(argv.get('<port>'))
    elif argv.get('build'):
        build=__import__('build')
        builder=build.UrsaBuilder(argv.get('--compress'),argv.get('--html'),argv.get('<target>'))
        builder.build();
    elif argv.get('help'):
        print 'https://github.com/yanni4night/ursa2/wiki'


if __name__=='__main__':
    run();