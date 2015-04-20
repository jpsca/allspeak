# coding=utf-8
import datetime
from babel import Locale, UnknownLocaleError
from babel.dates import get_timezone, UTC

from ._compat import string_types


__all__ = [
    'LOCALES_FOLDER', 'DEFAULT_LOCALE', 'DEFAULT_TIMEZONE',
    'DEFAULT_DATE_FORMATS', 'normalize_locale', 'normalize_timezone',
    'get_werkzeug_preferred_locales', 'get_webob_preferred_locales',
    'get_django_preferred_locales', 'get_preferred_locales', 'negotiate_locale',
    'get_request_timezone', 'get_request_locale', 'pluralize',
]

LOCALES_FOLDER = 'locales'

DEFAULT_LOCALE = 'en'
DEFAULT_TIMEZONE = UTC

DEFAULT_DATE_FORMATS = {
    'time': 'medium',
    'date': 'medium',
    'datetime': 'medium',
}


def split_locale(locale):
    """Returns a tuple (language, TERRITORY) or just (language, )
    from a a `~Babel.Locale` instance or a string like `en-US` or `en_US`.
    """
    if isinstance(locale, Locale):
        tloc = [locale.language.lower()]
        if locale.territory:
            tloc.append(locale.territory.upper())
        return tuple(tloc)

    if isinstance(locale, string_types):
        locale = locale.replace('-', '_').lower()
        tloc = locale.split('_')
        if len(tloc) > 1:
            tloc[-1] = tloc[-1].upper()
        return tuple(tloc)

    return locale


def normalize_locale(locale):
    if not locale:
        return
    if isinstance(locale, Locale):
        return locale

    locale = split_locale(locale)

    if isinstance(locale, (tuple, list)):
        try:
            if len(locale) == 1:
                return Locale(locale[0].lower())
            else:
                return Locale(locale[0].lower(), locale[1].upper())
        except UnknownLocaleError:
            return None
    return None


def normalize_timezone(tzinfo):
    if not tzinfo:
        return
    if isinstance(tzinfo, datetime.tzinfo):
        return tzinfo
    try:
        return get_timezone(tzinfo)
    except LookupError:
        return


def locale_to_str(locale):
    if not isinstance(locale, Locale):
        return locale
    strlocale = locale.language.lower()
    if locale.territory:
        strlocale += '_' + locale.territory.upper()
    return strlocale


def get_werkzeug_preferred_locales(request):
    """Return a list of preferred languages from a `werkzeug.wrappers.Request`
    instance.

    """
    languages = getattr(request, 'accept_languages', None)
    if languages:
        return [
            '_'.join(split_locale(l))
            for l in languages.values()
        ]


def get_webob_preferred_locales(request):
    """Return a list of preferred languages from a `webob.Request` instance.

    """
    languages = getattr(request, 'accept_language', None)
    if languages:
        return [
            '_'.join(split_locale(l))
            for l in languages
        ]


def get_django_preferred_locales(request):
    """Take a `django.HttpRequest` instance and return a list of preferred
    languages from the headers.

    """
    meta = getattr(request, 'META', None)
    if not meta:
        return None
    header = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if header:
        languages = [l.strip().split(';')[::-1] for l in header.split(',')]
        languages = sorted(languages)[::-1]
        return [
            '_'.join(split_locale(l[1].strip()))
            for l in languages
        ]


def get_preferred_locales(request):
    """Extract from the request a list of preferred strlocales.
    """
    return (
        get_werkzeug_preferred_locales(request) or
        get_webob_preferred_locales(request) or
        get_django_preferred_locales(request) or
        []
    )


def negotiate_locale(request, available_locales):
    """From the available locales, negotiate the most adequate for the
    client, based on the "accept language" header.
    """
    if not available_locales:
        return None
    preferred = get_preferred_locales(request)
    if preferred:
        preferred = map(
            lambda l: l.replace('-', '_').lower(),
            preferred
        )
        available_locales = map(
            lambda l: l.replace('-', '_').lower(),
            available_locales
        )
        # To ensure a consistent matching, Babel algorithm is used.
        return Locale.negotiate(preferred, available_locales, sep='_')


def get_request_timezone(request, default=None):
    """Returns the timezone that should be used for this request as a
    `datetime.tzinfo` instance.

    Tries the following in order:

    - an attribute called `'tzinfo'`
    - a GET argument called `'tzinfo'`
    - the provided default timezone

    """
    tzinfo = (
        getattr(request, 'tzinfo', None) or
        getattr(request, 'args', getattr(
                request, 'GET', {})).get('tzinfo')
    )
    request.tzinfo = normalize_timezone(tzinfo) or default
    return request.tzinfo


def get_request_locale(request, default=None):
    """Returns the locale that should be used for this request as a
    `babel.Locale` instance.

    Tries the following in order:

    - an request attribute called `'locale'`
    - a GET argument called `'locale'`
    - the default locale

    """
    locale = (
        getattr(request, 'locale', None) or
        getattr(request, 'args', getattr(request, 'GET', {})).get('locale')
    )
    request.locale = normalize_locale(locale) or default
    return request.locale


def pluralize(dic, count):
    """Takes a dictionary and a number and return the value whose key in
    the dictionary is that number.  If that key doesn't exist, a `'n'` key
    is tried instead.  If that doesn't exits either, an empty string is
    returned.  Examples:

    >>> dic = {
        0: u'No apples',
        1: u'One apple',
        3: u'Few apples',
        'n': u'%(count)s apples',
        }
    >>> pluralize(dic, 0)
    'No apples'
    >>> pluralize(dic, 1)
    'One apple'
    >>> pluralize(dic, 3)
    'Few apples'
    >>> pluralize(dic, 10)
    '%(count)s apples'
    >>> pluralize({0: 'off', 'n': 'on'}, 3)
    'on'
    >>> pluralize({0: 'off', 'n': 'on'}, 0)
    'off'
    >>> pluralize({}, 3)
    ''

    """
    if count is None:
        count = 0
    scount = str(count)
    return dic.get(count, dic.get(scount, dic.get('n', u'')))
