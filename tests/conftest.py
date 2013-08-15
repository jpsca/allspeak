# -*- coding: utf-8 -*-
import pytest

from django.http import HttpRequest as DjangoRequest
from webob import Request as WebobRequest
from werkzeug.wrappers import Request


def make_werkzeug_request(env, path):
    return Request(env)


def make_webob_request(env, path):
    return WebobRequest(dict(env))


def make_django_request(env, path):
    r = DjangoRequest()
    r.path = path
    r.META = dict(env)
    return r


@pytest.fixture(params=['werkzeug', 'webob', 'django'])
def make_req(request):
    return globals()['make_{0}_request'.format(request.param)]
