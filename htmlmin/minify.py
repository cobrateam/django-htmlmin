from lxml import html
from util import force_decode

def filter_lines(lines):
    code_lines = []
    is_comment = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('<!--'):
            is_comment = True

        if not is_comment:
            code_lines.append(line)

        if stripped_line.endswith('-->'):
            is_comment = False

    return code_lines

def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)
    dom = html.fromstring(html_code)
    html_code = html.tostring(dom, method='html', encoding=unicode)

    script = False
    lines = html_code.split('\n')

    if ignore_comments:
        lines = filter_lines(lines)

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

    return content
