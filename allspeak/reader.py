# -*- coding: utf-8 -*-
import io

import yaml


def get_data(filename):
    with io.open(filename, mode='r', encoding='utf8') as f:
        data = yaml.safe_load(f)
    return data

