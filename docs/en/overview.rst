.. module:: allspeak

Overview
=============================================

Allspeak does three things for you:

1. Get the user's preferred languages and timezone from the request.

2. Translate your previously extracted texts (more on this later) to the best available language or to the default language.

3. Localize dates, numbers and other values to the user's language

In *Allspeak* these concerns are actually separated, so you could for example, use to localize dates in a single-language application.


Install & Setup
---------------------------------------------

.. sourcecode:: bash

    pip install allspeak

The first thing to do is to create an `Allspeak` instance.

.. sourcecode:: python

    from allspeak import Allspeak

    speak = Allspeak(
        # path that will be searched for the translations files
        folderpath,

        # a callable that returns the current request
        get_request,

        # default locale (as a string or as a Babel.Locale instance)
        default_locale,

        # default (as a string or as a datetime.tzinfo instance)
        default_timezone
    )

and then you can use the methods for translation:

.. sourcecode:: python

    _ = speak.translate


and localization

.. sourcecode:: python

    speak.format_datetime(...)
    speak.format_date(...)
    speak.format_time(...)
    speak.format_timedelta(...)
    speak.format_number(...)(...)
    speak.format_decimal(...)
    speak.format_currency(...)
    speak.format_percent(...)
    speak.format_scientific(...)

The ``folderpath`` is an optional path of the folder containing all your yaml files with translations. If you are not planning to use translations, you can safely ignore that argument.

