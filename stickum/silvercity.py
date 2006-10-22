# -*- coding: utf-8 -*-
#
# Copyright (C) 2004-2006 Edgewall Software
# Copyright (C) 2004 Daniel Lundin <daniel@edgewall.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.
#
# Author: Daniel Lundin <daniel@edgewall.com>
# Modified for use in "Stickum" by: Lee McFadden <spleeman@gmail.com>

# Copyright (C) 2003-2006 Edgewall Software
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. The name of the author may not be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR `AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Syntax highlighting module, based on the SilverCity module.

Get it at: http://silvercity.sourceforge.net/
"""

import re
from StringIO import StringIO
import SilverCity

types = {
    'CSS':                      ('CSS', 3),
    'HTML':                     ('HyperText', 3, {'asp.default.language':1}),
    'XML':                      ('XML', 3),
    'JavaScript':               ('CPP', 3), # Kludgy.
    'ASP':                      ('HyperText', 3, {'asp.default.language':2}),
    'C++':                      ('CPP', 3),
    'Perl':                     ('Perl', 3),
    'PHP':                      ('HyperText', 3, {'asp.default.language':4}),
    #'text/x-psp':               ('HyperText', 3, {'asp.default.language':3}),
    'Python':                   ('Python', 3),
    'Ruby':                     ('Ruby', 3),
    'SQL':                      ('SQL', 3),
    'XSLT':                     ('XSLT', 3),
}

CRLF_RE = re.compile('\r$', re.MULTILINE)

def html_splitlines(lines):
    """Tracks open and close tags in lines of HTML text and yields lines that
    have no tags spanning more than one line."""
    open_tag_re = re.compile(r'<(\w+)(\s.*?)?[^/]?>')
    close_tag_re = re.compile(r'</(\w+)>')
    open_tags = []
    for line in lines:
        # Reopen tags still open from the previous line
        for tag in open_tags:
            line = tag.group(0) + line
        open_tags = []

        # Find all tags opened on this line
        for tag in open_tag_re.finditer(line):
            open_tags.append(tag)

        open_tags.reverse()

        # Find all tags closed on this line
        for ctag in close_tag_re.finditer(line):
            for otag in open_tags:
                if otag.group(1) == ctag.group(1):
                    open_tags.remove(otag)
                    break

        # Close all tags still open at the end of line, they'll get reopened at
        # the beginning of the next line
        for tag in open_tags:
            line += '</%s>' % tag.group(1)

        yield line
        
class SilverCityRenderer(object):
    """Syntax highlighting based on SilverCity."""

    expand_tabs = True

    def __init__(self):
        self._types = types

    def get_quality_ratio(self, mimetype):
        # Extend default MIME type to mode mappings with configured ones
        if not self._types:
            self._types = {}
            self._types.update(types)
        return self._types.get(mimetype, (None, 0))[1]

    def render(self, mimetype, content):
        try:
            typelang = self._types[mimetype]
            lang = typelang[0]
            module = getattr(SilverCity, lang)
            generator = getattr(module, lang + "HTMLGenerator")
            try:
                allprops = typelang[2]
                propset = SilverCity.PropertySet()
                for p in allprops.keys():
                    propset[p] = allprops[p]
            except IndexError:
                pass
        except (KeyError, AttributeError):
            err = "No SilverCity lexer found for mime-type '%s'." % mimetype
            raise Exception, err

        # SilverCity does not like unicode strings
        content = content.encode('utf-8')
        
        # SilverCity generates extra empty line against some types of
        # the line such as comment or #include with CRLF. So we
        # standardize to LF end-of-line style before call.
        content = CRLF_RE.sub('', content)

        buf = StringIO()
        generator().generate_html(buf, content)

        br_re = re.compile(r'<br\s*/?>$', re.MULTILINE)
        span_default_re = re.compile(r'<span class="\w+_default">(.*?)</span>',
                                     re.DOTALL)
        html = span_default_re.sub(r'\1', br_re.sub('', buf.getvalue()))
        
        # Convert the output back to a unicode string
        html = html.decode('utf-8')

        # SilverCity generates _way_ too many non-breaking spaces...
        # We don't need them anyway, so replace them by normal spaces
        return html.replace('&nbsp;', ' ')
