
from six import BytesIO

from werkzeug.serving import WSGIRequestHandler
from werkzeug.test import ClientRedirectError
from werkzeug.exceptions import BadRequest


__all__ = ['RawHTTPRequest', 'BadRequest', 'environ', 'open']


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class RawHTTPRequest(WSGIRequestHandler):
    """A subclass of `werkzeug.serving.WSGIRequestHandler` that accepts
    raw HTTP input from a string `raw`. `error_code` and `error_message` will
    be set if parsing fails.

    :param raw: Raw HTTP string.
    :returns: `werkzeug_raw.RawHTTPRequest`
    """

    def __init__(self, raw):
        self.server = AttrDict(
            ssl_context=None,
            multithread=False,
            multiprocess=False,
            server_address=('localhost', 80),
        )
        self.client_address = 'localhost'
        self.rfile = BytesIO(raw)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


class BadRequestSyntax(BadRequest):
    """**400** `Bad Request`

    Raise if the raw HTTP input parsing fails.
    """
    code = 400
    description = (
        'The browser (or proxy) sent a request that this server could '
        'not understand.'
    )


def environ(raw):
    """A wrapper around `RawHTTPRequest` that raises `ValueError` if HTTP
    parsing returns an error code. Returns a WSGI environment suitable for
    Flask request context.

    :param raw: Raw HTTP string.
    :returns: WSGI environment.
    :raises: `ValueError`
    """
    request = RawHTTPRequest(raw)

    if request.error_code:
        raise BadRequestSyntax

    return request.make_environ()


def open(client, raw, *args, **kwargs):
    """Opens a request on a `werkzeug.test.Client` with raw HTTP input from
    a string `raw`. Suitable for opening requests on Flask test clients.

    :param client: `werkzeug.test.Client`
    :param raw: Raw HTTP string.
    :param as_tuple: Returns a tuple in the form ``(environ, result)``
    :param buffered: Set this to True to buffer the application run.
                     This will automatically close the application for
                     you as well.
    :param follow_redirects: Set this to True if the `Client` should
                             follow HTTP redirects.

    :returns: Response.
    """
    as_tuple = kwargs.pop('as_tuple', False)
    buffered = kwargs.pop('buffered', False)
    follow_redirects = kwargs.pop('follow_redirects', False)
    _environ = environ(raw)

    response = client.run_wsgi_app(_environ, buffered=buffered)

    #: handle redirects
    redirect_chain = []
    while 1:
        status_code = int(response[1].split(None, 1)[0])
        if status_code not in (301, 302, 303, 305, 307) \
           or not follow_redirects:
            break
        new_location = response[2]['location']
        new_redirect_entry = (new_location, status_code)
        if new_redirect_entry in redirect_chain:
            raise ClientRedirectError('loop detected')
        redirect_chain.append(new_redirect_entry)
        _environ, response = client.resolve_redirect(response, new_location,
                                                     _environ,
                                                     buffered=buffered)

    if client.response_wrapper is not None:
        response = client.response_wrapper(*response)
    if as_tuple:
        return _environ, response
    return response
