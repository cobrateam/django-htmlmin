# -*- coding: utf-8 -*-
'''
File: pico_django.py
Description: Code based on snippet available here: https://github.com/readevalprint/mini-django/blob/master/pico_django.py
'''

from django.http import HttpResponse
from django.conf.urls.defaults import patterns
from htmlmin.decorators import minified_response, not_minified_response

CONTENT = '''
<html>
    <body>
        <p>Hello world! :D</p>
        <div>Copyright 3000</div>
    </body>
</html>
    '''

@minified_response
def minified(request):
    return HttpResponse(CONTENT)

@not_minified_response
def not_minified(request):
    return HttpResponse(CONTENT)

def raw(request):
    return HttpResponse(CONTENT)

urlpatterns = patterns('',
    (r'^min$', minified),
    (r'^raw$', raw),
    (r'^not_min$', not_minified))
