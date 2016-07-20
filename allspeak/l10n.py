# coding=utf-8
import datetime as dt
from decimal import Decimal

from babel import dates, numbers
from babel.dates import UTC

from . import utils
from .request_manager import RequestManager


class L10n(RequestManager):

    """Localization functions.

    :param get_locale: a callable that returns the current locale

    :param get_timezone: a callable that returns the current timezone

    :param default_locale: default locale (as a string or as a
        Babel.Locale instance). This value will be accepted
        without checking if it's available.

    :param default_timezone: default timezone (as a string or as a
        `datetime.tzinfo` instance).

    :param date_formats: update the defaults date formats.

    """
    DEFAULT_DATE_FORMATS = {
        'time': 'medium',
        'date': 'medium',
        'datetime': 'medium',
    }

    def __init__(self, date_formats=None, **kwargs):
        self.set_date_formats(date_formats)
        super(L10n, self).__init__(**kwargs)

    def set_date_formats(self, date_formats):
        """Update the default date and time formats used by `self.format*`
        **for all locales** when called without a `format` argument.

        These are the defaults::

            {
              'time': 'medium',
              'date': 'medium',
              'datetime': 'medium',
            }

        """
        self.date_formats = self.DEFAULT_DATE_FORMATS.copy()
        if date_formats:
            self.date_formats.update(date_formats)

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
        tzinfo = utils.normalize_timezone(tzinfo)
        return tzinfo.normalize(datetime.astimezone(tzinfo))

    def to_utc(self, datetime, tzinfo=None):
        """Convert a datetime object to UTC and drop tzinfo.
        """
        if datetime.tzinfo is None:
            tzinfo = tzinfo or self.get_timezone()
            tzinfo = utils.normalize_timezone(tzinfo)
            datetime = tzinfo.localize(datetime)
        return datetime.astimezone(UTC).replace(tzinfo=None)

    def _get_format(self, key, format):
        """Gets the date format for that key.
        Helper for the datetime formatting functions.
        """
        if format is None:
            format = self.date_formats.get(key)
        if format in ('short', 'medium', 'full', 'long'):
            dkey = '{key}.{format}'.format(key=key, format=format)
            rv = self.date_formats.get(dkey)
            if rv is not None:
                format = rv
        return format

    def _date_format(self, formatter, obj, format, rebase,
                     locale=None, tzinfo=None, **extra):
        if obj == 'now':
            obj = dt.datetime.utcnow()
        locale = utils.normalize_locale(locale) or self.get_locale()
        extra = {}
        if formatter is not dates.format_date and rebase:
            tzinfo = tzinfo or self.get_timezone()
            extra['tzinfo'] = utils.normalize_timezone(tzinfo)
        return formatter(obj, format, locale=locale, **extra)

    def format(self, value, *args, **kwargs):
        """Return a formatted `value` according to the detected type and
        given parameters.

        It doesn't know anything about currency, percent or
        scientific formats, so use the other methods for those cases.
        """
        locale = kwargs.pop('locale', None)
        tzinfo = kwargs.pop('tzinfo', None)

        if value in ('', None):
            return ''

        if isinstance(value, dt.date):
            if isinstance(value, dt.datetime):
                return self.format_datetime(
                    value, locale=locale, tzinfo=tzinfo, *args, **kwargs)
            else:
                return self.format_date(
                    value, locale=locale, tzinfo=tzinfo, *args, **kwargs)

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
                        locale=None, tzinfo=None, **kwargs):
        """Return a datetime formatted according to the given pattern.

        :param datetime: A `datetime.datetime` object.
            If no object is passed, the current datetime is assumed.

        :param format: The format parameter can either be `'short'`, `'medium'`,
            `'long'` or `'full'` (in which cause the language's default for
            that setting is used) or a format string as
            `documented by Babel <http://babel.pocoo.org/docs/dates/#date-fields>`_.

        :param rebase: Convert the given `date` to the users's timezone (as returned by
            :meth:`to_user_timezone`)
            By default rebasing happens.

        :param locale: Overwrite the global locale.
        :param tzinfo: Overwrite the global timezone.

        """
        format = self._get_format('datetime', format)
        return self._date_format(
            dates.format_datetime, datetime, format, rebase,
            locale=locale, tzinfo=tzinfo, **kwargs
        )

    def format_date(self, date=None, format=None, rebase=True,
                    locale=None, tzinfo=None, **kwargs):
        """Return a date formatted according to the given pattern.

        :param date: A `datetime.datetime` or `datetime.date` object.
            If no object is passed, the current datetime is assumed.

        :param format: The format parameter can either be `'short'`, `'medium'`,
            `'long'` or `'full'` (in which cause the language's default for
            that setting is used) or a format string as
            `documented by Babel <http://babel.pocoo.org/docs/dates/#date-fields>`_.

        :param rebase: Convert the given `date` to the users's timezone (as returned by
            :meth:`to_user_timezone`)
            By default rebasing happens.

        :param locale: Overwrite the global locale.
        :param tzinfo: Overwrite the global timezone.

        """
        if rebase and isinstance(date, dt.datetime):
            date = self.to_user_timezone(date, tzinfo=tzinfo)
        format = self._get_format('date', format)
        return self._date_format(
            dates.format_date, date, format, rebase,
            locale=locale, tzinfo=tzinfo, **kwargs
        )

    def format_time(self, time=None, format=None, rebase=True,
                    locale=None, tzinfo=None, **kwargs):
        """Return a time formatted according to the given pattern.

        :param time: A `time` or `datetime` object.
            If no object is passed, the current time is assumed.

        :param format: The format parameter can either be `'short'`, `'medium'`,
            `'long'` or `'full'` (in which cause the language's default for
            that setting is used) or a format string as
            `documented by Babel <http://babel.pocoo.org/docs/dates/#time-fields>`_.

        :param rebase: Convert the given `time` to the users's timezone (as returned by
            :meth:`to_user_timezone`).
            By default rebasing happens.

        :param locale: Overwrite the global locale.
        :param tzinfo: Overwrite the global timezone.

        """
        format = self._get_format('time', format)
        return self._date_format(
            dates.format_time, time, format, rebase,
            locale=locale, tzinfo=tzinfo, **kwargs
        )

    def format_timedelta(self, datetime_or_timedelta, granularity='second',
                         threshold=0.85, add_direction=False, format='medium',
                         locale=None, **kwargs):
        """Format the elapsed time from the given date to now or the given
        timedelta as documented in :func:`babel.dates.format_timedelta`.

        :param delta: a timedelta object representing the time difference to
            format, or the delta in seconds as an int value.

        :param granularity: determines the smallest unit that should be
            displayed, the value can be one of “year”, “month”, “week”, “day”,
            “hour”, “minute” or “second”.

        :param threshold: factor that determines at which point the
            presentation switches to the next higher unit.

        :param add_direction: if this flag is set to True the
            return value will include directional information. For instance a
            positive timedelta will include the information about it being in
            the future, a negative will be information about the value being in
            the past.

        :param format: the format (currently only “medium” and “short” are supported)
        :param locale: Overwrite the global locale.

        """
        if datetime_or_timedelta in ('', None):
            return ''
        locale = utils.normalize_locale(locale) or self.get_locale()
        if isinstance(datetime_or_timedelta, dt.datetime):
            datetime_or_timedelta = datetime_or_timedelta - dt.datetime.utcnow()

        resp = dates.format_timedelta(
            datetime_or_timedelta,
            granularity=granularity, threshold=threshold,
            add_direction=add_direction, locale=locale,
            **kwargs
        )
        if add_direction:
            # Inconsistent among different python versions (titlecased only sometimes)
            return resp[0].lower() + resp[1:]
        return resp

    def format_number(self, number, locale=None, **kwargs):
        """Return the given number formatted for the locale in the
        current request.

        :param number: the number to format
        :param locale: Overwrite the global locale.

        """
        if number in ('', None):
            return ''
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_number(number, locale=locale, **kwargs)

    def format_decimal(self, number, format=None, locale=None, **kwargs):
        """Return the given decimal number formatted for the locale in the
        current request.

        :param number: the number to format
        :param format: the format to use as
            `documented by Babel <http://babel.pocoo.org/docs/numbers/#pattern-syntax>`_.
        :param locale: Overwrite the global locale.

        """
        if number in ('', None):
            return ''
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_decimal(number, format=format, locale=locale, **kwargs)

    def format_currency(self, number, currency, format=None, locale=None, **kwargs):
        """Return the given number formatted for the locale in the
        current request.

        :param number: the number to format
        :param currency: the currency code
        :param format: the format to use as
            `documented by Babel <http://babel.pocoo.org/docs/numbers/#pattern-syntax>`_.
        :param locale: Overwrite the global locale.

        Also see: https://codeascraft.com/2016/04/19/how-etsy-formats-currency/
        """
        if number in ('', None):
            return ''
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_currency(
            number, currency, format=format, locale=locale, **kwargs)

    def format_percent(self, number, format=None, locale=None, **kwargs):
        """Return a percent value formatted for the locale in the
        current request.

        :param number: the number to format
        :param format: the format to use as
            `documented by Babel <http://babel.pocoo.org/docs/numbers/#pattern-syntax>`_.
        :param locale: Overwrite the global locale.

        """
        if number in ('', None):
            return ''
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_percent(number, format=format, locale=locale, **kwargs)

    def format_scientific(self, number, format=None, locale=None, **kwargs):
        """Return value formatted in scientific notation for the locale in
        the current request.

        :param number: the number to format
        :param format: the format to use as
            `documented by Babel <http://babel.pocoo.org/docs/numbers/#pattern-syntax>`_.
        :param locale: Overwrite the global locale.

        """
        if number in ('', None):
            return ''
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_scientific(number, format=format, locale=locale, **kwargs)
