from BeautifulSoup import BeautifulSoup, Comment
from util import force_decode

def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)

    soup = BeautifulSoup(html_code)

    if ignore_comments:
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]

    html_code = soup.prettify()
    script = False
    lines = html_code.split('\n')
    minified_lines = []

    last_line = '>'
    for line in lines:
        if '</script>' in line:
            script = False

        if script:
            minified_line = u"%s\n" % line.rstrip()
        else:
            minified_line = line.strip()

        minified_lines.append(str(minified_line))

        if not minified_line.startswith('<') and not last_line.endswith('>'):
            minified_lines.append(' ')

        if '<script' in line:
            script = True
            minified_lines.append('\n')

        last_line = minified_line


    content = "".join(minified_lines)

    if "DOCTYPE" not in content:
        content = "<!DOCTYPE html>%s" % content

    return content
