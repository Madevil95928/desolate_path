#!/usr/bin/env python
# coding=utf-8

from typing import Union, Optional
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class ChromeCommon:
    def __init__(self, driver: webdriver, wait_time: Union[int, float] = 0.2):
        self.driver = driver
        self.wait_time = wait_time

    def goto_page(self, title: Optional[str] = None):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if self.driver.title == title:
                return True
        raise RuntimeError

    def xpath(self, value: str):
        return self.driver.find_element(By.XPATH, value)

    def scroll_to_element(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
