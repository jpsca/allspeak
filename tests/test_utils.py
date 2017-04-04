# coding=utf-8
from __future__ import print_function

from allspeak import utils
from babel import Locale
from pytz import timezone

from .conftest import get_test_request


def test_split_locale():
    assert utils.split_locale('en-US') == ('en', 'US')
    assert utils.split_locale('En_us') == ('en', 'US')
    assert utils.split_locale(Locale('en', 'US')) == ('en', 'US')


def test_normalize_locale():
    assert utils.normalize_locale('es') == Locale('es')
    assert utils.normalize_locale('en-US') == Locale('en', 'US')
    assert utils.normalize_locale('en_us') == Locale('en', 'US')
    assert utils.normalize_locale('en-us') == Locale('en', 'US')
    assert utils.normalize_locale('en_US') == Locale('en', 'US')
    assert utils.normalize_locale('En-Us') == Locale('en', 'US')

    assert utils.normalize_locale(Locale('en', 'US')) == Locale('en', 'US')

    assert utils.normalize_locale(('es', )) == Locale('es')
    assert utils.normalize_locale(('en', 'US')) == Locale('en', 'US')
    assert utils.normalize_locale(['en', 'US']) == Locale('en', 'US')
    assert utils.normalize_locale(['EN', 'us']) == Locale('en', 'US')
    assert utils.normalize_locale(['en', 'US', 'Texas']) == Locale('en', 'US')

    assert utils.normalize_locale('klingon') is None
    assert utils.normalize_locale(None) is None
    assert utils.normalize_locale(1) is None


def test_normalize_timezone():
    assert utils.normalize_timezone(timezone('America/Lima')) == timezone('America/Lima')
    assert utils.normalize_timezone('America/Lima') == timezone('America/Lima')
    assert utils.normalize_timezone('Mars') is None
    assert utils.normalize_timezone(None) is None


def test_locale_to_str():
    assert utils.locale_to_str(Locale('en', 'US')) == 'en_US'
    assert utils.locale_to_str(Locale('es')) == 'es'
    assert utils.locale_to_str('en_US') == 'en_US'


def test_flatten():
    dic = {
        'a': 1,
        'c': {
            'a': 2,
            'b': {
                'x': 5,
                'y': 10,
            }
        },
        'd': [1, 2, 3],
    }
    expected = {'a': 1, 'c.a': 2, 'c.b.x': 5, 'c.b.y': 10, 'd': [1, 2, 3]}
    assert utils._flatten(dic) == expected
