# -*- coding: utf-8 -*-
import datetime as d
from decimal import Decimal
from os.path import join, dirname

from babel import Locale
from babel.dates import format_date, format_datetime, format_time
from babel.numbers import (format_currency, format_decimal, format_number,
    format_percent, format_scientific)
from jinja2 import Markup
import pytest
from pytz import timezone, UTC
try:
    from django.http import HttpRequest as DjangoRequest
except ImportError:
    pass
try:
    from webob import Request as WebobRequest
except ImportError:
    pass
from werkzeug.local import Local
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from allspeak import I18n


USE_WEBOB = False
USE_DJANGO = False

locales_dir = join(dirname(__file__), 'locales')


def test_search_paths():
    i18n = I18n(locales_dir)
    assert i18n.search_paths == [locales_dir]


def test_app_defaults():
    i18n = I18n(default_locale='es-PE', default_timezone='America/Lima')

    assert Locale('es', 'PE') == i18n.get_locale()
    assert timezone('America/Lima') == i18n.get_timezone()


def test_request_settings():
    request = get_test_request()
    request.locale = 'en'
    request.tzinfo = 'US/Eastern'
    get_request = lambda: request

    i18n = I18n(get_request=get_request, default_locale='es-PE',
        default_timezone='America/Lima')

    assert Locale.parse('en') == i18n.get_locale()
    assert timezone('US/Eastern') == i18n.get_timezone()


def test_content_negotiation():
    headers = [('Accept-Language', 'fr; q=1.0, es; q=0.5, pt; q=0.5')]
    request = get_test_request(headers=headers)
    get_request = lambda: request
    i18n = I18n(locales_dir, get_request)
    print i18n.available_languages

    assert Locale('es') == i18n.get_locale()

    headers = [('Accept-Language', 'fr; q=1.0, en-US; q=0.5, pt; q=0.5')]
    request = get_test_request(headers=headers)
    print request.headers
    get_request = lambda: request
    i18n = I18n(locales_dir, get_request)

    assert Locale('en') == i18n.get_locale()

    headers = [('Accept-Language', 'fr; q=1.0, es-PE; q=0.5, pt; q=0.5')]
    request = get_test_request(headers=headers)
    get_request = lambda: request
    i18n = I18n(locales_dir, get_request)

    assert Locale('es', 'PE') == i18n.get_locale()


def test_load_language():
    i18n = I18n(default_locale='fr')
    locale = Locale('es')

    data = i18n.load_language(locales_dir, Locale('es'))
    assert data['mytest']['greeting'] == u'Hola'
    data = i18n.load_language(locales_dir, Locale('es', 'PE'))
    assert data['mytest']['greeting'] == u'Habla'
    data = i18n.load_language(locales_dir, Locale('es', 'CO'))
    assert data['mytest']['greeting'] == u'Hola'
    data = i18n.load_language(locales_dir, Locale('pt'))
    assert data is None


def test_find_keypath():
    i18n = I18n(locales_dir)

    path, subkey = i18n.find_keypath('mytest.greeting')
    assert path == locales_dir
    assert subkey == 'mytest.greeting'

    path, subkey = i18n.find_keypath('sub:mytest.greeting')
    assert path == join(locales_dir, 'sub')
    assert subkey == 'mytest.greeting'


def test_key_lookup():
    i18n = I18n(locales_dir, default_locale='en')
    locale = Locale('es')

    assert i18n.key_lookup('mytest.greeting', locale) == u'Hola'
    assert i18n.key_lookup('mytest.bla', locale) == None
    assert i18n.key_lookup('sub:mytest.greeting', locale) == u'Hola mundo'


def test_translate():
    i18n = I18n(locales_dir, default_locale='es-PE')
    locale = Locale('es')

    assert i18n.translate('mytest.greeting', locale=locale) == u'Hola'
    assert i18n.translate('mytest.greeting') == u'Habla'
    assert i18n.translate('mytest.apple', 3, locale=locale) == u'Few apples'
    assert i18n.translate('mytest.apple', 10, locale=locale) == u'10 apples'
    assert i18n.translate('bla', locale=locale) == Markup(u'<missing:bla>')


def test_pluralize():
    i18n = I18n()
    d = {
        0: u'No apples',
        1: u'One apple',
        3: u'Few apples',
        'n': u'%(count)s apples',
    }
    assert i18n.pluralize(d, 0) == u'No apples'
    assert i18n.pluralize(d, 1) == u'One apple'
    assert i18n.pluralize(d, 3) == u'Few apples'
    assert i18n.pluralize(d, 10) == u'%(count)s apples'

    d = {
        0: u'off',
        'n': u'on'
    }
    assert i18n.pluralize(d, 3) == u'on'

    d = {
        0: u'off',
        'n': u'on'
    }
    assert i18n.pluralize(d, 0) == u'off'

    assert i18n.pluralize({}, 3) == u''


def test_to_user_timezone():
    i18n = I18n()
    tzinfo = timezone('US/Eastern')
    now = d.datetime.utcnow()
    result = i18n.to_user_timezone(now, tzinfo=tzinfo)
    expected = tzinfo.fromutc(now)
    assert result == expected


def test_to_utc():
    i18n = I18n()
    tzinfo = timezone('US/Eastern')
    now = d.datetime.utcnow()
    tznow = tzinfo.fromutc(now)
    assert i18n.to_utc(tznow) == now


def test_format():
    i18n = I18n()
    locale = 'en_US'
    tzinfo = UTC

    test_cases = [
        (456, format_number),
        (3.14159, format_decimal),
        (Decimal(3.14159), format_decimal),
    ]
    for value, bf in test_cases:
        assert i18n.format(value, locale=locale) == bf(value, locale=locale)

    test_cases = [
        (d.datetime(2012, 7, 28, 3, 4, 5), format_datetime),
        (d.date.today(), format_date),
        (d.time(3, 4, 5), format_time),
    ]
    for value, bf in test_cases:
        result = i18n.format(value, locale=locale, tzinfo=tzinfo)
        expected = bf(value, locale=locale)
        assert result == expected


def test_more_formatters():
    i18n = I18n()
    locale = 'en_US'
    v = 231.456

    result = i18n.format_currency(v, 'USD', locale=locale)
    expected = format_currency(v, 'USD', locale=locale)
    assert result == expected

    result = i18n.format_percent(v, locale=locale)
    expected = format_percent(v, locale=locale)
    assert result == expected
    
    result = i18n.format_scientific(v, locale=locale)
    expected = format_scientific(v, locale=locale)
    assert result == expected


# -----------------------------------------------------------------------------


def get_test_env(path, **kwargs):
    builder = EnvironBuilder(path=path, **kwargs)
    return builder.get_environ()


def get_test_request(path='/', **kwargs):
    env = get_test_env(path, **kwargs)
    if USE_WEBOB:
        return WebobRequest(dict(env))
    elif USE_DJANGO:
        request = DjangoRequest()
        request.path = path
        request.META = dict(env)
    return Request(env)

