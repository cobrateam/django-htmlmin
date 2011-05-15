from lxml import html

def html_minify(html_code):
    html_code = unicode(html_code)
    dom = html.fromstring(html_code)
    html_code = html.tostring(dom, method='xml', encoding=unicode)

    minified_lines = []
    for line in html_code.split('\n'):
        minified_line = line.strip()
        if minified_line:
            minified_lines.append(minified_line)

    return u"".join(minified_lines)
