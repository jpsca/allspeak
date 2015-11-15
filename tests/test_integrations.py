# coding=utf-8
from __future__ import print_function

from allspeak import integrations

from .conftest import (
    make_werkzeug_request, make_webob_request, make_django_request,
    get_test_request,
)


def test_get_werkzeug_preferred_locales():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_werkzeug_request, headers=headers)
    langs = integrations.get_werkzeug_preferred_locales(req)
    assert langs == ['fr', 'pt', 'es']


def test_get_webob_preferred_locales():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_webob_request, headers=headers)
    langs = integrations.get_webob_preferred_locales(req)
    assert langs == ['fr', 'pt', 'es']


def test_get_django_preferred_locales():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_django_request, headers=headers)
    langs = integrations.get_django_preferred_locales(req)
    assert langs == ['fr', 'pt', 'es']
