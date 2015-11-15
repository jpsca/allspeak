# coding=utf-8
from babel import Locale
from babel.dates import UTC, get_timezone

from allspeak import RequestManager

from .conftest import make_get_request


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


def test_get_locale_from_request():
    default = Locale('ru')

    get_request = make_get_request(locale='es')
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['es']
    )
    assert rm.get_locale() == Locale('es')

    get_request = make_get_request(locale='en-US')
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['en-US']
    )
    assert rm.get_locale() == Locale('en', 'US')

    get_request = make_get_request(locale='en_US')
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['en_US']
    )
    assert rm.get_locale() == Locale('en', 'US')

    get_request = make_get_request(locale=Locale('en', 'US'))
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['en-US']
    )
    assert rm.get_locale() == Locale('en', 'US')

    get_request = make_get_request(locale=('es', ))
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['es']
    )
    assert rm.get_locale() == Locale('es')

    get_request = make_get_request(locale=('es', ))
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=[]
    )
    assert rm.get_locale() == default

    get_request = make_get_request(locale=('en', 'US'))
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['en-US']
    )
    assert rm.get_locale() == Locale('en', 'US')

    get_request = make_get_request(locale='En-Us')
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['En-Us']
    )
    assert rm.get_locale() == Locale('en', 'US')

    get_request = make_get_request(locale=None)
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['es']
    )
    assert rm.get_locale() == default

    get_request = make_get_request(locale='klingon')
    rm = RequestManager(
        get_request=get_request,
        default_locale=default,
        available_locales=['es']
    )
    assert rm.get_locale() == default


def test_get_locale_from_request_invalid():
    locale = None
    default = Locale('en')
    get_request = make_get_request(locale=locale)
    available_locales = ['en', 'es_PE']
    rm = RequestManager(
        get_request=get_request, default_locale=default,
        available_locales=available_locales)
    assert rm.get_locale() == default


def test_get_locale_from_request_unavailable():
    locale = None
    default = Locale('en')
    get_request = make_get_request(locale=locale)
    available_locales = []
    rm = RequestManager(
        get_request=get_request, default_locale=default,
        available_locales=available_locales)
    assert rm.get_locale() == default


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


def test_get_timezone():
    tzinfo = get_timezone('America/Lima')
    rm = RequestManager(get_timezone=lambda: tzinfo, default_timezone=UTC)
    assert rm.get_timezone() == tzinfo
