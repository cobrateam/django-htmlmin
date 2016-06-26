++++++++++++++
django-htmlmin
++++++++++++++

.. image:: https://secure.travis-ci.org/cobrateam/django-htmlmin.png
   :target: http://travis-ci.org/cobrateam/django-htmlmin

django-html is an HTML minifier for Python, with full support for HTML 5. It
supports Django, Flask and many other Python web frameworks. It also provides a
command line tool, that can be used for static websites or deployment scripts.

Why minify HTML code?
=====================

One of the important points on client side optimization is to minify HTML. With
minified HTML code, you reduce the size of the data transferred from the server
to the client, which results in faster load times.

Installing
==========

To install django-htmlmin, run this on the terminal: :

.. code-block:: sh

    $ [sudo] pip install django-htmlmin

Using the middleware
====================

All you need to do is add two middlewares to your ``MIDDLEWARE_CLASSES`` and
enable the ``HTML_MINIFY`` setting:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # other middleware classes
        'htmlmin.middleware.HtmlMinifyMiddleware',
        'htmlmin.middleware.MarkRequestMiddleware',
    )

Note that if you're using Django's caching middleware,
``MarkRequestMiddleware`` should go after ``FetchFromCacheMiddleware``, and
``HtmlMinifyMiddleware`` should go after ``UpdateCacheMiddleware``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'django.middleware.cache.UpdateCacheMiddleware',
        'htmlmin.middleware.HtmlMinifyMiddleware',
        # other middleware classes
        'django.middleware.cache.FetchFromCacheMiddleware',
        'htmlmin.middleware.MarkRequestMiddleware',
    )

You can optionally specify the ``HTML_MINIFY`` setting:


.. code-block:: python

    HTML_MINIFY = True

The default value for the ``HTML_MINIFY`` setting is ``not DEBUG``. You only
need to set it to ``True`` if you want to minify your HTML code when ``DEBUG``
is enabled.

Excluding some URLs
-------------------

If you don't want to minify all views in your app and it's under a ``/my_app``
URL, you can tell the middleware to not minify the response of your views by
adding a ``EXCLUDE_FROM_MINIFYING`` setting on your settings.py:

.. code-block:: python

    EXCLUDE_FROM_MINIFYING = ('^my_app/', '^admin/')

Regex patterns are used for URL exclusion. If you want to exclude all URLs of
your app, except a specific view, you can use the decorator
``@minified_response`` (check the next section above).

Keeping comments
----------------

The default behaviour of the middleware is to remove all HTML comments. If you
want to keep the comments, set the setting ``KEEP_COMMENTS_ON_MINIFYING``
to ``True``:

.. code-block:: python

    KEEP_COMMENTS_ON_MINIFYING = True

Using the decorator
===================

django-htmlmin also provides a decorator, that you can use only on views you
want to minify the response:

.. code-block:: python

    from htmlmin.decorators import minified_response

    @minified_response
    def home(request):
        return render_to_response('home.html')

Decorator to avoid response to be minified
------------------------------------------

You can use the ``not_minified_response`` decorator on views if you want to
avoid the minification of any specific response, without using the
``EXCLUDE_FROM_MINIFYING`` setting:

.. code-block:: python

    from htmlmin.decorators import not_minified_response

    @not_minified_response
    def home(request):
        return render_to_response('home.html')

Using the ``html_minify`` function
==================================

If you are not working with Django, you can invoke the ``html_minify`` function
manually:

.. code-block:: python

    from htmlmin.minify import html_minify
    html = '<html>    <body>Hello world</body>    </html>'
    minified_html = html_minify(html)

Here is an example with a `Flask <http://flask.pocoo.org>`_ view:

.. code-block:: python

    from flask import Flask
    from htmlmin.minify import html_minify

    app = Flask(__name__)

    @app.route('/')
    def home():
        rendered_html = render_template('home.html')
        return html_minify(rendered_html)

Keeping comments
----------------

By default, ``html_minify()`` removes all comments. If you want to keep them,
you can pass ``ignore_comments=False``:

.. code-block:: python

    from htmlmin.minify import html_minify
    html = '<html>  <body>Hello world<!-- comment to keep --></body>  </html>'
    minified_html = html_minify(html, ignore_comments=False)


Using command line tool
=======================

If you are not even using Python, you can use the ``pyminify`` command line
tool to minify HTML files:

.. code-block:: sh

    $ pyminify index.html > index_minified.html

You can also keep the comments, if you want:

.. code-block:: sh

    $ pyminify --keep-comments index.html > index_minified_with_comments.html

development
===========

* Source hosted at `GitHub <http://github.com/cobrateam/django-htmlmin>`_
* Report issues on `GitHub Issues
  <http://github.com/cobrateam/django-htmlmin/issues>`_

Pull requests are very welcome! Make sure your patches are well tested.

Running tests
-------------

If you are using a virtualenv, all you need to do is:

.. code-block:: sh

    $ make test

community
=========

IRC channel
-----------

``#cobrateam`` channel on ``irc.freenode.net``

Changelog
=========

You can see the complete changelog on the
`Github releases page <https://github.com/cobrateam/django-htmlmin/releases>`_.

LICENSE
=======

Unless otherwise noted, the ``django-htmlmin`` source files are distributed
under the BSD-style license found in the LICENSE file.
