<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Stickum - Copy and Paste #${paste.id}</title>
</head>
<body>
    <div id="paste_${paste.id}" class="pasteview">
        <div class="paste_header">
            ${paste.lang=="None" and "P" or "%s code p" % paste.lang}asted @ ${paste.pasted_on.strftime("%H:%M")}
            on ${paste.pasted_on.strftime("%a, %d %b %y")}<br/>
            <a href="/paste/${paste.id}">Syntaxed up</a>
            <a href="/paste/${paste.id}/plain">Plain Text</a>
        </div>
        <table class="code_table" cellspacing="0" cellpadding="0">
            <tr py:for="i,line in enumerate(paste.formatted_lines)">
                <td id="L${i+1}" class="line_number ${(i+1)%10==0 and 'line_dec' or ''}">${i+1}</td>
                <td class="code_line"><pre><code>${XML(line)}</code></pre></td>
            </tr>
        </table>
    </div>
    <div id="edit" class="paste_zone">
    <form action="/paste/save" method="post">
        <div>
            <label for="lang">Syntax Highlighting:</label>
            <select name="lang">
                <option py:for="lang in languages" selected="${tg.selector(lang==paste.lang)}">${lang}</option>
            </select>
        </div>
        <div><textarea name="content" rows="20" cols="80" py:content="paste.content"></textarea></div>
        <div><input type="submit" name="submit" value="Paste it!"/></div>
    </form>
    </div>
</body>
</html>