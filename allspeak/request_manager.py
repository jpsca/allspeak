# coding=utf-8
from babel import Locale
from babel.dates import get_timezone

from . import utils
from .utils import DEFAULT_LOCALE, DEFAULT_TIMEZONE
from .integrations import (
    get_werkzeug_preferred_locales,
    get_webob_preferred_locales,
    get_django_preferred_locales,
)


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

    :param get_request: a callable that returns the current request.
        Do not use this, it exist only for backwards compatibility.

    """
    DEFAULT_DATE_FORMATS = {
        'time': 'medium',
        'date': 'medium',
        'datetime': 'medium',
    }

    def __init__(self, get_locale=None, get_timezone=None,
                 default_locale=DEFAULT_LOCALE,
                 default_timezone=DEFAULT_TIMEZONE,
                 get_request=None, available_locales=None):
        self._get_locale = get_locale
        self._get_timezone = get_timezone

        self.set_defaults(default_locale, default_timezone)
        self.translations = {}

        # Deprecated
        self._get_request = get_request
        self.available_locales = available_locales

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

    def get_locale(self):
        if self._get_locale:
            return self._get_locale()
        # deprecated
        if self._get_request:
            return self._deprecated_get_locale_from_request()
        #
        return self.default_locale

    def get_timezone(self):
        if self._get_timezone:
            return self._get_timezone()
        # deprecated
        if self._get_request:
            return self._deprecated_get_timezone_from_request()
        #
        return self.default_timezone

    def _deprecated_get_locale_from_request(self):
        """Set the locale that should be used for this request as a
        `babel.Locale` instance.

        Tries the following in order:

        - an request attribute called `'locale'`
        - a GET argument called `'locale'`
        - the prefered
        - the default locale

        """
        request = self._get_request()
        if not request:
            return self.default_locale
        if not self.available_locales:
            return self.default_locale
        locale = (
            getattr(request, 'locale', None) or
            getattr(request, 'args', getattr(request, 'GET', {})).get('locale')
        )
        if locale:
            preferred = [locale]
        else:
            preferred = (
                get_werkzeug_preferred_locales(request) or
                get_webob_preferred_locales(request) or
                get_django_preferred_locales(request) or
                []
            )

        preferred = map(utils.locale_to_str, preferred)
        available = map(utils.locale_to_str, self.available_locales)
        # To ensure a consistent matching, Babel algorithm is used.
        locale = Locale.negotiate(preferred, available, sep='_')
        request.locale = locale or self.default_locale
        return request.locale

    def _deprecated_get_timezone_from_request(self):
        """Set the timezone that should be used for this request as a
        `datetime.tzinfo` instance.

        Tries the following in order:

        - an attribute called `'tzinfo'`
        - a GET argument called `'tzinfo'`
        - the provided default timezone
        """
        request = self._get_request()
        if not request:
            return self.default_timezone
        tzinfo = (
            getattr(request, 'tzinfo', None) or
            getattr(request, 'args', getattr(
                    request, 'GET', {})).get('tzinfo')
        )
        request.tzinfo = utils.normalize_timezone(tzinfo) or self.default_timezone
        return request.tzinfo
