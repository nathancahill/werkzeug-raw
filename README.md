## Werkzeug-Raw

[![Build Status](https://travis-ci.org/nathancahill/werkzeug-raw.svg?branch=master)](https://travis-ci.org/nathancahill/werkzeug-raw)
[![Coverage Status](https://coveralls.io/repos/nathancahill/werkzeug-raw/badge.svg?branch=master&service=github)](https://coveralls.io/github/nathancahill/werkzeug-raw?branch=master)

Werkzeug meets Raw HTTP

__Werkzeug-Raw__ adds support to Werkzeug for accepting HTTP input from
raw text, from strings or files. Compatibility with Flask makes fuzzing or
testing complex HTTP requests in Flask applications very simple.

Additionally, it circumvents the need for a client/server/network setup,
and goes directly from raw HTTP to WSGI environment. A large number of requests
can be handled without needing to worry about secondary variables like network
latency clouding the water. This is not meant as a benchmarking tool for Werkzeug or Flask.

### Installation

To install Werkzeug-Raw, simply:

```
$ pip install werkzeug-raw
```

### Documentation

Documentation is available at [http://pythonhosted.org/Werkzeug-Raw](http://pythonhosted.org/Werkzeug-Raw)

### Contribute

Fork the repository, make changes and add a test which shows that the bug was fixed or that the feature works as expected with 100% coverage. Send a pull request.