# -*- coding: utf-8 -*-
"""
========================
AllSpeak
========================

Pythonic (yet ironically inspired by Rails) i18n/l10n solution for humans
doing WSGI-based web applications.  It's flexible, easy to use and
—unlike gettext— independent of any external compilation tool.

Powered by the awesome Babel and pytz libraries for the l10n part.

The library is MIT Licensed and compatible with Werkzeug, Webob and Django
request objects, so you can use it with pretty much any WSGI-based framework.

See the documentation online at http://lucuma.github.com/allspeak

"""
import os
# Workaround for a OSX bug
if os.environ.get('LC_CTYPE', '').lower() == 'utf-8':
    os.environ['LC_CTYPE'] = 'en_US.utf-8'

from allspeak.i18n import I18n, LOCALES_DIR  # noqa
from allspeak.utils import negotiate_locale, get_preferred_locales  # noqa

__version__ = '0.5.7'
