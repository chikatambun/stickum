import logging

import cherrypy
from cherrypy import NotFound

import turbogears
from turbogears import controllers, expose, validate, redirect
from turbogears import view
from turbogears.database import session

from urllib import urlopen
from stickum import json, model
from sqlalchemy import func

from datetime import datetime

from pygments.formatters import HtmlFormatter

from turbogears.i18n import gettext

log = logging.getLogger("stickum.controllers")

def my_providers(vars):    
    vars['paste_count'] = model.Paste.get_count()
    vars['sloganizer'] = urlopen("http://www.sloganizer.net/en/outbound.php?slogan=Stickum").read()    
view.variable_providers.append(my_providers)

class PasteController(controllers.Controller):
    
    @expose()
    def index(self, *args, **kw):
        raise redirect("/")
        
    @expose()
    def save(self, content, lang, submit):
        paste = model.Paste()
        paste.content = content
        paste.lang = lang
        paste.pasted_on = datetime.now()
        paste.flush()
        raise redirect(turbogears.url("/paste/%d" % paste.id))
            
    @expose()
    def save_cli(self, content, lang, submit):
        paste = model.Paste()
        paste.content = content
        paste.lang = lang
        paste.pasted_on = datetime.now()
        paste.flush()
        url_root = "http://paste.turbogears.org"
        paste_url = turbogears.url("/paste/%d" % paste.id)
        return "%s%s" % (url_root, paste_url)

    @expose()
    def default(self, id, action="view", *args, **kw):
        try:
            id = int(id)
        except ValueError:
            raise NotFound
        paste = model.Paste.get(id)
        handler = "on_%s" % action
        if paste and hasattr(self, handler):
            return getattr(self, handler)(paste)
        raise NotFound
        
    def on_view(self, paste):
        latest = model.Paste.get_latest()
        template = ".templates.paste_view"
        return dict(tg_template=template,
                    latest=latest,
                    paste=paste,
                    languages=Root.languages,
                    highlightStyles=Root.highlightStyles)
                    
    def on_plain(self, paste):
        # Output text/plain version of the paste.
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return paste.content
                    
    def on_copy(self, paste):
        template = ".templates.paste_copy"
        return dict(tg_template=template,
                    paste=paste,
                    languages=Root.languages,
                    highlightStyles=Root.highlightStyles)
        
        

class Root(controllers.RootController):

    formatter = HtmlFormatter(linenos='table', style="trac")
    highlightStyles = formatter.get_style_defs()

    paste = PasteController()
    languages = { 'apacheconf' : 'ApacheConf',
                  'bbcode' : 'BBCode',
                  'bash' : 'Bash',
                  'bat' : 'Batchfile',
                  'befunge' : 'Befunge',
                  'boo' : 'Boo',
                  'brainfuck' : 'Brainfuck',
                  'c' : 'C',
                  'csharp' : 'C#',
                  'cpp' : 'C++',
                  'css+django' : 'CSS+Django/Jinja',
                  'css+erb' : 'CSS+Ruby',
                  'css+genshitext' : 'CSS+Genshi Text',
                  'css' : 'CSS',
                  'css+php' : 'CSS+PHP',
                  'css+smarty' : 'CSS+Smarty',
                  'd' : 'D',
                  'delphi' : 'Delphi',
                  'diff' : 'Diff',
                  'django' : 'Django/Jinja',
                  'dylan' : 'DylanLexer',
                  'erb' : 'ERB',
                  'genshi' : 'Genshi',
                  'genshitext' : 'Genshi Text',
                  'groff' : 'Groff',
                  'haskell' : 'Haskell',
                  'html+django' : 'HTML+Django/Jinja',
                  'html+genshi' : 'HTML+Genshi',
                  'html' : 'HTML',
                  'html+php' : 'HTML+PHP',
                  'html+smarty' : 'HTML+Smarty',
                  'ini' : 'INI',
                  'irc' : 'IRC logs',
                  'java' : 'Java',
                  'js+django' : 'JavaScript+Django/Jinja',
                  'js+erb' : 'JavaScript+Ruby',
                  'js+genshitext' : 'JavaScript+Genshi Text',
                  'js' : 'JavaScript',
                  'js+php' : 'JavaScript+PHP',
                  'js+smarty' : 'JavaScript+Smarty',
                  'jsp' : 'Java Server Page',
                  'lua' : 'Lua',
                  'make' : 'Makefile',
                  'css+mako' : 'CSS+Mako',
                  'html+mako' : 'HTML+Mako',
                  'js+mako' : 'JavaScript+Mako',
                  'mako' : 'Mako',
                  'xml+mako' : 'XML+Mako',
                  'minid' : 'MiniD',
                  'trac-wiki' : 'MoinMoin/Trac Wiki markup',
                  'mupad' : 'MuPAD',
                  'css+myghty' : 'CSS+Myghty',
                  'html+myghty' : 'HTML+Myghty',
                  'js+myghty' : 'JavaScript+Myghty',
                  'myghty' : 'Myghty',
                  'xml+myghty' : 'XML+Myghty',
                  'objective-c' : 'Objective-C',
                  'ocaml' : 'OCaml',
                  'perl' : 'Perl',
                  'php' : 'PHP',
                  'pycon' : 'Python console session',
                  'python' : 'Python',
                  'pytb' : 'Python Traceback',
                  'raw' : 'Raw token data',
                  'redcode' : 'Redcode',
                  'rhtml' : 'RHTML',
                  'rst' : 'reStructuredText',
                  'rbcon' : 'Ruby irb session',
                  'rb' : 'Ruby',
                  'scheme' : 'Scheme',
                  'smarty' : 'Smarty',
                  'sourceslist' : 'Debian Sourcelist',
                  'sql' : 'SQL',
                  'tex' : 'TeX',
                  'text' : 'Text only',
                  'vb.net' : 'VB.net',
                  'vim' : 'VimL',
                  'xml+django' : 'XML+Django/Jinja',
                  'xml+erb' : 'XML+Ruby',
                  'xml' : 'XML',
                  'xml+php' : 'XML+PHP',
                  'xml+smarty' : 'XML+Smarty', }
    
    @expose(template="stickum.templates.index")
    def index(self):
        latest = model.Paste.get_latest()
        return dict(latest=latest, languages=self.languages)
        
    @expose()
    def secret_paste_count(self):
        return _("There have been %d pastes!") % model.Paste.get_count()
