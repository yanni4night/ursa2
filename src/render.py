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
from conf import C,log
import utils
import os
import json
from jinja2 import Template,Environment,FileSystemLoader,TemplateNotFound,TemplateSyntaxError

_template_dir = C('template_dir')

jinjaenv = Environment(loader=FileSystemLoader(utils.abspath(_template_dir),  C('encoding') ), extensions=["jinja2.ext.do"] , autoescape=True )
build_jinjaenv = Environment( loader=FileSystemLoader( os.path.join( os.getcwd() , 'build', _template_dir) ,  C('encoding') ))

def render_file(filename,data=None,noEnvironment=False):
    '''
    渲染文件
    '''
    if noEnvironment:
        body=Template(utils.readfile(filename))#这里应为绝对路径
    else:
        body = jinjaenv.get_template(filename)
    return body.render(data or {})

def render(token):
    '''
    查找数据文件依赖并渲染模板
    '''
    if token.startswith(os.path.sep):
        token = token[1:]
    json_filepath = utils.abspath(os.path.join(C('data_dir'),token+".json"))
    data = {}
    try:
        content = utils.readfile(json_filepath)
        content=re.sub('\/\*[\s\S]*?\*\/','',content)
        data = json.loads(content)
    except Exception, e:
        log.warn('%s:%s'%(json_filepath,e))

    multoken = token.split('/')
    data.update({'_token':token.replace('/','_')})
    data.update({'_folder':multoken[0]})
    data.update({'_subtoken':multoken[1] if len(multoken)>1 else ""})   
    tpl_path=token + "." + C('template_ext')
    return render_file( tpl_path,data)


if __name__ == '__main__':
    print render('index')
