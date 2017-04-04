# coding=utf-8
from .utils import locale_to_str


__all__ = [
    'get_werkzeug_preferred_locales',
    'get_webob_preferred_locales',
    'get_django_preferred_locales',
]


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
    meta = getattr(request, 'META', None) or {}
    header = meta.get('HTTP_ACCEPT_LANGUAGE')
    if header:
        languages = [l.strip().split(';')[::-1] for l in header.split(',')]
        languages = sorted(languages)[::-1]
        return [locale_to_str(l[1]) for l in languages]
