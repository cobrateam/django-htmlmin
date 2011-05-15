from lxml import html

def html_minify(html_code):
    html_code = unicode(html_code)
    dom = html.fromstring(html_code)
    html_code = html.tostring(dom, method='xml', encoding=unicode)

    script = False
    minified_lines = []
    for line in html_code.split('\n'):
        if '</script>' in line:
            script = False

        if script:
            minified_line = "%s\n" % line.rstrip()
        else:
            minified_line = line.strip()

        minified_lines.append(minified_line)

        if '<script' in line:
            script = True
            first = True
            minified_lines.append('\n')

    return u"".join(minified_lines)
