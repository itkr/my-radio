# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import functools
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def _default_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # docker 用
    return options


class Radio(object):

    def __init__(self, driver_path, url, options=_default_options()):
        self.new_driver = functools.partial(
            webdriver.Chrome, driver_path, chrome_options=options)
        self.driver = self.new_driver()
        self.driver.get(url)

    def reload(self, url):
        self.stop()
        self.driver.get(url)
        self.driver.refresh()
        self.play()

    def get_info(self):
        classes = {
            'title': 'live-detail__title',
            'description': 'live-detail__description',
            'cast': 'live-detail__cast',
            'time': 'live-detail__time',
        }
        return {
            key: self.driver.find_element_by_class_name(
                value).text for key, value in classes.items()
        }

    def play(self):
        try:
            self.driver.find_element_by_class_name('player_play').click()
        except NoSuchElementException:
            pass

    def stop(self):
        try:
            self.driver.find_element_by_class_name('player_stop').click()
        except NoSuchElementException:
            pass

    def play_or_stop(self):
        self._play_button.click()

    def exit(self):
        self.driver.quit()

    @property
    def _play_button(self):
        return self.driver.find_element_by_class_name('btn--primary')

    def __enter__(self):
        self.play_or_stop()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()
