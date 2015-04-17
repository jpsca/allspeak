# coding=utf-8
"""
========================
AllSpeak
========================

AllSpeak is a pythonic (yet ironically inspired by Rails) i18n/l10n solution
for humans. It's flexible, easy to use and —unlike gettext— independent of
any external compilation tool.

How can the translator of your multi-language web application update a text?
Compiling `.po` files for a web app, really? How the Rails community solved
that problem? Translations in `yaml` or `json` files. With Python it should
be that simple. **Now it is**.

And the files used by Allspeak are compatible with those of Rails, so you can
use any third-party service already compatible with them
(for example, `Transifex <https://www.transifex.com/>`_).

Powered by the awesome Babel and pytz libraries for the l10n part.

What's in a name?
----------------------------------------------

    "When Thor speaks with the All-Speak anyone who hears him will hear him
    speak their native language in their hearts" ——(from Thor's wiki page)

:copyright: `Juan-Pablo Scaletti <http://jpscaletti.com>`_.
:license: MIT, see LICENSE for more details.

"""
# import os
# Workaround for a possible (?) OSX and/or Windows bug.
# if os.environ.get('LC_CTYPE', '').lower() == 'utf-8':
#     os.environ['LC_CTYPE'] = 'en_US.utf-8'

from .allspeak import Allspeak  # noqa
from .i18n import I18n  # noqa
from .l10n import L10n  # noqa
from .reader import Reader  # noqa
from .request_manager import RequestManager  # noqa
from .utils import *  # noqa

__version__ = '0.6'
