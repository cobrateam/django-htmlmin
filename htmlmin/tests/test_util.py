# -*- coding: utf-8 -*-
import unittest
from htmlmin.util import force_decode

class TestUtil(unittest.TestCase):

    def test_should_decode_a_utf8_string(self):
        string = "Blá blá"
        self.assertEqual(u"Blá blá", force_decode(string))

    def test_shoulde_decode_a_latin_string(self):
        unicode_object = "Blá blá".decode("utf-8").encode("latin-1")
        string = str(unicode_object)
        self.assertEqual(u"Blá blá", force_decode(string))
