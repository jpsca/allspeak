# coding=utf-8
from babel import Locale
from babel.dates import UTC, get_timezone

from allspeak import RequestManager


def test_init():
    rm = RequestManager()
    assert rm.default_locale == Locale('en')
    assert rm.default_timezone == UTC


def test_set_defaults():
    rm = RequestManager(default_locale='es', default_timezone='America/Lima')
    assert rm.default_locale == Locale('es')
    assert rm.default_timezone == get_timezone('America/Lima')


def test_get_locale_default():
    locale = Locale('es')
    rm = RequestManager(default_locale=locale)
    assert rm.get_locale() == locale


def test_get_locale():
    locale = Locale('es', 'PE')
    default = Locale('en')
    available_locales = ['en', 'es_PE']
    rm = RequestManager(
        get_locale=lambda: locale, default_locale=default,
        available_locales=available_locales)
    assert rm.get_locale() == locale


def test_get_timezone_default():
    tzinfo = get_timezone('America/Lima')
    rm = RequestManager(default_timezone=tzinfo)
    assert rm.get_timezone() == tzinfo


def test_get_timezone():
    tzinfo = get_timezone('America/Lima')
    rm = RequestManager(get_timezone=lambda: tzinfo, default_timezone=UTC)
    assert rm.get_timezone() == tzinfo
