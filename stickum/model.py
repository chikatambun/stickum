from sqlalchemy import *
from sqlalchemy.ext.assignmapper import assign_mapper

from turbogears.database import metadata, session

from datetime import datetime

from stickum.util import Parser

from cStringIO import StringIO

from stickum.silvercity import html_splitlines, SilverCityRenderer

import cgi

paste_table = Table("pastes", metadata,
    Column("id", Integer, primary_key=True),
    Column("pasted_on", DateTime, default=datetime.now()),
    Column("lang", String(50), default="Python"),
    Column("content", Unicode),
    Column("formatted_content", Unicode)
)

setting_table = Table("settings", metadata,
    Column("name", String(50), primary_key=True),
    Column("data", PickleType)
)

class Paste(object):
    
    @classmethod
    def get_latest(self):
        limit = Setting.get("latest_limit")
        if not limit:
            # Set a reasonable default
            limit = Setting()
            limit.name = "latest_limit"
            limit.data = 10
            limit.flush()
        return Paste.select(order_by=desc("pasted_on"), limit=limit.data)
        
    @classmethod
    def get_count(self):
        return select([func.count(paste_table.c.id)]).scalar()
        
    def _get_formatted_content(self):
        if not self._formatted_content:
            if not self.lang == "None":                
                self._formatted_content = SilverCityRenderer().render(self.lang, self.content)
                self.flush()
            else:
                self._formatted_content = cgi.escape(self.content)
                self.flush()
        return self._formatted_content

        
    def _set_formatted_content(self, content):
        self._formatted_content = content
    
    formatted_content = property(_get_formatted_content, _set_formatted_content)
    
    def _get_formatted_lines(self):
        return html_splitlines(self.formatted_content.splitlines())
    formatted_lines = property(_get_formatted_lines)
        
    
class Setting(object):
    pass
    
assign_mapper(session.context, Paste, paste_table,
    properties={
        "_formatted_content": paste_table.c.formatted_content
    }
)
assign_mapper(session.context, Setting, setting_table)