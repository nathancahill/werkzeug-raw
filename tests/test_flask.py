
import os
from flask import Flask, redirect
import unittest
import werkzeug
import werkzeug_raw


VALID_DIR = os.path.join('tests', 'raw', 'valid')
INVALID_DIR = os.path.join('tests', 'raw', 'invalid')

app = Flask(__name__)
client = app.test_client()


@app.route('/redirect')
def _redirect():
    return redirect('/')


@app.route('/redirectloop')
def _redirectloop():
    return redirect('/redirectloop')


class FlaskTest(unittest.TestCase):
    def test_valid(self):
        for fn in os.listdir(VALID_DIR):
            with open(os.path.join(VALID_DIR, fn), "rb") as f:
                werkzeug_raw.open(client, f.read())

    def test_invalid(self):
        for fn in os.listdir(INVALID_DIR):
            with open(os.path.join(INVALID_DIR, fn), "rb") as f:
                with self.assertRaises(werkzeug_raw.BadRequestSyntax):
                    werkzeug_raw.open(client, f.read())

    def test_redirect(self):
        werkzeug_raw.open(client, b'GET /redirect HTTP/1.1', follow_redirects=True)

    def test_redirect_loop(self):
        with self.assertRaises(werkzeug.test.ClientRedirectError):
            werkzeug_raw.open(client, b'GET /redirectloop HTTP/1.1', follow_redirects=True)

    def test_tuple_resp(self):
        environ, resp = werkzeug_raw.open(client, b'GET /foo/bar HTTP/1.1', as_tuple=True)
