# -*- coding: utf-8 -*-

def force_decode(string, encoding="utf-8"):
    for c in (encoding, "utf-8", "latin-1"):
        try:
            return string.decode(c)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass

def between_two_tags(current_line, all_lines, index):
    if current_line and not current_line.startswith('<') and not all_lines[index-1].endswith('>'):
        return False
    return True
