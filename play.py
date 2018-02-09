import os
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

channels = {
    'tbs': 'http://radiko.jp/#!/live/TBS',
}


class DriverPathNotFoundError(Exception):
    pass


def get_driver_path():
    # 0: arg
    if len(sys.argv) >= 2:
        if os.path.exists(sys.argv[1]):
            return sys.argv[1]

    # 1: env
    driver_path = os.environ.get('SELENIUM_DRIVER')
    print(driver_path)
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
    driver_path = get_driver_path()
    url = channels['tbs']
    options = Options()
    options.add_argument('--headless')

    with Radio(driver_path, url, options):
        sleep(60 * 60)


if __name__ == '__main__':
    main()
