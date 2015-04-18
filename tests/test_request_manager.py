# coding=utf-8
from babel import Locale
from babel.dates import UTC, get_timezone

from allspeak import RequestManager

from .conftest import make_get_request


def test_init():
    rm = RequestManager()
    assert rm.default_locale == Locale('en')
    assert rm.default_timezone == UTC


def test_init_defaults():
    rm = RequestManager(default_locale='es', default_timezone='America/Lima')
    assert rm.default_locale == Locale('es')
    assert rm.default_timezone == get_timezone('America/Lima')


def test_get_locale_default():
    locale = Locale('es')
    rm = RequestManager(default_locale=locale)
    assert rm.get_locale() == locale


def test_get_locale_from_request():
    locale = Locale('es', 'PE')
    default = Locale('en')
    get_request = make_get_request(locale=locale)
    rm = RequestManager(get_request=get_request, default_locale=default)
    assert rm.get_locale() == locale


def test_get_locale_from_request_invalid():
    locale = None
    default = Locale('en')
    get_request = make_get_request(locale=locale)
    rm = RequestManager(get_request=get_request, default_locale=default)
    assert rm.get_locale() == default


def test_get_timezone_default():
    tzinfo = get_timezone('America/Lima')
    rm = RequestManager(default_timezone=tzinfo)
    assert rm.get_timezone() == tzinfo


def test_get_timezone_from_request():
    tzinfo = get_timezone('America/Lima')
    default = UTC
    get_request = make_get_request(tzinfo=tzinfo)
    rm = RequestManager(get_request=get_request, default_timezone=default)
    assert rm.get_timezone() == tzinfo


def test_get_timezone_from_request_invalid():
    tzinfo = None
    default = UTC
    get_request = make_get_request(tzinfo=tzinfo)
    rm = RequestManager(get_request=get_request, default_timezone=default)
    assert rm.get_timezone() == default
