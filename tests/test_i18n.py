# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime as d
from decimal import Decimal
from os.path import join, dirname

from babel import Locale
from babel.dates import format_date, format_datetime, format_time
from babel.numbers import (
    format_currency, format_decimal, format_number,
    format_percent, format_scientific)
from markupsafe import Markup
from pytz import timezone, UTC
from werkzeug.test import EnvironBuilder

from allspeak import I18n


USE_WEBOB = False
USE_DJANGO = False

locales_dir = join(dirname(__file__), 'locales')


def get_test_env(path, **kwargs):
    builder = EnvironBuilder(path=path, **kwargs)
    return builder.get_environ()


def get_test_request(make_req, path='/', **kwargs):
    env = get_test_env(path, **kwargs)
    return make_req(env, path)


def test_search_paths():
    i18n = I18n(locales_dir)
    assert i18n.search_paths == [locales_dir]


def test_app_defaults():
    i18n = I18n(default_locale='es-PE', default_timezone='America/Lima')
    assert True
    assert Locale('es', 'PE') == i18n.get_locale()
    assert timezone('America/Lima') == i18n.get_timezone()


def test_overwrite_date_formats():
    i18n = I18n(date_formats={'date': 'fizzbuzz'})
    assert i18n.date_formats['date'] == 'fizzbuzz'


def test_request_settings(make_req):
    request = get_test_request(make_req)
    request.locale = 'en'
    request.tzinfo = 'US/Eastern'
    get_request = lambda: request

    i18n = I18n(get_request=get_request, default_locale='es-PE',
                default_timezone='America/Lima')

    assert Locale.parse('en') == i18n.get_locale()
    assert timezone('US/Eastern') == i18n.get_timezone()


def test_no_preffered_language(make_req):
    request = get_test_request(make_req, headers=[])
    get_request = lambda: request
    i18n = I18n(locales_dir, get_request, default_locale='es')
    assert Locale('es') == i18n.get_locale()


def test_load_language():
    i18n = I18n(default_locale='fr')

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
    assert i18n.key_lookup('mytest.bla', locale) is None
    assert i18n.key_lookup('sub:mytest.greeting', locale) == u'Hola mundo'


def test_translate():
    i18n = I18n(locales_dir, default_locale='es-PE')
    locale = Locale('es')

    assert i18n.translate('mytest.greeting', locale=locale) == u'Hola'
    assert i18n.translate('mytest.greeting') == u'Habla'
    assert i18n.translate('mytest.apple', 3, locale=locale) == u'Few apples'
    assert i18n.translate('mytest.apple', 10, locale=locale) == u'10 apples'
    assert i18n.translate('bla', locale=locale) == Markup(u'<missing:bla>')


def test_lazy_translate():
    i18n = I18n(locales_dir, default_locale='es-PE')
    locale = Locale('es')

    lazy = i18n.lazy_translate('mytest.greeting', locale=locale)
    assert lazy != u'Hola'
    assert repr(lazy) == u'Hola'


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
        (Decimal('3.14159'), format_decimal),
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
