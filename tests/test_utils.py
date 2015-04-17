# coding=utf-8
from __future__ import print_function

from allspeak import utils
from babel import Locale
from pytz import timezone

from .conftest import (
    make_werkzeug_request, make_webob_request, make_django_request,
    get_test_request,
)


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
    assert utils.normalize_locale('es') == Locale('es')
    assert utils.normalize_locale('en-US') == Locale('en', 'US')
    assert utils.normalize_locale('en_US') == Locale('en', 'US')
    assert utils.normalize_locale(Locale('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale(('es', )) == Locale('es')
    assert utils.normalize_locale(('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale('En-Us') == Locale('en', 'US')
    assert utils.normalize_locale('klingon') == None


def test_normalize_timezone():
    assert utils.normalize_timezone(timezone('America/Lima')) == timezone('America/Lima')
    assert utils.normalize_timezone('America/Lima') == timezone('America/Lima')
    assert utils.normalize_timezone('Mars') == None


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


def test_get_request_timezone():
    class FakeRequest(object):
        pass

    request = FakeRequest()

    request.tzinfo = 'America/Lima'
    assert utils.get_request_timezone(request) == timezone('America/Lima')

    request.tzinfo = timezone('America/Lima')
    assert utils.get_request_timezone(request) == timezone('America/Lima')

    request.tzinfo = None
    assert utils.get_request_timezone(request) == None

    request.tzinfo = 'Mars'
    assert utils.get_request_timezone(request) == None

    request.tzinfo = 'Mars'
    assert (
        utils.get_request_timezone(request, default=utils.DEFAULT_TIMEZONE) ==
        utils.DEFAULT_TIMEZONE
    )


def test_get_request_locale():
    class FakeRequest(object):
        pass

    request = FakeRequest()

    request.locale = 'es'
    assert utils.get_request_locale(request) == Locale('es')

    request.locale = 'en-US'
    assert utils.get_request_locale(request) == Locale('en', 'US')

    request.locale = 'en_US'
    assert utils.get_request_locale(request) == Locale('en', 'US')

    request.locale = Locale('en', 'US')
    assert utils.get_request_locale(request) == Locale('en', 'US')

    request.locale = ('es', )
    assert utils.get_request_locale(request) == Locale('es')

    request.locale = ('en', 'US')
    assert utils.get_request_locale(request) == Locale('en', 'US')

    request.locale = 'En-Us'
    assert utils.get_request_locale(request) == Locale('en', 'US')

    request.locale = None
    assert utils.get_request_locale(request) == None

    request.locale = 'klingon'
    assert utils.get_request_locale(request) == None

    request.locale = 'klingon'
    assert (
        utils.get_request_locale(request, default=utils.DEFAULT_LOCALE) ==
        utils.DEFAULT_LOCALE
    )


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
    assert utils.pluralize(d, None) == u'off'
    assert utils.pluralize({}, 3) == u''
