#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 setup.py

 changelog
 2013-11-30[00:06:29]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''

from setuptools import setup, find_packages
from src.__init__ import __version__ as version


setup(
    name = "ursa2",
    version = version,
    packages = ['src'],
    install_requires = ['docopt>=0.6.1'],

    package_data = {
    },
    author = "yanni4night",
    author_email = "yinyong@sogou-inc.com",
    description = "2nd of ursa ,as a FE enviroment",
    license = "PSF",
    keywords = "ursa,fe",
    url = "http://github.com/yanni4night/ursa2",
    entry_points = {
        'console_scripts':[
            'ursa2=src.main:run'
            ]
        }
)