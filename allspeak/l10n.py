# coding=utf-8
import datetime as dt
from decimal import Decimal

from babel import dates, numbers
from babel.dates import UTC

from . import utils
from .request_manager import RequestManager


class L10n(RequestManager):
    """Localization functions
    """

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
        """
        format = self._get_format('datetime', format)
        return self._date_format(
            dates.format_datetime, datetime, format, rebase,
            locale=locale, tzinfo=tzinfo)

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
        """
        if rebase and isinstance(date, dt.datetime):
            date = self.to_user_timezone(date, tzinfo=tzinfo)
        format = self._get_format('date', format)
        return self._date_format(
            dates.format_date, date, format, rebase,
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
        """
        format = self._get_format('time', format)
        return self._date_format(
            dates.format_time, time, format, rebase,
            locale=locale, tzinfo=tzinfo)

    def format_timedelta(self, datetime_or_timedelta, granularity='second',
                         locale=None):
        """Format the elapsed time from the given date to now or the given
        timedelta.
        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        if isinstance(datetime_or_timedelta, dt.datetime):
            datetime_or_timedelta = dt.datetime.utcnow() - datetime_or_timedelta
        return dates.format_timedelta(
            datetime_or_timedelta, granularity, locale=locale)

    def format_number(self, number, locale=None):
        """Return the given number formatted for the locale in the
        current request.

        number:
            the number to format

        return (unicode):
            the formatted number
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
        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_currency(
            number, currency, format=format, locale=locale)

    def format_percent(self, number, format=None, locale=None):
        """Return a percent value formatted for the locale in the
        current request.

        number:
            the number to format
        format:
            the format to use

        return (unicode):
            the formatted percent number
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
        """
        locale = utils.normalize_locale(locale) or self.get_locale()
        return numbers.format_scientific(number, format=format, locale=locale)
