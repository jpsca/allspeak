# coding=utf-8
import io
import os
import re
from setuptools import setup, find_packages


def get_path(*args):
    return os.path.join(os.path.dirname(__file__), *args)


def read_from(filepath):
    with io.open(filepath, 'rt', encoding='utf8') as f:
        return f.read()


def get_version(package):
    data = read_from(get_path(package, '__init__.py'))
    version = re.search(r"__version__\s*=\s*u?'([^']+)'", data).group(1)
    return str(version)


def get_description(package):
    data = read_from(get_path(package, '__init__.py'))
    desc = re.search('"""(.+)"""', data, re.DOTALL).group(1)
    return desc.strip()


def get_requirements(filename='requirements.txt'):
    data = read_from(get_path(filename))
    lines = map(lambda s: s.strip(), data.splitlines())
    return [l for l in lines if l and not l.startswith('#')]


setup(
    name='AllSpeak',
    version=get_version('allspeak'),
    author='Juan-Pablo Scaletti',
    author_email='juanpablo@lucumalabs.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='http://github.com/lucuma/allspeak',
    license='MIT license (see LICENSE',
    description='Pythonic i18n/l10n system for WSGI-based web applications',
    long_description=get_description('allspeak'),
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
