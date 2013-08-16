# -*- coding: utf-8 -*-
from babel import Locale

from allspeak._compat import string_types


def normalize_locale(locale):
    if isinstance(locale, Locale):
        return locale
    if isinstance(locale, string_types):
        locale = locale.replace('_', '-')
        return Locale.parse(locale, sep='-')
    if isinstance(locale, tuple):
        return Locale(*locale)
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
