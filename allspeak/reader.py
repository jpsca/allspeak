# coding=utf-8
import fnmatch
import io
import os
from os.path import join, dirname, realpath, abspath, normpath, isdir, splitext

import yaml

from .utils import LOCALES_FOLDER, split_locale


def get_yaml_data(filepath):
    """Parse a yaml locale file"""
    with io.open(filepath, mode='r', encoding='utf8') as f:
        data = yaml.safe_load(f)
    return data


class Reader(object):
    """Functions related to loading and parsing translation files.

    :param folderpath: path that will be searched for the translations.

    """
    def __init__(self, folderpath=LOCALES_FOLDER):
        self.folderpath = self._process_folderpath(folderpath)
        self._set_loaders()

    def __repr__(self):
        return '{cname}()'.format(
            cname=self.__class__.__name__,
        )

    def _set_loaders(self):
        self.loaders = {}
        self.loaders_ext = []
        self.register_loader('yml', get_yaml_data)

    def _process_folderpath(self, folderpath):
        folderpath = normpath(abspath(realpath(folderpath)))
        if not isdir(folderpath):
            folderpath = dirname(folderpath)
        return folderpath

    def register_loader(self, ext, func):
        """Register a loader for a file extension.
        `func` must take a single argument with the full path of a
        locale file and return a dictionary with the data.
        """
        if ext not in self.loaders_ext:
            self.loaders_ext.append(ext)
        self.loaders[ext] = func

    def get_loader(self, filepath):
        """Get the file loader suitable for a specific file.
        """
        _, ext = splitext(filepath)
        ext = ext.strip('.')
        loader = self.loaders.get(ext)
        assert loader, "Don't known how to read `*.{ext}` files".format(ext=ext)
        return loader

    def _extract_locales(self, data):
        """Parse the translation data and return tuples with the first-level
        keys with the locale and it's children (the translations).
        """
        return [
            (
                '_'.join(split_locale(locale)),
                trans
            )
            for locale, trans in data.items()
        ]

    def _load_file(self, filepath):
        """Load and parse the locale file from filepath.
        `filepath` should be an absolute path.
        """
        loader = self.get_loader(filepath)
        data = loader(filepath)
        return self._extract_locales(data)

    def _update_translations(self, translations, filepath):
        """Update the `translations` dictionary with the translation data
        extracted from the file in `filepath`.
        """
        data = self._load_file(filepath)
        for locale, trans in data:
            translations.setdefault(locale, {})
            translations[locale].update(trans)

    def load_translations(self, folderpath=None, locales=None):
        """Search for locale files on `folderpath`,
        load and parse them to build a big dictionary with all the
        translations data.

        Only the files with an extension listed in ``loaders_ext`` are loaded
        because only them have a registered loader.

        :param folderpath: overwrite the stored locales folder

        :param locales: does nothing, but might be useful to implement
            load-on-demand in your own subclass.

        """
        if folderpath:
            folderpath = self._process_folderpath(folderpath)
        else:
            folderpath = self.folderpath

        translations = {}
        for root, dirnames, filenames in os.walk(folderpath):
            for ext in self.loaders_ext:
                pattern = u'*.{}'.format(ext)
                for filename in fnmatch.filter(filenames, pattern):
                    if filename.startswith('.'):
                        continue
                    filepath = join(root, filename)
                    self._update_translations(translations, filepath)

        return translations
