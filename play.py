#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import json
import os
import sys
import threading
from datetime import datetime, timedelta
from distutils.sysconfig import get_python_lib
from time import sleep

from modules.channel import get_channels
from modules.radio import Radio


class DriverPathNotFoundError(Exception):
    pass


def parse_args(channel_choices):
    parser = argparse.ArgumentParser(
        description='Play radio.')
    parser.add_argument(
        '-d', '--driver', dest='driver', help='driver file')
    parser.add_argument(
        '-c', '--channel', dest='channel', help='channel key',
        default='TBS', choices=channel_choices)
    parser.add_argument(
        '-s', '--seconds', dest='playback_seconds', type=int,
        help='playback seconds', default=60 * 60)
    return parser.parse_args()


def get_driver_path(args):
    # 0: arg
    driver_path = args.driver
    if driver_path and os.path.exists(driver_path):
        return driver_path

    # 1: env
    driver_path = os.environ.get('SELENIUM_DRIVER')
    if driver_path and os.path.exists(driver_path):
        return driver_path

    # 2: local
    driver_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'chromedriver'))
    if os.path.exists(driver_path):
        return driver_path

    # 3: home
    driver_path = os.path.abspath(os.path.join(
        os.path.expanduser('~'), 'chromedriver'))
    if os.path.exists(driver_path):
        return driver_path

    raise DriverPathNotFoundError


class Controller(object):
    _stop = False

    def __init__(self, radio, playback=60):
        self.radio = radio
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=playback)
        print('Start: {}'.format(self.start_time.isoformat()))
        print('End: {}'.format(self.end_time.isoformat()))

        self.prompt = threading.Thread(target=self._prompt)
        self.prompt.start()

    def _prompt(self):
        while not self._stop:
            try:
                user_in = raw_input('>> ')
            except EOFError:
                self.stop()
                break
            if user_in == 'q()':
                self.stop()
            if user_in == 'pause()':
                self.radio.play_or_stop()

    def _start_loop(self):
        while not self._stop:
            sleep(1)
            if self.end_time < datetime.now():
                self.stop()

    def start(self):
        self._start_loop()

    def stop(self):
        self._stop = True


def main():

    channels = get_channels()
    args = parse_args(channels.keys())
    channel = channels[args.channel]
    driver_path = get_driver_path(args)

    print('Driver: {}'.format(driver_path))
    print('Channel: {}'.format(channel['name'].encode('utf_8')))

    with Radio(driver_path, channel['url']) as radio:
        controller = Controller(radio, args.playback_seconds)
        controller.start()

    exit()


def _check_encoding():
    if sys.getdefaultencoding() == 'utf-8':
        return
    print('''{}/sitecustomize.pyに以下を記載
    import sys
    sys.setdefaultencoding(\'utf-8\')
    '''.format(get_python_lib()))
    exit()


if __name__ == '__main__':
    _check_encoding()
    main()
