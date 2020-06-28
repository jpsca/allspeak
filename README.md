[![Build Status](https://travis-ci.org/jpsca/allspeak.svg?branch=master)](https://travis-ci.org/jpsca/allspeak)

# Allspeak

*Allspeak* is a pythonic (yet ironically inspired by Rails) internationalization and localization solution for Python web applications.

It's flexible, easy to use and, unlike gettext, independent of any external compilation tool.
 
This library **does not** use gettext -we find it cumbersome, to say the least-, but instead it works with translations in **YAML** files, compatible by those used with the Rails internationalization system, so you can use any third-party service already compatible with them (for example, [Transifex](https://www.transifex.com/)).

It is powered by the [Babel](http://babel.pocoo.org/) and [pytz](http://pythonhosted.org/pytz/) libraries and tested with Python 3.5+

Read the documentation here: <http://allspeak.lucuma.co>


## What's in a name?

> "When Thor speaks with the All-Speak anyone who hears him will hear
> him speak their native language in their hearts"
> ------(from Thor's wiki page)


## Run the tests

    $  pip install .
    $  pip install .[testing]

To run the tests in your current Python version do:

    $  make test

To run them in every supported Python version do:

    $  tox

It might be also necessary to run the coverage report to make sure all lines
of code are touch by the tests:

    $  make coverage

The test suite [runs continuously on Travis
CI](https://travis-ci.org/jpsca/Allspeak) with every update.
