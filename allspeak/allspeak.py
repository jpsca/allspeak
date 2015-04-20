# coding=utf-8
from .i18n import I18n
from .l10n import L10n


class Allspeak(I18n, L10n):
    """
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

    def __init__(self, *args, **kwargs):
        super(Allspeak, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)
