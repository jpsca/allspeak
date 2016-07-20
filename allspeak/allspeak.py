# coding=utf-8
from .i18n import I18n
from .l10n import L10n


class Allspeak(I18n, L10n):

    """
    :param folderpath: path that will be searched for the translations.

    :param get_locale: a callable that returns the current locale

    :param get_timezone: a callable that returns the current timezone

    :param default_locale: default locale (as a string or as a
        Babel.Locale instance). This value will be accepted
        without checking if it's available.

    :param default_timezone: default timezone (as a string or as a
        `datetime.tzinfo` instance).

    :param markup: overwrite the function used by `translate` to flags HTML
        code as 'safe'. `markupsafe.Markup` is used by default.

    :param date_formats: update the defaults date formats.

    """

    def __init__(self, *args, **kwargs):
        super(Allspeak, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)
