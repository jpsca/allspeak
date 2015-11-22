
API
=============================================

.. module:: allspeak


Allspeak
----------------------------------------------

A class that inherit from both `I18n` and `L10n` classes.

.. autoclass:: Allspeak
   :members:


I18n
----------------------------------------------

.. autoclass:: I18n
   :members:

.. autofunction:: pluralize


L10n
----------------------------------------------

.. autoclass:: L10n
   :members:


Reader
----------------------------------------------

.. autoclass:: Reader
   :members:


RequestManager
----------------------------------------------

.. autoclass:: RequestManager
   :members:


Integrations
----------------------------------------------

.. autofunction:: get_werkzeug_preferred_locales

.. autofunction:: get_webob_preferred_locales

.. autofunction:: get_django_preferred_locales


Utilities
----------------------------------------------

.. autofunction:: normalize_locale

.. autofunction:: normalize_timezone

.. autofunction:: split_locale

.. autofunction:: locale_to_str
