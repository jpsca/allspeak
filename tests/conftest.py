# coding=utf-8
import pytest

from django.conf import settings
from django.http import HttpRequest as DjangoRequest
from webob import Request as WebobRequest
from werkzeug.wrappers import Request
from werkzeug.test import EnvironBuilder


settings.configure()


def make_werkzeug_request(env, path):
    return Request(env)


def make_webob_request(env, path):
    return WebobRequest(dict(env))


def make_django_request(env, path):
    r = DjangoRequest()
    r.path = path
    r.META = dict(env)
    return r


def get_test_env(path, **kwargs):
    builder = EnvironBuilder(path=path, **kwargs)
    return builder.get_environ()


def get_test_request(make_req, path='/', **kwargs):
    env = get_test_env(path, **kwargs)
    return make_req(env, path)


def make_get_request(locale='es_PE', tzinfo='America/Lima'):
    """Returns a fake request generator for testing
    """
    _locale = locale
    _tzinfo = tzinfo

    def get_request():
        req = get_test_request(make_werkzeug_request)
        req.locale = _locale
        req.tzinfo = _tzinfo
        return req

    return get_request


@pytest.fixture(params=['werkzeug', 'webob', 'django'])
def make_req(request):
    return globals()['make_{0}_request'.format(request.param)]
