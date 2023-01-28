#!/usr/bin/python3
# coding: utf-8
import datetime
import os
import sys
import time

path_frejya_arc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path_frejya_arc not in sys.path:
    sys.path.append(path_frejya_arc)

from arc_frejya.lib.frejya_misc import title
from arc_frejya.utils.web_helpers.web_factory import get_web

__author__ = 'Adrián Rodríguez Carneiro'


def cha_cha_slide(web):
    web.maximize()
    web.open("https://www.google.com/")
    web.find_by_id("L2AGLb").click()
    web.find_by_xpath("//input[@name='q']").send_keys('Cha Cha Slide')
    web.click_element_by_xpath("//input[@name='btnK']//following::input[@name='btnK']")
    # web.open("https://www.google.com/search?q=Cha+Cha+Slide")
    for a in range(15):
        web.click_element_by_xpath("//img[contains(@src, 'https://www.google.com/logos/fnbx/cha_cha_slide')]")
        time.sleep(2)   # ToDo: hacerlo sin el sleep
    web.close()


def main():
    """Main Execution"""
    title()
    # ToDo: usar argparse para poder obtener parámetros de ejecución de forma limpia y sencilla

    print('Started at:', datetime.datetime.now())
    for browser in ["Chrome", "Firefox", "Edge"]:
        cha_cha_slide(get_web(browser=browser))
    print('Ended at:', datetime.datetime.now())


if __name__ == "__main__":
    sys.exit(main())
