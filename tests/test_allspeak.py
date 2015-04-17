# coding=utf-8

from allspeak import Allspeak, L10n, I18n


def test_allspeak_repr():
    speak = Allspeak()
    assert repr(speak) == 'Allspeak()'


def test_allspeak_has_l10n():
    speak = Allspeak()
    l10n = L10n()
    for key in l10n.__dict__:
        assert hasattr(speak, key)


def test_allspeak_has_i18n():
    speak = Allspeak()
    i18n = I18n()
    for key in i18n.__dict__:
        assert hasattr(speak, key)
