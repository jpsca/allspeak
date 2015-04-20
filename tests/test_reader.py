# coding=utf-8
from __future__ import print_function

from os.path import join, dirname, abspath

from allspeak import Reader


LOCALES_TEST = abspath(join(dirname(__file__), u'locales'))


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
    assert expected == sorted(reader.extract_locales(data))


def test_load_file():
    reader = Reader()
    filepath = join(LOCALES_TEST, 'en.yml')
    locales = reader.load_file(filepath)
    locale, data = locales[0]
    assert locale == 'en'
    assert data['greeting'] == u'Hello World!'


def test_load_file_multilang():
    reader = Reader()
    filepath = join(LOCALES_TEST, 'multilang.yml')
    locales = reader.load_file(filepath)
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


def test_load_translations_from_other_folder():
    reader = Reader('.')
    data = reader.load_translations(folderpath=LOCALES_TEST)
    assert sorted(data.keys()) == ['en', 'es', 'es_PE']
    assert data['en']['cat'] == u'miaow'
    assert data['en']['foo'] == u'bar'
    assert data['es']['foo'] == u'bares'

    assert data['es']['accented'] == u'Olé niños y niñas'
