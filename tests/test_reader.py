# coding=utf-8
from __future__ import print_function

from os.path import join, dirname, abspath

from allspeak import Reader, parse_yaml


LOCALES_TEST = abspath(join(dirname(__file__), u'locales'))
LOCALES_TEST2 = LOCALES_TEST + u'2'


def test_reader_repr():
    reader = Reader()
    assert repr(reader) == 'Reader()'


def test_default_loaders():
    reader = Reader()
    assert reader.folderpath
    assert reader.loaders
    assert 'yml' in reader.loaders_ext


def test_extract_locales():
    reader = Reader()
    data = {
        'es-PE': {'foo-es': u'bar'},
        'en': {'foo-en': u'bar'},
    }
    expected = sorted([
        ('es_PE', {'foo-es': u'bar'}),
        ('en', {'foo-en': u'bar'}),
    ])
    assert expected == sorted(reader._extract_locales(data))


def test_load_file():
    reader = Reader()
    filepath = join(LOCALES_TEST, 'en.yml')
    locales = reader._load_file(filepath)
    locale, data = locales[0]
    assert locale == 'en'
    assert data['greeting'] == u'Hello World!'


def test_load_file_multilang():
    reader = Reader()
    filepath = join(LOCALES_TEST, 'multilang.yml')
    locales = reader._load_file(filepath)
    locales = sorted(locales)

    locale, data = locales[0]
    assert locale == 'en'
    assert data['cat'] == u'miaow'

    locale, data = locales[1]
    assert locale == 'es'
    assert data['cat'] == u'miau'


def test_load_translations():
    reader = Reader(LOCALES_TEST)
    data = reader.load_translations()
    assert sorted(data.keys()) == ['en', 'es', 'es_PE']
    assert data['en']['cat'] == 'miaow'
    assert data['en']['foo'] == 'bar'
    assert data['es']['foo'] == 'bares'


def test_deep_update():
    reader = Reader(LOCALES_TEST)
    data = reader.load_translations()
    assert data['en']['sub1']['sub2']['sub3']
    assert data['en']['sub1']['sub4']


def test_load_translations_from_other_folder():
    reader = Reader('.')
    data = reader.load_translations(folderpath=LOCALES_TEST)
    assert sorted(data.keys()) == ['en', 'es', 'es_PE']
    assert data['en']['cat'] == u'miaow'
    assert data['en']['foo'] == u'bar'
    assert data['es']['foo'] == u'bares'

    assert data['es']['accented'] == u'Olé niños y niñas'


def test_load_translations_from_multiple_sources():
    reader = Reader([LOCALES_TEST, LOCALES_TEST2])
    data = reader.load_translations()
    assert sorted(data.keys()) == ['en', 'es', 'es_PE']
    assert data['es']['greeting'] == u'¡Bienvenidos!'
    assert data['es']['foo'] == u'lorem ipsum'


def test_yaml_parser():
    yaml = u'''
foo: This is valid? This is valid! a, b, c
not_a_boolean: on
also_not_a_boolean: off
whatever: !ruby/object:Gem::Version
meh: @2%
number: 5
backtick: `poyo` is cool
quoted: "it's ok"
i18n: ¿olé? año
a_dict:
    0: zero
    one: one
    two: olé
'''
    expected = {
        'foo': 'This is valid? This is valid! a, b, c',
        'not_a_boolean': 'on',
        'also_not_a_boolean': 'off',
        'whatever': '!ruby/object:Gem::Version',
        'meh': '@2%',
        'number': 5,
        'backtick': '`poyo` is cool',
        'quoted': "it's ok",
        'i18n': u'¿olé? año',
        'a_dict': {
            0: 'zero',
            'one': 'one',
            'two': u'olé'
        }
    }
    result = parse_yaml(yaml)
    print(result)
    assert result == expected
