from __future__ import print_function

# stdlib
import pickle
import unittest

# pyramid testing requirements
from pyramid import testing
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.response import Response
from pyramid.request import Request

# local
import pyramid_https_session_redis


# ------------------------------------------------------------------------------


def view_cookie_unused(request):
    return Response(
        "<html><head></head><body>OK</body></html>", content_type="text/html"
    )


def view_cookie_used(request):
    request.session_https["foo"] = "bar"
    return Response(
        "<html><head></head><body>OK</body></html>", content_type="text/html"
    )


# for testing, we MUST pass `ensure_scheme=False`
# otherwise it is too hard to test, as we need to layer in the middleware
redis_session_config = {
    "secret": "supersecret",
    "db": 9,
    "serialize": pickle.dumps,
    "deserialize": pickle.loads,
    "ensure_scheme": False,
}

# https_prefixes = ("session_https.", "redis.sessions_https.", "redis.session_https.")


class _TestCookiePrefixed(object):
    _prefix = None

    def generated_prefixed(self):
        _prefixed = {}
        for (k, v) in redis_session_config.items():
            _prefixed["%s.%s" % (self._prefix, k)] = v
        return _prefixed


class _TestCookieUnused(_TestCookiePrefixed):
    def setUp(self):
        settings = self.generated_prefixed()
        self.config = testing.setUp(settings=settings)
        self.settings = self.config.registry.settings
        pyramid_https_session_redis.initialize_https_session_support(
            self.config,
            self.settings,
        )
        # create a view
        self.config.add_view(view_cookie_unused)

    def tearDown(self):
        testing.tearDown()

    def test_itworked(self):

        # make the app
        app = self.config.make_wsgi_app()

        # make a request
        req1 = Request.blank("/")
        req1.remote_addr = "127.0.0.1"
        resp1 = req1.get_response(app)
        self.assertEqual(resp1.status_code, 200)
        self.assertNotIn("Set-Cookie", resp1.headers)


class _TestCookieUsed(_TestCookiePrefixed):
    def setUp(self):
        settings = self.generated_prefixed()
        self.config = testing.setUp(settings=settings)
        self.settings = self.config.registry.settings
        pyramid_https_session_redis.initialize_https_session_support(
            self.config,
            self.settings,
        )
        # create a view
        self.config.add_view(view_cookie_used)

    def tearDown(self):
        testing.tearDown()

    def test_itworked(self):

        # make the app
        app = self.config.make_wsgi_app()

        # make a request
        req1 = Request.blank("/")
        req1.remote_addr = "127.0.0.1"
        resp1 = req1.get_response(app)
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("Set-Cookie", resp1.headers)


class TestCookieUnused_A(_TestCookieUnused, unittest.TestCase):
    _prefix = "session_https"


class TestCookieUnused_B(_TestCookieUnused, unittest.TestCase):
    _prefix = "redis.sessions_https"


class TestCookieUnused_C(_TestCookieUnused, unittest.TestCase):
    _prefix = "redis.session_https"


class TestCookieUsed_A(_TestCookieUsed, unittest.TestCase):
    _prefix = "session_https"


class TestCookieUsed_B(_TestCookieUsed, unittest.TestCase):
    _prefix = "redis.sessions_https"


class TestCookieUsed_C(_TestCookieUsed, unittest.TestCase):
    _prefix = "redis.session_https"
