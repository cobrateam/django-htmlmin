# -*- coding: utf-8 -*-

def force_decode(string, encoding="utf-8"):
    for c in (encoding, "utf-8", "latin-1"):
        try:
            return string.decode(c)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
