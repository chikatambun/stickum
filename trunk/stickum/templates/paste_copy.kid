<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Stickum - Copy and Paste #${paste.id}</title>
    <style type="text/css" py:content="highlightStyles" />
</head>
<body>
    <div id="paste_${paste.id}" class="pasteview">
        <div class="paste_header">
            ${paste.lang=="None" and "P" or "%s code p" % languagedict[paste.lang]}asted @ ${paste.pasted_on.strftime("%H:%M")}
            on ${paste.pasted_on.strftime("%a, %d %b %y")}<br/>
        <ul class="actions">
          <li class="first"><a href="${tg.url('/paste/%s' % paste.id)}">Syntaxed up</a></li>
          <li><a href="${tg.url('/paste/%s/plain' % paste.id)}">Plain Text</a></li>
        </ul>
      </div>
      ${XML(paste.formatted_lines)}
    </div>
    <div id="edit" class="paste_zone">
    <form action="${tg.url('/paste/save')}" method="post">
        <div>
            <label for="lang">Syntax Highlighting:</label>
            <select name="lang">
                <option py:for="lang in languages" value="${lang[0]}" selected="${tg.selector(lang[0]==paste.lang)}">${lang[1]}</option>
            </select>
        </div>
        <div><textarea name="content" rows="20" cols="80" py:content="paste.content"></textarea></div>
        <div><input type="submit" name="submit" value="Paste it!"/></div>
    </form>
    </div>
</body>
</html>
