# -*- coding: utf-8 -*-
import re

from babel import Locale


# For parsing raw 'User-Agent' headers
_language_re = re.compile(
    r'(?:;\s*|\s+)(\b\w{2}\b(?:-\b\w{2}\b)?)\s*;|'
    r'(?:\(|\[|;)\s*(\b\w{2}\b(?:-\b\w{2}\b)?)\s*(?:\]|\)|;)'
)


def normalize_locale(locale):
    if isinstance(locale, Locale):
        return locale
    if isinstance(locale, basestring):
        locale = locale.replace('_', '-')
        return Locale.parse(locale, sep='-')
    if isinstance(locale, tuple):
        return Locale(*locale)
    return


def get_werkzeug_preferred_languages(request):
    """Return a list of preferred languages from a `werkzeug.wrappers.Request`
    instance.

    """
    languages = getattr(request, 'accept_languages', None)
    return languages.values() if languages else None


def get_webob_preferred_languages(request):
    """Return a list of preferred languages from a `webob.Request` instance.

    """
    languages = getattr(request, 'accept_language', None)
    return list(languages) if languages else None


def get_django_preferred_languages(request):
    """Take a `django.HttpRequest` instance and return a list of preferred
    languages from the headers.

    """
    meta = getattr(request, 'META', None)
    if not meta:
        return None
    header = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if not header:
        return None
    languages = [l.split(';')[0].strip() for l in header.split(',')]


def get_werkzeug_ua_language(request):
    """Return the language from the Werkzeug/Webob processed 'User-Agent'
    header.

    """
    ua = getattr(request, 'user_agent', None)
    if not ua:
        return None
    return getattr(request.user_agent, 'language', None)


def get_django_ua_language(request):
    """Take a `django.HttpRequest` instance and try to extract the language
    from the 'User-Agent' header.

    """
    meta = getattr(request, 'META', None)
    if not meta:
        return None
    header = request.META.get('HTTP_USER_AGENT')
    if not header:
        return None
    match = _language_re.search(header)
    if match is not None:
        return match.group(1) or match.group(2)
    return None

