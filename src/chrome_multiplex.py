#!/usr/bin/env python
# coding=utf-8

from os import PathLike
from typing import Union, Optional
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.chrome_common import ChromeCommon


class ChromeMultiplex(ChromeCommon):
    def __init__(self, port: int = 9992, wait_time: Union[int, float] = 0.2, driver_path: Optional[PathLike] = None):
        self.port = port
        self.wait_time = wait_time
        self.driver: webdriver.Chrome = self.get_driver(driver_path)
        super().__init__(self.driver, self.wait_time)

    @staticmethod
    def get_default_chromedriver():
        chromedriver = Path(__file__).parent.joinpath('../data/chromedriver.exe')
        if chromedriver.is_file():
            return chromedriver.resolve().__str__()
        raise FileNotFoundError(f'No driver found at {chromedriver}')

    def get_driver(self, driver_path: Optional[PathLike] = None) -> webdriver.Chrome:
        if driver_path is None or not Path(driver_path).is_file():
            driver_path = self.get_default_chromedriver()
        options = Options()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")
        # noinspection PyUnreachableCode
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        return driver
