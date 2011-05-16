# -*- coding: utf-8 -*-

def force_decode(string):
    for c in ("utf-8", "latin-1"):
        try:
            return string.decode(c)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
