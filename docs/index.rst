.. Werkzeug-Raw documentation master file, created by
   sphinx-quickstart on Wed Oct 21 12:41:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Werkzeug-Raw
============

Werkzeug meets Raw HTTP.

**Werkzeug-Raw** adds support to Werkzeug for accepting
HTTP input from raw text, from strings or files. Compatibility with Flask
makes fuzzing or testing complex HTTP requests in Flask applications
very simple.

Additionally, it circumvents the need for a client/server/network setup,
and goes directly from raw HTTP to WSGI environment. A large number of requests
can be handled without needing to worry about secondary variables like network
latency clouding the water. This is not meant as a benchmarking tool for Werkzeug or Flask.


Installation
------------

Install with **pip**::

    $ pip install werkzeug-raw

Or download the latest version from Github::

    $ git clone https://github.com/nathancahill/werkzeug-raw.git
    $ cd werkzeug-raw
    $ python setup.py install


Example Usage
-------------

Creating a WSGI environment from an HTTP request is easy. The resulting
environment is compatible with Flask's request context::

    from flask import Flask
    import werkzeug_raw

    app = Flask(__name__)

    environ = werkzeug_raw.environ('GET /foo/bar?tequila=42 HTTP/1.1')

    with app.request_context(environ):
        print request.args  # ImmutableMultiDict([('tequila', u'42')])


Opening a request on a Flask test client is just as easy. The parameters and
behavior are the same as `flask.testing.FlaskClient.open()`
or the more common `client.get()`/`client.post()` except with raw HTTP::

    from flask import Flask
    import werkzeug_raw

    app = Flask(__name__)
    client = app.test_client()

    rv = werkzeug_raw.open(client, 'GET /foo/bar?tequila=42 HTTP/1.1')

For testing against a directory of raw HTTP requests stored as text files,
open each request on a Flask test client like this::

    import os

    from flask import Flask
    import werkzeug_raw

    app = Flask(__name__)

    client = app.test_client()

    for fn in os.listdir('raw'):
        with open(os.path.join('raw', fn)) as f:
            rv = werkzeug_raw.open(client, f.read())

For fuzzing, malformed HTTP requests can be ignored by handling the raised
error during parsing::

    try:
        rv = werkzeug_raw.open('GET ----- /foo/bar?tequila=42 HTTP/1.1')
    except werkzeug_raw.BadRequestSyntax:
        pass
    else:
        assert rv.status_code == 200


API
---

.. module:: werkzeug_raw

.. autoclass:: RawHTTPRequest

.. autofunction:: environ

.. autofunction:: open

