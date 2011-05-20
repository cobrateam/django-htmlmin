from lxml.html.clean import Cleaner
from util import force_decode

def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)

    cleaner = Cleaner(scripts=False, javascript=False, comments=ignore_comments, links=False, meta=False, page_structure=False, processing_instructions=False, embedded=False, frames=False, forms=False, annoying_tags=False, remove_unknown_tags=False, safe_attrs_only=False)
    html_code = cleaner.clean_html(html_code)

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

    return content
