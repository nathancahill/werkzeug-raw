## Werkzeug-Raw

Werkzeug meets Raw HTTP

### Installation

To install Werkzeug-Raw, simply:

```
$ pip install werkzeug-raw
```

### Usage

Given raw HTTP:

```
GET /foo/bar?tequila=42 HTTP/1.1
Host: example.org
```

Send a request to a Flask test client:

```python
from werkzeug_raw import open_raw_request

client = app.test_client()

with open('foobar.txt') as f:
    rv = open_raw_request(client, f.read())
```

Request context is also supported:

```python
from werkzeug_raw import raw_environ

with open('foobar.txt') as f:
    environ = raw_environ(f.read())

with app.request_context(environ):
    print request.args  # ImmutableMultiDict([('tequila', u'42')])
```