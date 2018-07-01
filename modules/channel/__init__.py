# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import json
import os


def get_channels():
    channel_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fixtures/JP13.json'))
    with open(channel_path, encoding='utf-8') as channel:
        return json.loads(channel.read())
