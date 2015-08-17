# coding=utf-8
import datetime
from babel import Locale, UnknownLocaleError
from babel.dates import get_timezone, UTC

from ._compat import string_types


LOCALES_FOLDER = 'locales'

DEFAULT_LOCALE = 'en'
DEFAULT_TIMEZONE = UTC

DEFAULT_DATE_FORMATS = {
    'time': 'medium',
    'date': 'medium',
    'datetime': 'medium',
}


def get_request_locale(request, available_locales, default=None):
    """Returns the locale that should be used for this request as a
    `babel.Locale` instance.

    Tries the following in order:

    - an request attribute called `'locale'`
    - a GET argument called `'locale'`
    - the prefered
    - the default locale

    """
    if not available_locales:
        return None
    locale = (
        getattr(request, 'locale', None) or
        getattr(request, 'args', getattr(request, 'GET', {})).get('locale')
    )
    if locale:
        preferred = [locale]
    else:
        preferred = get_preferred_locales(request)

    locale = negotiate_locale(preferred, available_locales)
    request.locale = normalize_locale(locale) or default
    return request.locale


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


def get_preferred_locales(request):
    """Extract from the request a list of preferred strlocales.
    """
    return (
        get_werkzeug_preferred_locales(request) or
        get_webob_preferred_locales(request) or
        get_django_preferred_locales(request) or
        []
    )


def get_werkzeug_preferred_locales(request):
    """Return a list of preferred languages from a `werkzeug.wrappers.Request`
    instance.

    """
    languages = getattr(request, 'accept_languages', None)
    if languages:
        return [locale_to_str(l) for l in languages.values()]


def get_webob_preferred_locales(request):
    """Return a list of preferred languages from a `webob.Request` instance.

    """
    languages = getattr(request, 'accept_language', None)
    if languages:
        return [locale_to_str(l) for l in languages]


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
        return [locale_to_str(l[1]) for l in languages]


def negotiate_locale(preferred, available):
    """From the available locales, negotiate the most adequate for the
    client, based on the "accept language" header.
    """
    preferred = map(locale_to_str, preferred)
    available = map(locale_to_str, available)
    # To ensure a consistent matching, Babel algorithm is used.
    return Locale.negotiate(preferred, available, sep='_')


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


def normalize_timezone(tzinfo):
    if not tzinfo:
        return
    if isinstance(tzinfo, datetime.tzinfo):
        return tzinfo
    try:
        return get_timezone(tzinfo)
    except LookupError:
        return


def split_locale(locale):
    """Returns a tuple (language, TERRITORY) or just (language, )
    from a a :class:`babel.core.Locale` instance or a string like `en-US` or
    `en_US`.
    """
    if isinstance(locale, Locale):
        tloc = [locale.language.lower()]
        if locale.territory:
            tloc.append(locale.territory.upper())
        return tuple(tloc)

    if isinstance(locale, string_types):
        locale = locale.replace('-', '_').lower().strip()
        tloc = locale.split('_')
        if len(tloc) > 1:
            tloc[-1] = tloc[-1].upper()
        return tuple(tloc)

    return locale


def locale_to_str(locale):
    return '_'.join(split_locale(locale))


def flatten(dic):
    """Flatten a dictionary, separating keys by dots.

    >>>> dic = {
        'a': 1,
        'c': {
            'a': 2,
            'b': {
                'x': 5,
                'y' : 10,
            }
        },
        'd': [1, 2, 3],
    }
    >>>> flatten(dic)
    {'a': 1, 'c.a': 2, 'c.b.x': 5, 'c.b.y': 10, 'd': [1, 2, 3]}

    """
    def items():
        for key, value in dic.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten(value).items():
                    yield str(key) + '.' + str(subkey), subvalue
            else:
                yield key, value

    return dict(items())
