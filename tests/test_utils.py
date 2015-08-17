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

    preferred = ['fr', 'es', 'pt']
    assert utils.negotiate_locale(preferred, available_locales) == Locale('es')

    preferred = ['fr', 'en-US', 'pt']
    assert utils.negotiate_locale(preferred, available_locales) == Locale('en')

    preferred = ['fr', 'es-PE', 'pt']
    assert utils.negotiate_locale(preferred, available_locales) == Locale('es', 'PE')

    preferred = ['fr', 'es-PE', 'pt']
    assert utils.negotiate_locale(preferred, ['ru']) is None

    preferred = ['martian', 'venus', 'pt']
    assert utils.negotiate_locale(preferred, ['klingon']) is None

    preferred = ['fr', 'es-PE', 'pt']
    assert utils.negotiate_locale(preferred, []) is None


def test_get_preferred_locales(make_req):
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.6, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.get_preferred_locales(req) == ['fr', 'es', 'pt']

    headers = [('Accept-Language', 'fr; q=1.0, en-US; q=0.6, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.get_preferred_locales(req) == ['fr', 'en_US', 'pt']

    headers = [('Accept-Language', 'fr; q=1.0, es-PE; q=0.6, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.get_preferred_locales(req) == ['fr', 'es_PE', 'pt']

    headers = [('Accept-Language', 'fr; q=1.0, es_pe; q=0.6, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.get_preferred_locales(req) == ['fr', 'es_PE', 'pt']

    headers = [('Accept-Language', 'martian; q=1.0, venus; q=0.6, pt; q=0.5')]
    req = get_test_request(make_req, headers=headers)
    assert utils.get_preferred_locales(req) == ['martian', 'venus', 'pt']

    req = get_test_request(make_req)
    assert utils.get_preferred_locales(req) == []


def test_split_locale():
    assert utils.split_locale('en-US') == ('en', 'US')
    assert utils.split_locale('En_us') == ('en', 'US')
    assert utils.split_locale(Locale('en', 'US')) == ('en', 'US')


def test_normalize_locale():
    assert utils.normalize_locale('es') == Locale('es')
    assert utils.normalize_locale('en-US') == Locale('en', 'US')
    assert utils.normalize_locale('en_us') == Locale('en', 'US')
    assert utils.normalize_locale('en-us') == Locale('en', 'US')
    assert utils.normalize_locale('en_US') == Locale('en', 'US')
    assert utils.normalize_locale('En-Us') == Locale('en', 'US')

    assert utils.normalize_locale(Locale('en', 'US')) == Locale('en', 'US')

    assert utils.normalize_locale(('es', )) == Locale('es')
    assert utils.normalize_locale(('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale(['en', 'US']) == Locale('en', 'US')
    assert utils.normalize_locale(['EN', 'us']) == Locale('en', 'US')
    assert utils.normalize_locale(['en', 'US', 'Texas']) == Locale('en', 'US')

    assert utils.normalize_locale('klingon') is None
    assert utils.normalize_locale(None) is None
    assert utils.normalize_locale(1) is None


def test_normalize_timezone():
    assert utils.normalize_timezone(timezone('America/Lima')) == timezone('America/Lima')
    assert utils.normalize_timezone('America/Lima') == timezone('America/Lima')
    assert utils.normalize_timezone('Mars') == None


def test_locale_to_str():
    assert utils.locale_to_str(Locale('en', 'US')) == 'en_US'
    assert utils.locale_to_str(Locale('es')) == 'es'
    assert utils.locale_to_str('en_US') == 'en_US'


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
    assert utils.get_request_locale(request, ['es']) == Locale('es')

    request.locale = 'en-US'
    assert utils.get_request_locale(request, ['en-US']) == Locale('en', 'US')

    request.locale = 'en_US'
    assert utils.get_request_locale(request, ['en_US']) == Locale('en', 'US')

    request.locale = Locale('en', 'US')
    assert utils.get_request_locale(request, ['en-US']) == Locale('en', 'US')

    request.locale = ('es', )
    assert utils.get_request_locale(request, ['es']) == Locale('es')

    request.locale = ('es', )
    assert utils.get_request_locale(request, []) == None

    request.locale = ('en', 'US')
    assert utils.get_request_locale(request, ['en-US']) == Locale('en', 'US')

    request.locale = 'En-Us'
    assert utils.get_request_locale(request, ['En-Us']) == Locale('en', 'US')

    request.locale = None
    assert utils.get_request_locale(request, ['es']) == None

    request.locale = 'klingon'
    assert utils.get_request_locale(request, ['es']) == None

    request.locale = 'klingon'
    assert (
        utils.get_request_locale(request, [utils.DEFAULT_LOCALE], default=utils.DEFAULT_LOCALE) ==
        utils.DEFAULT_LOCALE
    )
