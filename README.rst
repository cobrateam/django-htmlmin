++++++++++++++
django-htmlmin
++++++++++++++

html minify for django

Why minify HTML code?
=====================

One of important points on client side optimization is minify HTML, with minified HTML code, you reduce the size of data transferred from your server to your client, and your pages load faster.

Installing
==========

For install django-htmlmin, run on terminal: ::

    $ [sudo] pip install django-htmlmin

Using the midleware
===================

All you need to do is add ``htmlmin.middleware.HtmlMinifyMiddleware`` to your ``MIDDLEWARE_CLASSES``: ::

    MIDDLEWARE_CLASSES = (
        # other middleware classes
        'htmlmin.middleware.HtmlMinifyMiddleware',
    )

Using the html_minify function
==============================

If you are not working with Django, you can invoke the ``html_minify`` function manually: ::

    from htmlmin.minify import html_minify
    html = '<html>    <body>Hello world</body>    </html>'
    minified_html = html_minify(html)

Here is an example of `Flask <http://flask.pocoo.org>`_ view: ::

    from flask import Flask
    from htmlmin.minify import html_minify

    app = Flask(__name__)

    @app.route('/')
    def home():
        rendered_html = render_template('home.html')
        return html_minify(rendered_html)

development
===========

* Source hosted at `GitHub <http://github.com/cobrateam/django-htmlmin>`_
* Report issues on `GitHub Issues <http://github.com/cobrateam/django-htmlmin/issues>`_

Pull requests are very welcomed! Make sure your patches are well tested.

running the tests
-----------------

if you are using a virtualenv, all you need is:

::

    $ make test

community
=========

irc channel
-----------

#cobrateam channel on irc.freenode.net
