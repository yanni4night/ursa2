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

from uitls  import log
from conf  import $
from docopt import docopt
from __init__ import __version__ as version

def run():
    '''
    ursa2

    Usage:
        ursa2 start [<port>]
        ursa2 build [<proj>] [-ch]
        ursa2 help
        ursa2 (-v | --version)
    
    Options:
        -c --compress    compress js and css when building.
        -h --html            creating HTML when building.
        -v --version        show version.
    '''
    log.info('Hello World from logbook')
    argv=docopt(run.__doc__,version=version)
    print argv


if __name__=='__main__':
    run();