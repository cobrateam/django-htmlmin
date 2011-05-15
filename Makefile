test:
	@nosetests --with-xunit --xunit-file=nose.xml --with-coverage --cover-erase --cover-package=htmlmin --verbosity=2 --where=htmlmin/tests
