import re
from lxml import html
from util import force_decode

def drop_comments(content):
    comment_regexes = re.compile('<!--(.|\s)*?-->')
    return comment_regexes.sub('', content)

def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)
    dom = html.fromstring(html_code)
    html_code = html.tostring(dom, method='html', encoding=unicode)

    script = False
    lines = html_code.split('\n')
    minified_lines = []

    for line in lines:
        if '</script>' in line:
            script = False

        if script:
            minified_line = u"%s\n" % line.rstrip()
        else:
            minified_line = line.strip()

        minified_lines.append(str(minified_line.encode('utf-8')))

        if '<script' in line:
            script = True
            minified_lines.append('\n')

    content = "".join(minified_lines)

    if "DOCTYPE" not in content:
        content = "<!DOCTYPE html>%s" % content

    if ignore_comments:
        content = drop_comments(content)

    return content
