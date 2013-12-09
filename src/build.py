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

from conf import C,log,BASE_DIR
import shutil
import os
import re
import sys
import subprocess
import mimetypes
import utils
from render import render
from exception import ConfigurationError,DirectoryError
from replace import replace
from timestamp import html_link,html_script,all_url

RJS_PATH = os.path.join(BASE_DIR,'../assets','r.js')
RPL_PATH = os.path.join(BASE_DIR,'../assets','rpl.js')
YC_PATH = os.path.join(BASE_DIR,'../assets',C('yuicompressor'))

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
        self._compile_dir=C('compile_folder') or ''#copy and repalce

        #check dunplicated
        if os.path.relpath(self._build_dir,self._tpl_dir) == '.':
            raise ConfigurationError('template_dir and build_dir are dumplicated')
        elif os.path.relpath(self._build_dir,self._static_dir)=='.':
            raise ConfigurationError('template_dir and static_dir are dumplicated')
        elif self._compile_dir and os.path.relpath(self._compile_dir,self._static_dir) == '.':
            raise ConfigurationError('compile_dir and static_dir are dunplicated')
        elif self._compile_dir and os.path.relpath(self._compile_dir,self._build_dir) == '.':
            raise ConfigurationError('compile_dir and build_dir are dunplicated')
        elif self._compile_dir and os.path.relpath(self._compile_dir,self._tpl_dir) == '.':
            raise ConfigurationError('compile_dir and tpl_dir are dunplicated')

        self._build_static_dir=os.path.join(self._build_dir,self._static_dir)
        self._build_css_dir=os.path.join(self._build_static_dir,self._css_dir,C('css_folder') or '')
        self._build_js_dir=os.path.join(self._build_static_dir,self._js_dir,C('js_folder') or '')
        self._build_tpl_dir=os.path.join(self._build_dir,self._tpl_dir)
        self._build_compile_dir=os.path.join(self._build_dir,self._compile_dir)

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

        if self._compile_dir:
            shutil.copytree(self._compile_dir,self._build_compile_dir)

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
        all_css_files=utils.FileSearcher(r'\.css$',self._build_css_dir,relative=False).search()

        #replace and timsstamp all css files
        for dst in all_css_files:
            content=utils.readfile(dst)
            #timestamp
            content=all_url(content,os.path.dirname(dst))
            content=replace(content,self._target)
            utils.writefile(dst,content)


        css_modules=C('require_css_modules')
        if not utils.isList(css_modules):
            css_modules=['main']

        for css in css_modules:
            if not utils.isStr(css):
                continue;
            css = re.sub(r'\/*','',css)
            if not css.endswith('.css'):
                css+='.css'
            css_realpath=os.path.join(self._build_css_dir,css)
            self.build_css(css_realpath,css_realpath)
            continue

    @classmethod
    def build_css(self,src,dst):
        '''
        handle one css src to dst
        '''
        subprocess.call('node %s -o cssIn=%s out=%s'%(RJS_PATH,src,dst),shell=True)
        if self._compress:
            subprocess.call( 'java -jar ' + YC_PATH + ' --type css --charset ' + C('encoding') + ' ' + dst + ' -o ' + dst , shell=True )

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
            self.build_js(js_realpath,js_realpath,self._build_js_dir)

    @classmethod
    def build_js(self,src,dst,base_dir):
        '''
        handle one js src to dst
        '''
        js=os.path.relpath(src,base_dir)
        subprocess.call( 'node ' + RJS_PATH +' -o name=' + js[0:-3] + ' out='+ dst + ' optimize=none baseUrl='\
            + base_dir , shell=True)
        #repalce
        content=utils.readfile(dst)
        content=replace(content,self._target)
        utils.writefile(dst,content)
        if C('js_ascii_only'):
            subprocess.call( 'node ' + RPL_PATH +' '+dst+' '+dst,shell=True)
        if self._compress:
            subprocess.call( 'java -jar ' + YC_PATH + ' --type js --charset ' + C('encoding') + ' ' + dst + ' -o ' + dst , shell=True )
                
    @classmethod
    def _tpl(self):
        '''
        handle tempaltes
        '''
        fs=utils.FileSearcher(r'\.%s$'%C('template_ext'),self._build_tpl_dir,relative=False)
        tpls=fs.search()
        nfs=utils.FileSearcher(r'.+',self._build_compile_dir,relative=False)
        compile_files=nfs.search()
        for f in compile_files:
            mime=mimetypes.guess_type(f,False)
            content_type=mime[0] or 'text/plain'
            if not re.match(utils.BINARY_CONTENT_TYPE_KEYWORDS,content_type,re.I):
                tpls.insert(0,f)

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
            try:
                html = render(re.sub(r'\.%s$'%C('template_ext'),'',tpl),build=True)
                target_dir= os.path.join(self._build_html_dir,os.path.dirname(tpl))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                dst_file=re.sub(r'\.tpl$','.html',os.path.join(self._build_html_dir,tpl))
                utils.writefile(dst_file,html)
            except Exception,e:
                if not C('html_force_output'):
                    raise e
                else:
                    log.error(e)


if __name__ == '__main__':
    builder=UrsaBuilder(True,True,'online')
    builder._dir();
    builder._css();