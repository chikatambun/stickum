<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
<title>Stickum - New</title>
</head>
<body>
    <div class="paste_zone central">
    <p><strong>Instructions:</strong> Type or Paste.  Click "Paste it!". It's that simple. :)</p>
    <form action="${tg.url('/paste/save')}" method="post">
        <div>
            <label for="lang">Syntax Highlighting:</label>
            <select name="lang">
                <option py:for="lang in languages" value="${lang[0]}">${lang[1]}</option>
            </select>
        </div>
        <div><textarea name="content" rows="20" cols="80"></textarea></div>
        <div><input type="submit" name="submit" value="Paste it!"/></div>
    </form>
    </div>

</body>
</html>
