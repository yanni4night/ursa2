#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
 render.py

 changelog
 2013-12-01[00:32:46]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.101,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''
from conf import C
import utils
from jinja2 import Template,Environment,FileSystemLoader,TemplateNotFound,TemplateSyntaxError

_template_dir=C('template_dir')

jinjaenv = Environment( loader=FileSystemLoader( utils.abspath(_template_dir),  C('encoding') , extensions=["jinja2.ext.do"] , autoescape=True )
build_jinjaenv = Environment( loader=FileSystemLoader( os.path.join( os.getcwd() , 'build', C('template_dir')) ,  C('encoding') ))


