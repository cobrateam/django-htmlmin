from lxml import html


def html_minify(html_code):
    dom = html.fromstring(html_code)
    return html.tostring(dom)
