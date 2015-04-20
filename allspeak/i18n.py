# coding=utf-8
from markupsafe import Markup

from . import utils
from ._compat import string_types
from .reader import Reader
from .request_manager import RequestManager
from .utils import locale_to_str


class I18n(RequestManager):
    """Internationalization functions.

    Uses the :class:`Reader` class to load and parse the translations files.

    :param folderpath: path that will be searched for the translations.

    :param markup: overwrite the function used by `translate` to flags HTML
        code as 'safe'. `markupsafe.Markup` is used by default.

    :param get_request: a callable that returns the current request.

    :param default_locale: default locale (as a string or as a
        Babel.Locale instance).

    :param default_timezone: default timezone (as a string or as a
        `datetime.tzinfo` instance).

    :param date_formats: update the defaults date formats.
    """

    def __init__(self, folderpath=utils.LOCALES_FOLDER, markup=Markup, **kwargs):
        self.reader = Reader(folderpath)
        self.markup = markup
        super(I18n, self).__init__(**kwargs)

    def __repr__(self):
        return '{cname}()'.format(
            cname=self.__class__.__name__,
        )

    def load_translations(self, locale=None):
        self.translations = self.reader.load_translations(locale=locale)

    def get_translations_from_locale(self, locale):
        """Return the available translations for a locale: the
        country-specific (is defined) and the one for the language in general.

        :param locale: must be a :class:`babel.core.Locale` instance
        """
        if not self.translations:
            self.load_translations(locale)

        objs = []
        strlocale = locale_to_str(locale)
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

        :param locale: must be a :class:`babel.core.Locale` instance
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
        whose key is that number.  If that key doesn't exist, a `'n'` key
        is tried instead.  If that doesn't exits either, an empty string is
        returned.

        The final value is formatted using `kwargs` (and also `count` if
        available) so the format placeholders must be named instead of
        positional.

        If the value isn't a dictionary or a string, is returned as is.

        Examples:

            >>> translate('hello_world')
            'hello %(what)s'
            >>> translate('hello_world', what='world')
            'hello world'
            >>> translate('a_list', what='world')
            ['a', 'b', 'c']

        """
        key = str(key)
        locale = utils.normalize_locale(locale) or self.get_locale()
        value = self.key_lookup(locale, key)
        if value is None:
            return self.markup('<missing:%s>' % (key, ))

        if isinstance(value, dict):
            value = utils.pluralize(value, count)

        if isinstance(value, string_types):
            kwargs.setdefault('count', count)
            value = value % kwargs
            if key.endswith('_html'):
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
