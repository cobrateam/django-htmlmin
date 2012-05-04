# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

dependencies: coverage django BeautifulSoup nosedjango

clean:
	@find . -name "*.pyc" -delete

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

django:
	@python -c 'import django' 2>/dev/null || pip install django

BeautifulSoup:
	@python -c 'import BeautifulSoup' 2>/dev/null || pip install BeautifulSoup

nosedjango:
	@python -c 'import nosedjango' 2>/dev/null || pip install nosedjango

test: dependencies clean
	@nosetests -s --with-xunit --xunit-file=nose.xml --with-coverage --with-django --django-settings=htmlmin.tests.mock_settings --django-sqlite=use_sqlite --cover-erase --cover-package=htmlmin --where=htmlmin/tests
