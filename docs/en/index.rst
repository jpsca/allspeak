:orphan:

.. figure:: _static/allspeak-logo.png
   :align: center


.. container:: lead

    *Allspeak* is a pythonic (yet ironically inspired by Rails) internationalization and localization solution for Python web applications.

    It's flexible, easy to use and, unlike gettext, independent of any external compilation tool.

For the translations, this library **does not** use gettext [#]_, but instead it works with translations in **yaml** files, compatible by those used with the Rails internationalization system, so you can use any third-party service already compatible with them (for example, `Transifex <https://www.transifex.com/>`_).

It is powered by the `Babel <http://babel.pocoo.org/>`_ and `pytz <http://pythonhosted.org/pytz/>`_ libraries and tested with Python 2.7, 3.3+ and pypy.

----

Allspeak
==============================================

.. include:: contents.rst.inc


What's in a name?
----------------------------------------------

    "When Thor speaks with the *All-Speak* anyone who hears him will hear him speak their native language in their hearts"

    — *(from Thor's wiki page)*


.. [#] We find gettext cumbersome for translations of web apps.