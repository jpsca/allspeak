# coding=utf-8
from .i18n import I18n
from .l10n import L10n


class Allspeak(I18n, L10n):

    def __init__(self, *args, **kwargs):
        """
        folderpath:
            path or list of paths that will be searched for the translations

        markup:
            overwrite the function used by `translate` to flags HTML code
            as 'safe'. `markupsafe.Markup` is used by default.

        get_request:
            a callable that returns the current request.

        default_locale:
            default locale (as a string or as a Babel.Locale instance).

        default_timezone:
            default timezone.

        date_formats:
            update the defaults date formats.

        """
        super(Allspeak, self).__init__(*args, **kwargs)


    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)
