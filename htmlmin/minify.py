import re
from BeautifulSoup import BeautifulSoup, Comment
from util import force_decode

SCRIPT_PATTERN = '############ script %d ############'

def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)
    soup = BeautifulSoup(html_code)

    scripts = [ str(script) for script in soup.findAll(name='script') if len(script.text) > 0 ]

    for index, script in enumerate(scripts):
        html_code = html_code.replace(script, SCRIPT_PATTERN % index)

    soup = BeautifulSoup(html_code)

    if ignore_comments:
        [ comment.extract() for comment in soup.findAll(text=lambda text:isinstance(text, Comment)) ]

    html_code = str(soup)
    lines = html_code.split('\n')
    minified_lines = []
    last_line = '<>'

    for index, line in enumerate(lines):
        minified_line = line.strip()
        minified_lines.append(str(minified_line))

    content = "".join(minified_lines)

    for index, script in enumerate(scripts):
        content = content.replace(SCRIPT_PATTERN % index, script)

    if "DOCTYPE" not in content:
        content = "<!DOCTYPE html>%s" % content

    return content
