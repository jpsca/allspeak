# coding=utf-8
from __future__ import print_function

from allspeak import pluralize
from babel import Locale


def test_pluralize_numbers():
    d = {
        0: u'No apples',
        1: u'One apple',
        3: u'Few apples',
        'other': u'{count} apples',
    }
    assert pluralize(d, 0) == u'No apples'
    assert pluralize(d, 1) == u'One apple'
    assert pluralize(d, 3) == u'Few apples'
    assert pluralize(d, 10) == u'{count} apples'


def test_pluralize_literal():
    d = {
        'zero': u'No apples',
        'one': u'One apple',
        'few': u'Few apples',
        'many': u'{count} apples',
    }
    assert pluralize(d, 0) == u'No apples'
    assert pluralize(d, 1) == u'One apple'
    assert pluralize(d, 3) == u'{count} apples'
    assert pluralize(d, 10) == u'{count} apples'


def test_pluralize_mixed():
    d = {
        'one': u'One apple',
        2: u'Two apples',
        'other': u'{count} apples',
    }
    assert pluralize(d, 1) == u'One apple'
    assert pluralize(d, 2) == u'Two apples'
    assert pluralize(d, 10) == u'{count} apples'


def test_pluralize_zero_or_many():
    d = {
        'zero': u'off',
        'many': u'on'
    }
    assert pluralize(d, 3) == u'on'

    d = {
        'zero': u'off',
        'many': u'on'
    }
    assert pluralize(d, 0) == u'off'
    assert pluralize(d, None) == u'off'
    assert pluralize({}, 3) == u''


def test_pluralize_other():
    d = {
        'one': u'One apple',
        'other': u'meh',
    }
    assert pluralize(d, 0) == u'meh'
    assert pluralize(d, 1) == u'One apple'
    assert pluralize(d, 2) == u'meh'
    assert pluralize(d, 3) == u'meh'
    assert pluralize(d, 10) == u'meh'


def test_two_plural_mode():
    d = {
        'zero': u'zero',
        'one': u'one',
        'two': u'two',
        'few': u'few',
        'other': u'other',
    }
    locale = Locale('en')

    assert pluralize(d, 0, locale) == u'zero'
    assert pluralize(d, 1, locale) == u'one'

    assert pluralize(d, 2, locale) == u'other'
    assert pluralize(d, 3, locale) == u'other'
    assert pluralize(d, 4, locale) == u'other'
    assert pluralize(d, 5, locale) == u'other'
    assert pluralize(d, 6, locale) == u'other'
    assert pluralize(d, 7, locale) == u'other'
    assert pluralize(d, 10, locale) == u'other'
    assert pluralize(d, 11, locale) == u'other'
    assert pluralize(d, 50, locale) == u'other'
    assert pluralize(d, 99, locale) == u'other'
    assert pluralize(d, 101, locale) == u'other'
    assert pluralize(d, 102, locale) == u'other'
    assert pluralize(d, 105, locale) == u'other'


def test_one_plural_mode():
    d = {
        'one': u'one',
        'two': u'two',
        'few': u'few',
        'many': u'many',
        'other': u'other',
    }
    locale = Locale('zh')

    assert pluralize(d, 0, locale) == u'other'
    assert pluralize(d, 1, locale) == u'other'
    assert pluralize(d, 2, locale) == u'other'
    assert pluralize(d, 3, locale) == u'other'
    assert pluralize(d, 4, locale) == u'other'
    assert pluralize(d, 5, locale) == u'other'
    assert pluralize(d, 6, locale) == u'other'
    assert pluralize(d, 7, locale) == u'other'
    assert pluralize(d, 10, locale) == u'other'
    assert pluralize(d, 11, locale) == u'other'
    assert pluralize(d, 50, locale) == u'other'
    assert pluralize(d, 99, locale) == u'other'
    assert pluralize(d, 101, locale) == u'other'
    assert pluralize(d, 102, locale) == u'other'
    assert pluralize(d, 105, locale) == u'other'

    d = {
        'zero': u'zero',
        'one': u'one',
        'two': u'two',
        'few': u'few',
        'many': u'many',
        'other': u'other',
    }
    locale = Locale('zh')

    assert pluralize(d, 0, locale) == u'zero'


def test_pluralize_arabic():
    d = {
        'zero': u'zero',
        'one': u'one',
        'two': u'two',
        'few': u'few',
        'many': u'many',
        'other': u'other',
    }
    locale = Locale('ar')

    assert pluralize(d, 0, locale) == u'zero'
    assert pluralize(d, 1, locale) == u'one'
    assert pluralize(d, 2, locale) == u'two'

    assert pluralize(d, 3, locale) == u'few'
    assert pluralize(d, 4, locale) == u'few'
    assert pluralize(d, 5, locale) == u'few'
    assert pluralize(d, 6, locale) == u'few'
    assert pluralize(d, 7, locale) == u'few'
    assert pluralize(d, 10, locale) == u'few'

    assert pluralize(d, 11, locale) == u'many'
    assert pluralize(d, 50, locale) == u'many'
    assert pluralize(d, 99, locale) == u'many'

    assert pluralize(d, 101, locale) == u'other'
    assert pluralize(d, 102, locale) == u'other'
    assert pluralize(d, 105, locale) == u'few'


def test_pluralize_russian():
    d = {
        'zero': u'zero',
        'one': u'one',
        'two': u'two',
        'few': u'few',
        'many': u'many',
        'other': u'other',
    }
    locale = Locale('ru')

    assert pluralize(d, 0, locale) == u'zero'
    assert pluralize(d, 1, locale) == u'one'

    assert pluralize(d, 2, locale) == u'few'
    assert pluralize(d, 3, locale) == u'few'
    assert pluralize(d, 4, locale) == u'few'

    assert pluralize(d, 5, locale) == u'many'
    assert pluralize(d, 6, locale) == u'many'
    assert pluralize(d, 7, locale) == u'many'
    assert pluralize(d, 10, locale) == u'many'
    assert pluralize(d, 11, locale) == u'many'

    assert pluralize(d, 21, locale) == u'one'
    assert pluralize(d, 22, locale) == u'few'
    assert pluralize(d, 23, locale) == u'few'
    assert pluralize(d, 24, locale) == u'few'
    assert pluralize(d, 25, locale) == u'many'

    assert pluralize(d, 50, locale) == u'many'
    assert pluralize(d, 99, locale) == u'many'

    assert pluralize(d, 101, locale) == u'one'
    assert pluralize(d, 102, locale) == u'few'
    assert pluralize(d, 105, locale) == u'many'

    assert pluralize(d, 111, locale) == u'many'
    assert pluralize(d, 112, locale) == u'many'
    assert pluralize(d, 113, locale) == u'many'
    assert pluralize(d, 114, locale) == u'many'
    assert pluralize(d, 119, locale) == u'many'

    assert pluralize(d, 121, locale) == u'one'
    assert pluralize(d, 122, locale) == u'few'
    assert pluralize(d, 125, locale) == u'many'
