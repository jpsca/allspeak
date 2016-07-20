# coding=utf-8
from babel import Locale
from babel.dates import get_timezone

from . import utils
from .utils import DEFAULT_LOCALE, DEFAULT_TIMEZONE


class RequestManager(object):

    """
    A base class with methods for getting the locale and timezone.

    :param get_locale: a callable that returns the current locale

    :param get_timezone: a callable that returns the current timezone

    :param default_locale: default locale (as a string or as a
        Babel.Locale instance). This value will be accepted
        without checking if it's available.

    :param default_timezone: default timezone (as a string or as a
        `datetime.tzinfo` instance).

    """

    def __init__(self, get_locale=None, get_timezone=None,
                 default_locale=DEFAULT_LOCALE,
                 default_timezone=DEFAULT_TIMEZONE,
                 get_request=None, available_locales=None):
        self._get_locale = get_locale
        self._get_timezone = get_timezone

        self.set_defaults(default_locale, default_timezone)
        self.translations = {}

    def __repr__(self):
        return '{}(default_locale={}, default_timezone={})'.format(
            self.__class__.__name__, self.default_locale, self.default_timezone)

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

    def get_locale(self):
        if self._get_locale:
            return self._get_locale()
        return self.default_locale

    def get_timezone(self):
        if self._get_timezone:
            return self._get_timezone()
        return self.default_timezone
