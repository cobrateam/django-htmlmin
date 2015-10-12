# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

EXCLUDE_FROM_MINIFYING = ('^raw',)

DATABASE_NAME = 'htmlmin.db'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_NAME,
    },
}
DEBUG = True
HTML_MINIFY = True
ROOT_URLCONF = 'htmlmin.tests.pico_django'
KEEP_COMMENTS_ON_MINIFYING = True
SECRET_KEY = "sosecret"
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
