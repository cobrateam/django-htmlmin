# -*- coding: utf-8 -*-
'''
File: pico_django.py
Description: Code based on snippet available here: https://github.com/readevalprint/mini-django/blob/master/pico_django.py
'''

from django.http import HttpResponse
from django.conf.urls.defaults import patterns
DEBUG=True
ROOT_URLCONF = 'pico_django'
DATABASES = { 'default': {} }

CONTENT = '''
<html>
    <body>
        <p>Hello world! :D</p>
        <div>Copyright 3000</div>
    </body>
</html>
    '''

def minified(request, name):
    return HttpResponse(CONTENT)

def raw():
    return HttpResponse(CONTENT)

urlpatterns = patterns('', (r'^/?$', minified))
