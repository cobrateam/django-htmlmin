# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

dependencies:
	@pip install -r test-requirements.txt

clean:
	@find . -name "*.pyc" -delete

test: dependencies clean
	@nosetests -s --with-xunit --xunit-file=nose.xml --with-coverage --with-django --django-settings=htmlmin.tests.mock_settings --cover-erase --cover-package=htmlmin --where=htmlmin/tests
