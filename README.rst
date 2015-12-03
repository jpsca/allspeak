
.. image:: https://travis-ci.org/jpscaletti/allspeak.svg?branch=master
   :target: https://travis-ci.org/jpscaletti/allspeak
   :alt: Build Status

===========================
Allspeak
===========================

*Allspeak* is a pythonic (yet ironically inspired by Rails) internationalization and localization solution for Python web applications.

It's flexible, easy to use and, unlike gettext, independent of any external compilation tool.

This library **does not** use gettext —we find it cumbersome, to say the least—, but instead it works with translations in **yaml** files, compatible by those used with the Rails internationalization system, so you can use any third-party service already compatible with them (for example, `Transifex <https://www.transifex.com/>`_).

It is powered by the `Babel <http://babel.pocoo.org/>`_ and `pytz <http://pythonhosted.org/pytz/>`_ libraries and tested with Python 2.7, 3.3+ and pypy.

Read the documentation here: http://allspeak.lucuma.co


What's in a name?
==============================================

    "When Thor speaks with the All-Speak anyone who hears him will hear him speak their native language in their hearts" ——(from Thor's wiki page)


Contributing
==============================================

#. Check for `open issues <https://github.com/jpscaletti/Allspeak/issues>`_ or open
   a fresh issue to start a discussion around a feature idea or a bug.
#. Fork the `Allspeak repository on Github <https://github.com/jpscaletti/Allspeak>`_
   to start making your changes.
#. Write a test which shows that the bug was fixed or that the feature works
   as expected.
#. Send a pull request and bug the maintainer until it gets merged and published.
   :) Make sure to add yourself to ``AUTHORS``.


Run the tests
==============================================

We use some external dependencies, listed in ``requirements_tests.txt``::

    $  pip install -r requirements-tests.txt
    $  python setup.py install

To run the tests in your current Python version do::

    $  make test

To run them in every supported Python version do::

    $  tox

It's also neccesary to run the coverage report to make sure all lines of code
are touch by the tests::

    $  make coverage

Our test suite `runs continuously on Travis CI <https://travis-ci.org/jpscaletti/Allspeak>`_ with every update.


-----

:copyright: 2012-2015 by `Juan-Pablo Scaletti <http://jpscaletti.com>`_.
:license: Three clause BSD License, see LICENSE for more details.
:code: https://github.com/jpscaletti/allspeak
