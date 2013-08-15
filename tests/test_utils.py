# -*- coding: utf-8 -*-
from __future__ import print_function

from allspeak import utils
from werkzeug.test import EnvironBuilder

from .conftest import make_werkzeug_request, make_webob_request, make_django_request 


def get_test_env(path, **kwargs):
    builder = EnvironBuilder(path=path, **kwargs)
    return builder.get_environ()


def get_test_request(make_req, path='/', **kwargs):
    env = get_test_env(path, **kwargs)
    return make_req(env, path)


def test_normalize_locale():
    from babel import Locale

    assert utils.normalize_locale(Locale('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale('en-US') == Locale('en', 'US')
    assert utils.normalize_locale('en_US') == Locale('en', 'US')
    assert utils.normalize_locale('es') == Locale('es')
    assert utils.normalize_locale(('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale(('es', )) == Locale('es')


def test_get_werkzeug_preferred_languages():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_werkzeug_request, headers=headers)
    langs = utils.get_werkzeug_preferred_languages(req)
    assert langs == ['fr', 'pt', 'es']


def test_get_webob_preferred_languages():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_webob_request, headers=headers)
    langs = utils.get_webob_preferred_languages(req)
    assert langs == ['fr', 'pt', 'es']


def test_get_django_preferred_languages():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_django_request, headers=headers)
    langs = utils.get_django_preferred_languages(req)
    assert langs == ['fr', 'pt', 'es']
