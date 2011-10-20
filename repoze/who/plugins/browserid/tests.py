import unittest

from zope.interface.verify import verifyClass
from repoze.who.interfaces import IIdentifier
from repoze.who.interfaces import IAuthenticator
from repoze.who.interfaces import IChallenger

from repoze.who.plugins.browserid import BrowserIDPlugin


def make_environ(**kwds):
    environ = {}
    environ["wsgi.version"] = (1, 0)
    environ["wsgi.url_scheme"] = "http"
    environ["SERVER_NAME"] = "localhost"
    environ["SERVER_PORT"] = "80"
    environ["REQUEST_METHOD"] = "GET"
    environ["SCRIPT_NAME"] = ""
    environ["PATH_INFO"] = "/"
    environ.update(kwds)
    return environ


def get_response(app, environ):
    output = []
    def start_response(status, headers, exc_info=None): # NOQA
        output.append(status + "\r\n")
        for name, value in headers:
            output.append("%s: %s\r\n" % (name, value))
        output.append("\r\n")
    for chunk in app(environ, start_response):
        output.append(chunk)
    return "".join(output)


class TestBrowserIDPlugin(unittest.TestCase):
    """Testcases for the main BrowserIDPlugin class."""

    def test_implements(self):
        verifyClass(IIdentifier, BrowserIDPlugin)
        verifyClass(IAuthenticator, BrowserIDPlugin)
        verifyClass(IChallenger, BrowserIDPlugin)