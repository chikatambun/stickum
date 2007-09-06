<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Viewing paste #${paste.id}</title>
    <style type="text/css" py:content="highlightStyles" />
  </head>
  <body>
    
    <div id="paste_${paste.id}" class="pasteview">
        <div class="paste_header">
            ${paste.lang=="None" and "P" or "%s code p" % languagedict[paste.lang]}asted @ ${paste.pasted_on.strftime("%H:%M")}
            on ${paste.pasted_on.strftime("%a, %d %b %y")}<br/>
        <ul class="actions">
          <li class="first"><a href="${tg.url('/paste/%s/copy#edit' % paste.id)}">Copy &amp; Paste</a></li>
          <li><a href="${tg.url('/paste/%s/plain' % paste.id)}">Plain Text</a></li>
        </ul>
        </div>
        ${XML(paste.formatted_lines)}
    </div>
  </body>
</html>
