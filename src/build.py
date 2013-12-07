#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
 build.py

 changelog
 2013-12-07[12:01:09]:created

 @info yinyong,osx-x64,UTF-8,192.168.1.104,py,/Users/yinyong/work/ursa2/src
 @author yinyong@sogou-inc.com
 @version 0.0.1
 @since 0.0.1
'''

from conf import C,log
import shutil
import os
import re
import sys
import subprocess
import utils
from render import render
from exception import ConfigurationError,DirectoryError
from replace import replace
from timestamp import html_link,html_script,all_url

RJS_PATH = utils.abspath(os.path.join(os.path.dirname(sys.argv[0]),'../assets','r.js'))
YC_PATH = utils.abspath(os.path.join(os.path.dirname(sys.argv[0]),'../assets',C('yuicompressor')))

class UrsaBuilder(object):
    '''
    build project:
    copy and handle static resources
    generate html with json data
    '''
    @classmethod
    def __init__(self,compress,html,target=None):
        '''
        '''
        self._compress=compress
        self._generate_html=html
        self._target=target
        self._tpl_dir=C('template_dir')
        self._build_dir=C('build_dir')
        self._static_dir=C('static_dir')
        self._js_dir=C('js_dir')
        self._css_dir=C('css_dir')

        #check dunplicated
        if os.path.relpath(self._build_dir,self._tpl_dir) == '.':
            raise ConfigurationError('template_dir and build_dir are dumplicated')
        elif os.path.relpath(self._build_dir,self._static_dir)=='.':
            raise ConfigurationError('template_dir and static_dir are dumplicated');

        self._build_static_dir=os.path.join(self._build_dir,self._static_dir)
        self._build_css_dir=os.path.join(self._build_static_dir,self._css_dir)
        self._build_js_dir=os.path.join(self._build_static_dir,self._js_dir)
        self._build_tpl_dir=os.path.join(self._build_dir,self._tpl_dir)

        self._build_html_dir=os.path.join(self._build_dir,C('html_dir'))

    @classmethod
    def build(self):
        '''
        do build
        '''
        self._check();
        self._dir();
        self._less();
        self._css();
        self._js();
        self._tpl();
        if self._generate_html:
            self._html();

    @classmethod
    def _check(self):
        '''
        '''
        require_dirs=[self._tpl_dir,self._static_dir];
        for d in require_dirs:
            if not os.path.exists(d):
                raise DirectoryError('Ursa project requires %s directory'%d)
    @classmethod
    def _dir(self):
        '''
        handle build dir
        '''
        shutil.rmtree(self._build_dir,True)
        os.mkdir(self._build_dir);
        shutil.copytree(self._static_dir,self._build_static_dir)
        shutil.copytree(self._tpl_dir,self._build_tpl_dir)

    @classmethod
    def _less(self):
        '''
        handle less files to css

        @todo
        to be supported
        '''

    @classmethod
    def _css(self):
        '''
        handle css
        '''
        css_modules=C('require_css_modules')
        if not utils.isList(css_modules):
            css_modules=['main']

        for css in css_modules:
            if not utils.isStr(css):
                continue;
            if css.startswith('/'):
                css=css[1:]
            if not css.endswith('.css'):
                css+='.css'
            css_realpath=os.path.join(self._build_css_dir,css)
            subprocess.call('node %s -o cssIn=%s out=%s'%(RJS_PATH,css_realpath,css_realpath),shell=True)
            #repalce
            content=utils.readfile(css_realpath)
            #timestamp
            content=all_url(content,os.path.dirname(css_realpath))
            content=replace(content,self._target)
            utils.writefile(css_realpath,content)
            if self._compress:
                subprocess.call( 'java -jar ' + YC_PATH + ' --type css --charset ' + C('encoding') + ' ' + css_realpath + ' -o ' + css_realpath , shell=True )

    @classmethod
    def _js(self):
        '''
        handle js
        '''
        js_modules=C('require_modules') or C('require_js_modules')
        if not utils.isList(js_modules):
            js_modules=['main']

        for js in js_modules:
            if not utils.isStr(js):
                continue;
            if js.startswith('/'):
                js=js[1:]
            if not js.endswith('.js'):
                js+='.js'
            js_realpath=os.path.join(self._build_js_dir,js)
            subprocess.call( 'node ' + RJS_PATH +' -o name=' + js[0:-3] + ' out='+ js_realpath + ' optimize=none baseUrl='\
             + self._build_js_dir , shell=True)
            #repalce
            content=utils.readfile(js_realpath)
            content=replace(content,self._target)
            utils.writefile(js_realpath,content)
            if self._compress:
                subprocess.call( 'java -jar ' + YC_PATH + ' --type js --charset ' + C('encoding') + ' ' + js_realpath + ' -o ' + js_realpath , shell=True )
    @classmethod
    def _tpl(self):
        '''
        handle tempaltes
        '''
        fs=utils.FileSearcher(r'\.%s$'%C('template_ext'),self._build_tpl_dir,relative=False)
        tpls=fs.search()
        for tpl in tpls:
            content = utils.readfile(tpl)
            content = html_link(content,'.')#模板的静态资源相对目录应该写死为cwd
            content = html_script(content,'.')
            content = all_url(content,'.')
            content = replace(content,self._target)
            utils.writefile(tpl,content)
    @classmethod
    def _html(self):
        '''
        generate html
        '''
        fs=utils.FileSearcher(r'\.%s$'%C('template_ext'),self._build_tpl_dir)
        tpls=fs.search()
        for tpl in tpls:
            html = render(tpl[0:-4])
            target_dir= os.path.join(self._build_html_dir,os.path.dirname(tpl))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            dst_file=re.sub(r'\.tpl$','.html',os.path.join(self._build_html_dir,tpl))
            utils.writefile(dst_file,html)

if __name__ == '__main__':
    builder=UrsaBuilder(True,True,'online')
    builder.build();