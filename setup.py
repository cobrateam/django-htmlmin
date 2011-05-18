from setuptools import setup, find_packages


README = open('README.rst').read()

setup(name='django-htmlmin',
      version='0.1',
      description='html minify for django',
      long_description=README,
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      test_suite='nose.collector',
      install_requires=['django', 'lxml'],
      tests_require=['nose', 'coverage'],
      )
