# -*- coding: utf-8 -*-
import datetime as dt
import os
from decimal import Decimal
from os.path import join, dirname, realpath, abspath, normpath, isdir, isfile

from babel import dates, numbers, Locale
from markupsafe import Markup
from pytz import timezone, UTC

from allspeak import utils
from allspeak._compat import string_types
from allspeak.reader import get_data


LOCALES_DIR = 'locales'

DEFAULT_DATE_FORMATS = {
    'time': 'medium',
    'date': 'medium',
    'datetime': 'medium',
}

DEFAULT_LOCALE = 'en'


class I18n(object):

    def __init__(self, locales_dirs=None, get_request=None,
                 default_locale=DEFAULT_LOCALE, default_timezone=None,
                 date_formats=None, markup=Markup):
        """
        locales_dirs:
            list of paths that will be searched, in order,
            for the locales.

        get_request:
            a callable that returns the current request.

        default_locale:
            default locale (as a string or as a Babel.Locale instance).

        default_timezone:
            default timezone.

        date_formats:
            overwrite the defaults date formats.

        markup:
            overwrite the function used by `translate` to flags HTML code
            as 'safe'. `markupsafe.Markup` is used by default.

        """
        self.get_request = get_request

        if isinstance(locales_dirs, string_types):
            locales_dirs = [locales_dirs]
        locales_dirs = locales_dirs or [LOCALES_DIR]
        search_paths = []
        for p in locales_dirs:
            p = normpath(abspath(realpath(p)))
            if not isdir(p):
                p = dirname(p)
            search_paths.append(p)
        self.search_paths = search_paths
        self.set_defaults(default_locale, default_timezone)
        self.date_formats = DEFAULT_DATE_FORMATS.copy()
        if date_formats:
            self.date_formats.update(date_formats)
        self.markup = markup
        self.translations = {}

    def set_defaults(self, default_locale, default_timezone):
        """Set the default locale from the configuration as an instance of
        `Babel.Locale` and the default timezone as a `pytz.timezone` object.

        """
        default_locale = utils.normalize_locale(default_locale) or Locale(DEFAULT_LOCALE)
        self.default_locale = default_locale
        self.default_timezone = timezone(default_timezone or 'utc')

    def get_locale(self):
        """Returns the locale that should be used for this request as
        an instance of `Babel.Locale`.
        This returns the default locale if used outside of a request.

        """
        request = self.get_request and self.get_request()
        if not request:
            return self.default_locale
        return utils.get_request_locale(request, self.default_locale)

    def get_timezone(self):
        """Returns the timezone that should be used for this request as
        `pytz.timezone` object.  This returns the default timezone if used
        outside of a request or if no timezone was defined.

        """
        request = self.get_request and self.get_request()
        if not request:
            return self.default_timezone
        return utils.get_request_timezone(request, self.default_timezone)

    def load_language(self, path, locale):
        """From the given `path`, load the language file for the current or
        given locale.  If the locale has a territory attribute (eg: 'US') the
        the specific 'en-US' version will be tried first.

        """
        if locale.territory:
            filenames = [str(locale).replace('_', '-'), locale.language]
        else:
            filenames = [locale.language]
        filenames.append(str(self.default_locale).replace('_', '-'))

        for filename in filenames:
            cache_key = join(path, filename)
            cached = self.translations.get(cache_key)
            if cached:
                return cached
            filename = cache_key + '.yml'
            if isfile(filename):
                break
        else:
            return
        try:
            data = get_data(filename)
        except (IOError, AttributeError):
            return
        self.translations[cache_key] = data
        return data

    def find_keypath(self, key):
        """Based on the `key`, teturn the path of the language file and the
        subkey inside that file.

        """
        if ':' not in key:
            return self.search_paths[0], key

        path, subkey = key.split(':', 1)
        lpath = path.split('.')

        for root in self.search_paths:
            dirname, dirnames, filenames = next(os.walk(root))
            if lpath[0] in dirnames:
                break
        else:
            return None, None

        path = join(root, *lpath)
        if not isdir(path):
            return None, None
        return path, subkey

    def key_lookup(self, key, locale):
        """
        """
        path, subkey = self.find_keypath(key)
        if not (path and subkey):
            return None

        value = self.load_language(path, locale)
        if value is None:
            return None

        try:
            for k in subkey.split('.'):
                value = value.get(k)
                if value is None:
                    return None
            return value
        except (IndexError, ValueError):
            return None

    def translate(self, key, count=None, locale=None, **kwargs):
        """Load the translation for the given key using the current locale.

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
        value = self.key_lookup(key, locale)
        if not value:
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

    def to_user_timezone(self, datetime, tzinfo=None):
        """Convert a datetime object to the user's timezone.  This
        automatically happens on all date formatting unless rebasing is
        disabled.  If you need to convert a `datetime.datetime` object at any
        time to the user's timezone (as returned by `get_timezone` this
        function can be used).

        """
        if datetime.tzinfo is None:
            datetime = datetime.replace(tzinfo=UTC)
        tzinfo = tzinfo or self.get_timezone()
        return tzinfo.normalize(datetime.astimezone(tzinfo))

    def to_utc(self, datetime, tzinfo=None):
        """Convert a datetime object to UTC and drop tzinfo.  This is the
        opposite operation to `to_user_timezone`.

        """
        if datetime.tzinfo is None:
            tzinfo = tzinfo or self.get_timezone()
            datetime = tzinfo.localize(datetime)
        return datetime.astimezone(UTC).replace(tzinfo=None)

    def _get_format(self, key, format):
        """A small helper for the datetime formatting functions.  Looks up
        format defaults for different kinds.

        """
        if format is None:
            format = self.date_formats.get(key)
        if format in ('short', 'medium', 'full', 'long'):
            rv = self.date_formats.get('%s.%s' % (key, format))
            if rv is not None:
                format = rv
        return format

    def _date_format(self, formatter, obj, format, rebase,
                     locale=None, tzinfo=None, **extra):
        """Internal helper that formats the date.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        extra = {}
        if formatter is not dates.format_date and rebase:
            extra['tzinfo'] = tzinfo or self.get_timezone()
        return formatter(obj, format, locale=locale, **extra)

    def format(self, value, *args, **kwargs):
        """Return a formatted `value` according to the detected type and
        given parameters.  It doesn't know anything about currency, percent or
        scientific formats, so use the other methods for those cases.

        """
        locale = kwargs.pop('locale', None)
        tzinfo = kwargs.pop('tzinfo', None)

        if isinstance(value, dt.date):
            if isinstance(value, dt.datetime):
                return self.format_datetime(value, locale=locale,
                                            tzinfo=tzinfo, *args, **kwargs)
            else:
                return self.format_date(value, locale=locale, tzinfo=tzinfo,
                                        *args, **kwargs)

        if isinstance(value, int):
            return self.format_number(value, locale=locale, *args, **kwargs)
        if isinstance(value, (float, Decimal)):
            return self.format_decimal(value, locale=locale, *args, **kwargs)

        if isinstance(value, dt.time):
            return self.format_time(value, locale=locale, tzinfo=tzinfo,
                                    *args, **kwargs)
        if isinstance(value, dt.timedelta):
            return self.format_timedelta(value, locale=locale, *args, **kwargs)

        return value

    def format_datetime(self, datetime=None, format=None, rebase=True,
                        locale=None, tzinfo=None):
        """Return a date formatted according to the given pattern.  If no
        `datetime.datetime` object is passed, the current time is
        assumed.  By default rebasing happens which causes the object to
        be converted to the users's timezone (as returned by
        `to_user_timezone`).  This function formats both date and
        time.

        The format parameter can either be `'short'`, `'medium'`,
        `'long'` or `'full'` (in which cause the language's default for
        that setting is used, or the default from the `Babel.date_formats`
        mapping is used) or a format string as documented by Babel.

        This function is also available in the template context as filter
        named `datetimeformat`.

        """
        format = self._get_format('datetime', format)
        return self._date_format(dates.format_datetime, datetime, format,
                                 rebase, locale=locale, tzinfo=tzinfo)

    def format_date(self, date=None, format=None, rebase=True,
                    locale=None, tzinfo=None):
        """Return a date formatted according to the given pattern.  If no
        `datetime.datetime` or `datetime.date` object is passed,
        the current time is assumed.  By default rebasing happens which causes
        the object to be converted to the users's timezone (as returned by
        `to_user_timezone`).  This function only formats the date part
        of a `datetime.datetime` object.

        The format parameter can either be `'short'`, `'medium'`,
        `'long'` or `'full'` (in which cause the language's default for
        that setting is used, or the default from the `Babel.date_formats`
        mapping is used) or a format string as documented by Babel.

        This function is also available in the template context as filter
        named `dateformat`.

        """
        if rebase and isinstance(date, dt.datetime):
            date = self.to_user_timezone(date, tzinfo=tzinfo)
        format = self._get_format('date', format)
        return self._date_format(dates.format_date, date, format, rebase,
                                 locale=locale, tzinfo=tzinfo)

    def format_time(self, time=None, format=None, rebase=True,
                    locale=None, tzinfo=None):
        """Return a time formatted according to the given pattern.  If no
        `datetime.datetime` object is passed, the current time is
        assumed.  By default rebasing happens which causes the object to
        be converted to the users's timezone (as returned by
        `to_user_timezone`).  This function formats both date and
        time.

        The format parameter can either be `'short'`, `'medium'`,
        `'long'` or `'full'` (in which cause the language's default for
        that setting is used, or the default from the Babel.date_formats`
        mapping is used) or a format string as documented by Babel.

        This function is also available in the template context as filter
        named `timeformat`.

        """
        format = self._get_format('time', format)
        return self._date_format(dates.format_time, time, format, rebase,
                                 locale=locale, tzinfo=tzinfo)

    def format_timedelta(self, datetime_or_timedelta, granularity='second',
                         locale=None):
        """Format the elapsed time from the given date to now or the given
        timedelta.

        This function is also available in the template context as filter
        named `timedeltaformat`.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        if isinstance(datetime_or_timedelta, dt.datetime):
            datetime_or_timedelta = dt.datetime.utcnow(
            ) - datetime_or_timedelta
        return dates.format_timedelta(datetime_or_timedelta, granularity,
                                      locale=locale)

    def format_number(self, number, locale=None):
        """Return the given number formatted for the locale in the
        current request.

        number:
            the number to format

        return (unicode):
            the formatted number

        This function is also available in the template context as filter
        named `numberformat`.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_number(number, locale=locale)

    def format_decimal(self, number, format=None, locale=None):
        """Return the given decimal number formatted for the locale in the
        current request.

        number:
            the number to format
        format:
            the format to use

        return (unicode):
            the formatted number

        This function is also available in the template context as filter
        named `decimalformat`.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_decimal(number, format=format, locale=locale)

    def format_currency(self, number, currency, format=None, locale=None):
        """Return the given number formatted for the locale in the
        current request.

        number:
            the number to format
        currency:
            the currency code
        format:
            the format to use

        return (unicode):
            the formatted number

        This function is also available in the template context as filter
        named `currencyformat`.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_currency(
            number, currency, format=format, locale=locale
        )

    def format_percent(self, number, format=None, locale=None):
        """Return a percent value formatted for the locale in the
        current request.

        number:
            the number to format
        format:
            the format to use

        return (unicode):
            the formatted percent number

        This function is also available in the template context as filter
        named `percentformat`.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_percent(number, format=format, locale=locale)

    def format_scientific(self, number, format=None, locale=None):
        """Return value formatted in scientific notation for the locale in
        the current request.

        number:
            the number to format
        format:
            the format to use

        return (unicode):
            the formatted percent number

        This function is also available in the template context as filter
        named `scientificformat`.

        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_scientific(number, format=format, locale=locale)
