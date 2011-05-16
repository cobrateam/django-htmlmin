dependencies: coverage lxml nose

clean:
	@find . -name "*.pyc" -delete

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml

test: dependencies clean
	@nosetests --with-xunit --xunit-file=nose.xml --with-coverage --cover-erase --cover-package=htmlmin --verbosity=2 --where=htmlmin/tests
