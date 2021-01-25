# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

.PHONY: dependencies
dependencies:
	@pip install -r requirements.txt

.PHONY: clean
clean:
	@find . -name "*.pyc" -delete

.PHONY: test
test: dependencies clean runtests

.PHONY: runtests
runtests:
	django-admin.py test --settings htmlmin.tests.mock_settings htmlmin
