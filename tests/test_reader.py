# -*- coding: utf-8 -*-
from os.path import join, dirname

from allspeak import reader


locales_dir = join(dirname(__file__), 'locales')


def test_load_language():
    path = join(locales_dir, 'es.yml')
    data = reader.get_data(path)
    assert data['mytest']['greeting'] == u'Hola'

    path = join(locales_dir, 'es-PE.yml')
    data = reader.get_data(path)
    assert data['mytest']['greeting'] == u'Habla'
