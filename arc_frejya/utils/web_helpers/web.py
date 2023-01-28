#!/usr/bin/python3
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

__author__ = 'Adrián Rodríguez Carneiro'


class Web(object):
    __TIMEOUT = 10

    def __init__(self, web_driver: webdriver):
        super(Web, self).__init__()
        self.driver_wait = WebDriverWait(web_driver, Web.__TIMEOUT)
        self.driver = web_driver

    def open(self, url: str):
        self.driver.get(url)

    def maximize(self):
        self.driver.maximize_window()

    def title(self):
        return self.driver.title

    def current_url(self):
        return self.driver.current_url

    def get_text_xpath(self, xpath: str):
        return self.driver_wait.until(ec.presence_of_element_located((By.XPATH, xpath))).text

    def find_by_xpath(self, xpath: str):
        return self.driver_wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))

    def finds_by_xpath(self, xpath: str):
        return self.driver_wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))

    def find_by_xpath_displayed(self, xpath: str):
        return self.driver_wait.until(ec.visibility_of_element_located((By.XPATH, xpath))).is_displayed()

    def find_by_name(self, name: str):
        return self.driver_wait.until(ec.visibility_of_element_located((By.NAME, name)))

    def finds_by_name(self, name: str):
        return self.driver_wait.until(ec.presence_of_all_elements_located((By.NAME, name)))

    def find_by_id(self, id: str):
        return self.driver_wait.until(ec.visibility_of_element_located((By.ID, id)))

    def find_by_id_displayed(self, id_value: str):
        return self.driver_wait.until(ec.presence_of_element_located((By.ID, id_value))).is_displayed()

    def finds_by_id(self, id: str):
        return self.driver_wait.until(ec.presence_of_all_elements_located((By.ID, id)))

    def find_by_class_name(self, classname: str):
        return self.driver_wait.until(ec.visibility_of_element_located((By.CLASS_NAME, classname)))

    def finds_by_class_nam(self, classname: str):
        return self.driver_wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, classname)))

    def find_by_css_selector(self, css_selector: str):
        return self.driver_wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

    def finds_by_css_selector(self, css_selector: str):
        return self.driver_wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    def switch_frame(self, frame):
        return self.driver.switch_to.frame(frame)

    def click_element_by_xpath(self, xpath: str):
        return self.driver_wait.until(ec.element_to_be_clickable((By.XPATH, xpath))).click()

    def close(self):
        self.driver.quit()
