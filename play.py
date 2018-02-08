import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
    driver_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'chromedriver_linux64_2.34')
    url = 'http://radiko.jp/#!/live/TBS'
    options = Options()
    options.add_argument('--headless')

    with Radio(driver_path, url, options):
        sleep(60 * 60)


if __name__ == '__main__':
    main()
