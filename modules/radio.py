# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _default_options():
    options = Options()
    options.add_argument('--headless')
    return options


class Radio(object):

    def __init__(self, driver_path, url, options=_default_options()):
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
