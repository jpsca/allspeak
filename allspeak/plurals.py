# coding=utf-8
from babel import Locale

from ._compat import string_types
from .utils import DEFAULT_LOCALE


def pluralize(dic, count, locale=DEFAULT_LOCALE):
    """Takes a dictionary and a number and return the value whose key in
    the dictionary is either

        a. that number, or
        b. the textual representation of that number according to the CLDR
           rules_ for that locale, Dependending of the language, this can be:
           "zero", "one", "two", "few", "many" or "other".

    ..  rules: http://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html

    As a deviation of the standard:

    - If ``count`` is 0, a `'zero'` is tried
    - If the textual representation is `'other'` but that key doesn't exists, a
      `'many'` key is tried instead.

    Finally, if none of these exits, an empty string is returned.

    Examples:

    >>> dic = {
            0: u'No apples',
            1: u'One apple',
            3: u'Few apples',
            'many': u'{count} apples',
        }
    >>> pluralize(dic, 0)
    'No apples'
    >>> pluralize(dic, 1)
    'One apple'
    >>> pluralize(dic, 3)
    'Few apples'
    >>> pluralize(dic, 10)
    '{count} apples'

    >>> dic = {
            'zero': u'No apples whatsoever',
            'one': u'One apple',
            'other': u'{count} apples',
        }
    >>> pluralize(dic, 0)
    u'No apples whatsoever'
    >>> pluralize(dic, 1)
    'One apple'
    >>> pluralize(dic, 2)
    '{count} apples'
    >>> pluralize(dic, 10)
    '{count} apples'

    >>> pluralize({0: 'off', 'many': 'on'}, 3)
    'on'
    >>> pluralize({0: 'off', 'other': 'on'}, 0)
    'off'
    >>> pluralize({0: 'off', 'other': 'on'}, 456)
    'on'
    >>> pluralize({}, 3)


    Note that this function **does not** interpolate the string, just returns
    the right one for the value of ``count``.
    """
    count = int(count or 0)
    scount = str(count).strip()
    plural = dic.get(count, dic.get(scount))
    if plural is not None:
        return plural

    if count == 0:
        plural = dic.get('zero')
        if plural is not None:
            return plural

    if isinstance(locale, string_types):
        locale = Locale(locale)
    literal = locale.plural_form(count)
    return dic.get(literal, dic.get('many', u''))
