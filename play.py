import os
from time import sleep

from selenium import webdriver

DRIVER_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'chromedriver_mac64')
URL = 'http://radiko.jp/#!/live/TBS'


class Radio(object):

    def __init__(self, driver_path, url):
        self.driver = webdriver.Chrome(driver_path)
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
    with Radio(DRIVER_PATH, URL):
        sleep(60 * 60)


if __name__ == '__main__':
    main()
