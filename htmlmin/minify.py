from lxml import html
from util import force_decode

def html_minify(html_code):
    html_code = force_decode(html_code)
    dom = html.fromstring(html_code)
    html_code = html.tostring(dom, method='html', encoding=unicode)

    script = False
    minified_lines = []
    for line in html_code.split('\n'):
        if '</script>' in line:
            script = False

        if script:
            minified_line = u"%s\n" % line.rstrip()
        else:
            minified_line = line.strip()

        minified_lines.append(str(minified_line.encode('utf-8')))

        if '<script' in line:
            script = True
            first = True
            minified_lines.append('\n')

    return "".join(minified_lines)
