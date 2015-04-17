# coding=utf-8
"""
Utilities for writing code that runs on Python 2 and 3.
"""
import sys


PY2 = sys.version_info[0] == 2
string_types = (basestring, ) if PY2 else (str, )
