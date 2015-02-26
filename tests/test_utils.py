# -*- coding: utf-8 -*-
from __future__ import print_function

from allspeak import utils
from babel import Locale
from werkzeug.test import EnvironBuilder

from .conftest import make_werkzeug_request, make_webob_request, make_django_request


def get_test_env(path, **kwargs):
    builder = EnvironBuilder(path=path, **kwargs)
    return builder.get_environ()


def get_test_request(make_req, path='/', **kwargs):
    env = get_test_env(path, **kwargs)
    return make_req(env, path)


def test_content_negotiation(make_req):
    available_locales = ['en', 'es', 'es-PE']

    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.negotiate_locale(req, available_locales) == Locale('es')

    headers = [('Accept-Language', 'fr; q=1.0, en-US; q=0.5, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.negotiate_locale(req, available_locales) == Locale('en')

    headers = [('Accept-Language', 'fr; q=1.0, es-PE; q=0.5, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.negotiate_locale(req, available_locales) == Locale('es', 'PE')

    headers = [('Accept-Language', 'fr; q=1.0, es-PE; q=0.5, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.negotiate_locale(req, ['ru']) is None

    headers = [('Accept-Language', 'martian; q=1.0, venus; q=0.5, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.negotiate_locale(req, ['klingon']) is None


def test_normalize_locale():
    from babel import Locale

    assert utils.normalize_locale(Locale('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale('en-US') == Locale('en', 'US')
    assert utils.normalize_locale('en_US') == Locale('en', 'US')
    assert utils.normalize_locale('es') == Locale('es')
    assert utils.normalize_locale(('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale(('es', )) == Locale('es')
    assert utils.normalize_locale('klingon') == None


def test_get_werkzeug_preferred_locales():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_werkzeug_request, headers=headers)
    langs = utils.get_werkzeug_preferred_locales(req)
    assert langs == ['fr', 'pt', 'es']


def test_get_webob_preferred_locales():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_webob_request, headers=headers)
    langs = utils.get_webob_preferred_locales(req)
    assert langs == ['fr', 'pt', 'es']


def test_get_django_preferred_locales():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.6')]
    req = get_test_request(make_django_request, headers=headers)
    langs = utils.get_django_preferred_locales(req)
    assert langs == ['fr', 'pt', 'es']


def test_pluralize():
    d = {
        0: u'No apples',
        1: u'One apple',
        3: u'Few apples',
        'n': u'%(count)s apples',
    }
    assert utils.pluralize(d, 0) == u'No apples'
    assert utils.pluralize(d, 1) == u'One apple'
    assert utils.pluralize(d, 3) == u'Few apples'
    assert utils.pluralize(d, 10) == u'%(count)s apples'

    d = {
        0: u'off',
        'n': u'on'
    }
    assert utils.pluralize(d, 3) == u'on'

    d = {
        0: u'off',
        'n': u'on'
    }
    assert utils.pluralize(d, 0) == u'off'
    assert utils.pluralize({}, 3) == u''
