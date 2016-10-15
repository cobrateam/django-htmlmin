# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

dependencies:
	@pip install -r requirements.txt

clean:
	@find . -name "*.pyc" -delete

test: dependencies clean
	@tox
