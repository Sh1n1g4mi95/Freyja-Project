#!/usr/bin/python3
# coding: utf-8
import os
import sys
try:
    from selenium import webdriver
except Exception as e:
    print(e)
    print("Trying to install selenium")
    os.system('pip install selenium')

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

path_frejya_arc = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if path_frejya_arc not in sys.path:
    sys.path.append(path_frejya_arc)

from arc_frejya.lib.drivers import VerWebDriver
from arc_frejya.utils.config import Config
from arc_frejya.utils.web_helpers.web import Web

__author__ = 'Adrián Rodríguez Carneiro'


def get_web(browser=None, workspace=None):
    try:
        # Ruta principal de los útiles y arquitectura principal del framework, si no se especifica workspace,
        # es la tomada por defecto para la carga de properties y drivers
        frejya_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        project_path = os.path.dirname(frejya_path) + os.sep + workspace if workspace else ""
        config_dir = (project_path if project_path else frejya_path)
        drivers_dir = config_dir + os.sep + "drivers"

        if not browser:     # Si no se pasa browser, se carga el que exista en properties
            conf = Config(config_dir + os.sep + "config.ini")
            browser = conf.get_config_value('browser')

        browser = browser.capitalize()

        ver_driver = VerWebDriver(drivers_dir, browser)
        ver_driver.verify_current_driver()
        driver_type = eval("webdriver." + browser)
        return Web(driver_type(executable_path=r'' + ver_driver.driver_path + ''))
    except Exception as e:
        raise e

