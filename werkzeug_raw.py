
from StringIO import StringIO

from werkzeug.serving import WSGIRequestHandler
from werkzeug.test import ClientRedirectError


__all__ = ['RawHTTPRequest', 'raw_environ', 'open_raw_request']


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class RawHTTPRequest(WSGIRequestHandler):
    """A subclass of `werkzeug.serving.WSGIRequestHandler` that accepts
    raw HTTP input from a string `raw`.

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
        self.rfile = StringIO(raw)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


def raw_environ(raw):
    """A wrapper around `RawHTTPRequest` that raises `ValueError` if HTTP
    parsing returns an error code. Returns a WSGI environment.

    :param raw: Raw HTTP string.
    :returns: WSGI environment.
    :raises: `ValueError`
    """
    request = RawHTTPRequest(raw)

    if request.error_code:
        raise ValueError(request.error_message)

    return request.make_environ()


def open_raw_request(client, raw, *args, **kwargs):
    """Opens a request on a `werkzeug.test.Client` with raw HTTP input from
    a string `raw`.

    :param client: `werkzeug.test.Client`
    :param raw: Raw HTTP string.

    Additional parameters:

    :param as_tuple: Returns a tuple in the form ``(environ, result)``
    :param buffered: Set this to True to buffer the application run.
                     This will automatically close the application for
                     you as well.
    :param follow_redirects: Set this to True if the `Client` should
                             follow HTTP redirects.

    :returns: Response
    """
    as_tuple = kwargs.pop('as_tuple', False)
    buffered = kwargs.pop('buffered', False)
    follow_redirects = kwargs.pop('follow_redirects', False)
    environ = raw_environ(raw)

    response = client.run_wsgi_app(environ, buffered=buffered)

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
        environ, response = client.resolve_redirect(response, new_location,
                                                    environ,
                                                    buffered=buffered)

    if client.response_wrapper is not None:
        response = client.response_wrapper(*response)
    if as_tuple:
        return environ, response
    return response
