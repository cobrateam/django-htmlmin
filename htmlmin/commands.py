import os
import sys
from htmlmin.minify import html_minify

my_dir = os.getcwd()

def main(args=sys.argv[1:]):
    filename = args[0]
    filename = os.path.join(my_dir, filename)

    content = ""
    with open(filename) as html_file:
        content = html_file.read()

    print html_minify(content)
