#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from distutils.sysconfig import get_python_lib
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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


def get_channels():
    channel_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'channel.json'))
    with open(channel_path) as channel:
        return json.loads(channel.read())


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


class Radio(object):

    def __init__(self, driver_path, url, options=None):
        self.driver = webdriver.Chrome(driver_path, chrome_options=options)
        self.driver.get(url)

    def play_or_stop(self):
        self._play_button.click()

    def exit(self):
        self.driver.quit()

    @property
    def _play_button(self):
        return self.driver.find_element_by_class_name('btn--primary')

    def __enter__(self):
        self.play_or_stop()

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()


def main():
    options = Options()
    options.add_argument('--headless')

    channels = get_channels()
    args = parse_args(channels.keys())
    channel = channels[args.channel]
    driver_path = get_driver_path(args)

    start = datetime.now()
    end = start + timedelta(seconds=args.playback_seconds)

    print('Driver: {}'.format(driver_path))
    print('Channel: {}'.format(channel['name'].encode('utf_8')))
    print('Start: {}'.format(start.isoformat()))
    print('End: {}'.format(end.isoformat()))

    with Radio(driver_path, channel['url'], options):
        sleep(args.playback_seconds)


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
