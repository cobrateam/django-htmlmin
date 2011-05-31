dependencies: coverage django BeautifulSoup specloud nosedjango

clean:
	@find . -name "*.pyc" -delete

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

django:
	@python -c 'import django' 2>/dev/null || pip install django

BeautifulSoup:
	@python -c 'import BeautifulSoup' 2>/dev/null || pip install BeautifulSoup

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install specloud

nosedjango:
	@python -c 'import nosedjango' 2>/dev/null || pip install nosedjango

test: dependencies clean
	@specloud --with-xunit --xunit-file=nose.xml --with-coverage --with-django --django-settings=htmlmin.tests.mock_settings --django-sqlite=use_sqlite --cover-erase --cover-package=htmlmin --verbosity=2 --where=htmlmin/tests
