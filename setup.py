
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Werkzeug-Raw',
    version='0.0.1',
    description='Werkzeug meets Raw HTTP',
    long_description=long_description,
    url='http://pythonhosted.org/Werkzeug-Raw/',
    author='Nathan Cahill',
    author_email='nathan@nathancahill.com',
    license='MIT',
    keywords='werkzeug flask http',
    py_modules=['werkzeug_raw'],
    install_requires=['werkzeug', 'six'],
    tests_require=['nose', 'coverage'],
)
