# coding=utf-8
from __future__ import print_function

from os.path import join, dirname, abspath

from babel import Locale
from babel.dates import UTC
from markupsafe import Markup

from allspeak import I18n


LOCALES_TEST = abspath(join(dirname(__file__), u'locales'))


def test_init_i18n():
    i18n = I18n(LOCALES_TEST)
    assert i18n.default_locale == Locale('en')
    assert i18n.default_timezone == UTC
    assert repr(i18n) == 'I18n()'


def test_init_i18n_default_locale():
    i18n = I18n(LOCALES_TEST, default_locale='es-PE')
    locale = Locale('es', 'PE')
    assert i18n.default_locale == locale
    assert i18n.get_locale() == locale


def test_init_i18n_locales():
    i18n = I18n(LOCALES_TEST)
    assert i18n.reader.folderpath == LOCALES_TEST

    folderpath = join(LOCALES_TEST, u'sub')
    i18n = I18n(folderpath)
    assert i18n.reader.folderpath == folderpath


def test_load_translations():
    i18n = I18n(LOCALES_TEST)
    i18n.load_translations()
    trans = i18n.translations
    print(trans)

    assert trans['en']['greeting'] == u'Hello World!'
    assert trans['es']['greeting'] == u'Hola mundo'
    assert trans['es_PE']['greeting'] == u'Habla'


def test_get_translations_from_locale():
    i18n = I18n(LOCALES_TEST)

    ltrans_es = i18n.get_translations_from_locale(Locale('es'))
    assert len(ltrans_es) == 1
    expected_es = 'foo cat greeting accented so'.split()
    trans_es = ltrans_es[0]
    assert sorted(trans_es.keys()) == sorted(expected_es)

    ltrans_espe = i18n.get_translations_from_locale(Locale('es', 'PE'))
    assert len(ltrans_espe) == 2
    expected_es = 'foo cat greeting accented so'.split()
    expected_espe = 'greeting'.split()
    trans_espe = ltrans_espe[0]
    trans_es = ltrans_espe[1]
    assert sorted(trans_espe.keys()) == sorted(expected_espe)
    assert sorted(trans_es.keys()) == sorted(expected_es)

    ltrans_en = i18n.get_translations_from_locale(Locale('en'))
    expected_en = 'foo cat greeting apple with_html'.split()
    trans_en = ltrans_en[0]
    assert sorted(trans_en.keys()) == sorted(expected_en)


def test_key_lookup():
    i18n = I18n(LOCALES_TEST)

    locale = Locale('es')
    assert i18n.key_lookup(locale, 'greeting') == u'Hola mundo'
    assert i18n.key_lookup(locale, 'so.much.such') == u'wow'

    locale = Locale('es', 'PE')
    assert i18n.key_lookup(locale, 'greeting') == u'Habla'

    locale = Locale('en')
    expected = {
        0: 'No apples',
        1: 'One apple',
        3: 'Few apples',
        'n': '%(count)s apples',
    }
    assert i18n.key_lookup(locale, 'apple') == expected

    # Key not found
    assert i18n.key_lookup(locale, 'this.is.wrong') == None

    # Language not found
    assert i18n.key_lookup(Locale('fr'), 'greeting') == None


def test_translate():
    i18n = I18n(LOCALES_TEST, default_locale='es-PE')

    assert i18n.translate('greeting') == u'Habla'

    locale = Locale('es')
    assert i18n.translate('greeting', locale=locale) == u'Hola mundo'

    locale = Locale('en')
    assert i18n.translate('apple', 3, locale=locale) == u'Few apples'
    assert i18n.translate('apple', 10, locale=locale) == u'10 apples'

    assert i18n.translate('bla', locale=locale) == '<missing:bla>'
    # assert i18n.translate('olé', locale=locale) == '<missing:olé>'

    assert i18n.translate('with_html', locale=locale) == Markup(u'<b>Hello</b>')


def test_lazy_translate():
    i18n = I18n(LOCALES_TEST, default_locale='es_PE')

    lazy = i18n.lazy_translate('greeting')
    assert lazy != u'Habla'
    assert repr(lazy) == u'Habla'

    lazy = i18n.lazy_translate('bla')
    assert repr(lazy) == '<missing:bla>'

    locale = Locale('en')
    lazy = i18n.lazy_translate('greeting', locale=locale)
    assert lazy != u'Hello World!'
    assert repr(lazy) == u'Hello World!'

    locale = Locale('fr')
    lazy = i18n.lazy_translate('greeting', locale=locale)
    assert lazy != '<missing:greeting>'
    assert repr(lazy) == '<missing:greeting>'
