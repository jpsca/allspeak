# -*- coding: utf-8 -*-
from babel import Locale, UnknownLocaleError
from pytz import timezone, UTC

from allspeak._compat import string_types


def normalize_locale(locale):
    if isinstance(locale, Locale):
        return locale
    try:
        if isinstance(locale, string_types):
            locale = locale.replace('_', '-')
            return Locale.parse(locale, sep='-')
        if isinstance(locale, tuple):
            return Locale(*locale)
    except UnknownLocaleError:
        return


def get_werkzeug_preferred_locales(request):
    """Return a list of preferred languages from a `werkzeug.wrappers.Request`
    instance.

    """
    languages = getattr(request, 'accept_languages', None)
    if languages:
        return list(languages.values())


def get_webob_preferred_locales(request):
    """Return a list of preferred languages from a `webob.Request` instance.

    """
    languages = getattr(request, 'accept_language', None)
    if languages:
        return list(languages)


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
        return [l[1].strip() for l in languages]


def get_preferred_locales(request):
    return (get_werkzeug_preferred_locales(request) or
            get_webob_preferred_locales(request) or
            get_django_preferred_locales(request))


def negotiate_locale(request, available_locales):
    """From the available locales, negotiate the most adequate for the
    client, based on the "accept language" header.
    """
    preferred = get_preferred_locales(request)
    if preferred:
        available_locales = map(
            lambda l: l.replace('_', '-'),
            available_locales
        )
        # To ensure a consistent matching, Babel algorithm is used.
        return Locale.negotiate(preferred, available_locales, sep='-')


def get_request_timezone(request, default=UTC):
    """Returns the timezone that should be used for this request as a
    `DstTzInfo` instance.

    Tries the following in order:
    - an attribute called `'tzinfo'`
    - a GET argument called `'tzinfo'`
    - the provided default timezone

    """
    tzinfo = (
        getattr(request, 'tzinfo', None) or
        getattr(request, 'args', getattr(
                request, 'GET', {})).get('tzinfo')
    ) or default

    if isinstance(tzinfo, string_types):
        tzinfo = timezone(tzinfo)
    request.tzinfo = tzinfo
    return request.tzinfo


def get_request_locale(request, default):
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
