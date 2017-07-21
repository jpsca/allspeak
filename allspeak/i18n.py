# coding=utf-8
from babel import Locale
from markupsafe import Markup

from . import utils
from ._compat import string_types
from .reader import Reader
from .request_manager import RequestManager


class I18n(RequestManager):

    """Internationalization functions.

    Uses the :class:`Reader` class to load and parse the translations files.

    :param folderpath: path that will be searched for the translations.

    :param get_locale: a callable that returns the current locale

    :param default_locale: default locale (as a string or as a
        Babel.Locale instance). This value will be accepted
        without checking if it's available.

    :param markup: overwrite the function used by `translate` to flags HTML
        code as 'safe'. `markupsafe.Markup` is used by default.

    """

    def __init__(self, folderpath=utils.LOCALES_FOLDER, markup=Markup, **kwargs):
        self.reader = Reader(folderpath)
        self.markup = markup
        self.load_translations()
        super(I18n, self).__init__(**kwargs)
        self._set_available_locales(self.translations.keys())

    def __repr__(self):
        return '{cname}()'.format(
            cname=self.__class__.__name__,
        )

    def __call__(self, *args, **kwargs):
        """Calling this instance is a shortcut to calling ``self.translate``.
        Useful when translating Sphinx documentation, that pickle the environment
        (a method of an instance isn't pickable, but an instance of a class is).
        """
        return self.translate(*args, **kwargs)

    @property
    def filepaths(self):
        return self.reader.filepaths

    def load_translations(self, *locales):
        self.translations = self.reader.load_translations(locales=locales)

    def get_translations_from_locale(self, locale):
        """Return the available translations for a locale: the
        country-specific (is defined) and the one for the language in general.

        :param locale: must be a :class:`babel.core.Locale` instance or a
            string.
        """
        strlocale = utils.locale_to_str(locale)
        if not self.translations or strlocale not in self.translations:
            self.load_translations(locale)

        objs = []
        trans = self.translations.get(strlocale)
        if trans:
            objs.append(trans)
        if '_' not in strlocale:
            return objs

        strlocale = strlocale.split('_')[0]
        trans = self.translations.get(strlocale)
        if trans:
            objs.append(trans)
        return objs

    def key_lookup(self, locale, key):
        """Return the value of the translation for the given key using the
        current locale. It tries first with the country-specific (eg `en-US`)
        translations (if the locale it's that specific) and then with those
        of the general language (eg. `en`).

        :param locale: must be a :class:`babel.core.Locale` instance or a
            string.
        :param key: a string, the ID of the looked up translation
        """
        translations = self.get_translations_from_locale(locale)
        if not translations:
            # Language not found!
            return None

        for trans in translations:
            for subkey in key.split('.'):
                value = trans.get(subkey)
                if value is None:
                    break
                trans = value
            if value is not None:
                return value
        return None

    def translate(self, key, count=None, locale=None, **kwargs):
        """Get the translation for the given key using the current locale.

        If the value is a dictionary, and `count` is defined, uses the value
        whose key is that number. If that key doesn't exist, a `'n'` key
        is tried instead. If that doesn't exits either, an empty string is
        returned.

        The final value is formatted using `kwargs` (and also `count` if
        available) so the format placeholders must be named instead of
        positional.

        If the value isn't a dictionary or a string, is returned as is.

        Examples:

            >>> translate('hello_world')
            'hello {what}'
            >>> translate('hello_world', what='world')
            'hello world'
            >>> translate('a_list', what='world')
            ['a', 'b', 'c']

        :param key: a string, the ID of the looked up translation
        :param count: If the value is a dictionary, and `count` is defined,
            uses the value whose key is that number. If that key doesn't exist,
            a `'n'` key is tried instead. If that doesn't exits either, an
            empty string is returned.
        :param locale: must be a :class:`babel.core.Locale` instance or a
            string.
        :param **kwargs: for string interpolation of the value.

        """
        key = str(key)
        locale = utils.normalize_locale(locale) or self.get_locale()
        value = self.key_lookup(locale, key)
        if value is None:
            return self.markup('<missing:{0}/>'.format(key))

        if isinstance(value, dict):
            value = pluralize(value, count, locale)

        if isinstance(value, string_types):
            kwargs.setdefault('count', count)
            value = value.format(**kwargs)
            return self.markup(value)

        return value

    @property
    def lazy_translate(self):

        class LazyWrapper(object):

            def __init__(self_, *args, **kwargs):
                self_.args = args
                self_.kwargs = kwargs

            def __repr__(self_):
                return self.translate(*self_.args, **self_.kwargs)

        return LazyWrapper

    def _set_available_locales(self, available_locales):
        _available = []
        for locale in available_locales or [self.default_locale]:
            lparts = utils.split_locale(locale)

            lp = '_'.join(lparts)
            if lp not in _available:
                _available.append(lp)

            if len(lparts) > 1:
                if lparts[0] not in _available:
                    _available.append(lparts[0])
        self.available_locales = _available

    def test_for_incomplete_locales(self, *locales):
        """Check a list of locales for keys that are defined in one but not in
        the other.

        :param locales: two or more locales as strings. If not provided, all
            of the available locales are tested.

        :return: a dictionary with strlocales as keys and sets of missing
            keys for those locales as values.

        """
        if not self.translations:
            self.load_translations(*locales)
        if not locales:
            locales = self.translations.keys()
        locales = [utils.locale_to_str(locale) for locale in locales]

        all_keys = []
        keys = {}
        for strlocale in locales:
            trans_keys = utils._flatten(self.translations.get(strlocale)).keys()
            keys[strlocale] = set(trans_keys)
            all_keys.extend(trans_keys)

        all_keys = set(all_keys)
        missing_keys = {}
        for key, value in keys.items():
            missing = all_keys - value
            if missing:
                missing_keys[key] = missing

        return missing_keys


def pluralize(dic, count, locale=utils.DEFAULT_LOCALE):
    """Takes a dictionary and a number and return the value whose key in
    the dictionary is either

        a. that number, or
        b. the textual representation of that number according to the `CLDR
           rules <cldr_rules>`_ for that locale, Depending of the language, this can be:
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
