dependencies: coverage lxml specloud

clean:
	@find . -name "*.pyc" -delete

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install specloud

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml

test: dependencies clean
	@specloud --with-xunit --xunit-file=nose.xml --with-coverage --cover-erase --cover-package=htmlmin --verbosity=2 --where=htmlmin/tests
