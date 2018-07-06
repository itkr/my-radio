# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from datetime import datetime, timedelta
from pprint import pprint
from time import sleep

from modules.channel import get_channels
from modules.color import ColorString, print_error
from modules.commands import Commands


def title_string(text):
    return ColorString(text.capitalize()).yellow().under_line()


class BaseController(object):

    _stop = False

    def __init__(self, radio, timer=0):
        self.radio = radio
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(
            seconds=timer) if timer else None

        self.print_status()
        self.print_info()

    @property
    def commands(self):
        return Commands(self)

    def _check_time(self):
        if not self.end_time:
            return
        if self.end_time < datetime.now():
            self.stop()

    def _loop(self):
        while not self._stop:
            sleep(1)
            self._check_time()

    def start(self):
        self._loop()

    def stop(self):
        self._stop = True
        print('Good bye.')

    def extend(self, seconds):
        seconds = int(seconds)
        if not self.end_time:
            self.end_time = datetime.now()
        self.end_time += timedelta(seconds=int(seconds))
        self.print_status()

    def change(self, channel_key, area='JP13'):
        channel = get_channels(area).get(channel_key)
        if not channel:
            print_error('{} not found'.format(channel_key))
            return
        self.radio.reload(channel['url'])
        self.print_info()

    def print_channels(self, area='JP13'):
        pprint(get_channels(area))

    def print_info(self):
        for key, value in self.radio.get_info().items():
            print('{}:\n{}'.format(title_string(key), value))

    def print_status(self):
        status = {
            'start': self.start_time.isoformat(),
            'end': self.end_time.isoformat() if self.end_time else '',
        }
        for key, value in status.items():
            print('{}: \n{}'.format(title_string(key), value))
