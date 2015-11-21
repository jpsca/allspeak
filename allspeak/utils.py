# coding=utf-8
import datetime
from babel import Locale, UnknownLocaleError
from babel.dates import get_timezone, UTC

from ._compat import string_types


__all__ = [
    'LOCALES_FOLDER', 'DEFAULT_LOCALE', 'DEFAULT_TIMEZONE',
    'normalize_locale', 'normalize_timezone',
    'split_locale', 'locale_to_str',
]

LOCALES_FOLDER = 'locales'

DEFAULT_LOCALE = 'en'
DEFAULT_TIMEZONE = UTC


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


def _flatten(dic):
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
                for subkey, subvalue in _flatten(value).items():
                    yield str(key) + '.' + str(subkey), subvalue
            else:
                yield key, value

    return dict(items())


def _is_sequence(arg):
    return not hasattr(arg, "strip") and (
        hasattr(arg, "__getitem__") or hasattr(arg, "__iter__")
    )
