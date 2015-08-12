# coding=utf-8
from babel import Locale
from babel.dates import get_timezone

from . import utils
from .utils import DEFAULT_LOCALE, DEFAULT_TIMEZONE, DEFAULT_DATE_FORMATS


class RequestManager(object):
    """
    A base class with methods for getting the locale and timezone
    from the request object.

    :param get_request: a callable that returns the current request.

    :param get_locale: overwrites the ``get_locale`` method.

    :param get_timezone: overwrites the ``get_timezone`` method.

    :param default_locale: default locale (as a string or as a
        Babel.Locale instance).

    :param default_timezone: default timezone (as a string or as a
        `datetime.tzinfo` instance).

    :param available_locales: list of available locales
        (as ISO 639-1 language codes).

    :param date_formats: update the defaults date formats.

    """

    def __init__(self,
                 get_request=None, get_locale=None, get_timezone=None,
                 default_locale=DEFAULT_LOCALE,
                 default_timezone=DEFAULT_TIMEZONE,
                 available_locales=None,
                 date_formats=None):
        self._get_request = get_request
        self._get_locale = get_locale
        self._get_timezone = get_timezone

        self.set_defaults(default_locale, default_timezone)
        self.set_available(available_locales)
        self.set_date_formats(date_formats)
        self.translations = {}

    def __repr__(self):
        return '{cname}(default_locale={default_locale}, default_timezone={default_timezone})'.format(
            cname=self.__class__.__name__,
            default_locale=self.default_locale,
            default_timezone=self.default_timezone,
        )

    def set_defaults(self, default_locale, default_timezone):
        """Set the default locale from the configuration as an instance of
        :class:`babel.core.Locale` and the default timezone as a
        `datetime.tzinfo`.

        """
        self.default_locale = (
            utils.normalize_locale(default_locale) or
            Locale(DEFAULT_LOCALE)
        )
        self.default_timezone = (
            utils.normalize_timezone(default_timezone) or
            get_timezone(DEFAULT_TIMEZONE)
        )

    def set_available(self, available_locales):
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

    def set_date_formats(self, date_formats):
        self.date_formats = DEFAULT_DATE_FORMATS.copy()
        if date_formats:
            self.date_formats.update(date_formats)

    def get_locale(self):
        if self._get_locale:
            return self._get_locale()
        return self.__get_locale()

    def get_timezone(self):
        if self._get_timezone:
            return self._get_timezone()
        return self.__get_timezone()

    def __get_locale(self):
        """Returns the locale that should be used for this request as
        an instance of :class:`babel.core.Locale`.
        This returns the default locale if used outside of a request.

        """
        request = self._get_request and self._get_request()
        if not request:
            return self.default_locale
        return utils.get_request_locale(request, self.available_locales, self.default_locale)

    def __get_timezone(self):
        """Returns the timezone that should be used for this request as
        `datetime.tzinfo` instance.  This returns the default timezone if used
        outside of a request or if no timezone was defined.

        """
        request = self._get_request and self._get_request()
        if not request:
            return self.default_timezone
        return utils.get_request_timezone(request, self.default_timezone)
