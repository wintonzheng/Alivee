# Put Third Party/Django Imports Here:
import urllib

# Put Alivee Imports Here:
from general_utils.requests.exceptions import RequestMethodNotSupportedException


class RequestMeta(object):
    '''
    Request metadata class which holds:
        host name, url path, url params, headers, reqeuest body, request method and reqeust protocol.
    '''

    def __init__(self,
                 host,
                 path='',
                 params=None,
                 method=None,
                 headers=None,
                 body=None,
                 protocol='https'):
        if method not in self.validMethods():
            raise RequestMethodNotSupportedException(
                "invalid_method={0} for url={1} valid_methods={2}".format(
                    method,
                    self.url,
                    self.validMethods()
                )
            )
        self._method = method
        self._host = host
        self._path = path
        self._params = params or {}
        self._headers = headers or {}
        self._body = body or {}
        self._protocol = protocol

    def validMethods(self):
        raise NotImplementedError

    @property
    def host(self):
        return self._host

    @property
    def path(self):
        return self._path

    @property
    def params(self):
        return self._params

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

    @property
    def protocol(self):
        return self._protocol

    @property
    def url(self):
        base_url = '{0}://{1}/{2}'.format(self.protocol, self.host, self.path)
        if self.params:
            return '{0}?{1}'.format(base_url, self.encodedParams)
        return base_url

    @property
    def encodedParams(self):
        return urllib.urlencode(self._params)
