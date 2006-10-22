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

log = logging.getLogger("stickum.controllers")

def my_providers(vars):    
    vars['sloganizer'] = urlopen("http://www.sloganizer.net/en/outbound.php?slogan=Stickum").read()
    vars['paste_count'] = model.Paste.get_count()
    
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
        raise redirect("/paste/%d" % paste.id)
            
        
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
                    paste=paste)
                    
    def on_plain(self, paste):
        # Output text/plain version of the paste.
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return paste.content
                    
    def on_copy(self, paste):
        template = ".templates.paste_copy"
        return dict(tg_template=template,
                    paste=paste,
                    languages=Root.langs)
        
        

class Root(controllers.RootController):

    paste = PasteController()
    langs = ["Python",
            "HTML",
            "CSS",
            "JavaScript",
            "SQL",
            "XML",
            "ASP",
            "C++",
            "Perl",
            "PHP",
            "Ruby",
            "XSLT",
            "None"]
    
    @expose(template="stickum.templates.index")
    def index(self):
        latest = model.Paste.get_latest()

        return dict(latest=latest, languages=self.langs)
        
    @expose()
    def secret_paste_count(self):
        return "There have been %d pastes!" % model.Paste.get_count()
