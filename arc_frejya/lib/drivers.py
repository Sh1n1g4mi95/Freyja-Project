#!/usr/bin/python3
# coding: utf-8
import logging
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as elemTree
import zipfile
from enum import Enum
from io import BytesIO


__author__ = 'Adrián Rodríguez Carneiro'


class VerWebDriver:
    class BrowserType(Enum):
        chrome = {'name': "Chrome", 'driver': "chromedriver"}
        firefox = {'name': "Firefox", 'driver': "geckodriver"}
        edge = {'name': "Edge", 'driver': "msedgedriver"}

    def __init__(self, web_driver_dir: str, browser_type: str):
        """
            Constructor of the class.

            :param web_driver_dir: Directory where the webdriver is
            :param browser_type: Browser type name
        """
        self.logger = logging.getLogger(__name__)  # Logger de la clase
        self.logger.setLevel(logging.DEBUG)     # ToDo: setear esto en función de properties
        if not self.logger.hasHandlers():  # Si el logger de la clase no tiene handlers, se crean.
            # Handler nivel debug con salida a fichero
            logs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "logs" + os.sep
            log_file = logs_dir + __name__.split(".")[-1] + ".log"
            if not os.path.isfile(log_file):
                os.open(log_file, os.O_APPEND|os.O_CREAT)
            handler_log_file = logging.FileHandler(log_file, mode='a', encoding='UTF-8')
            handler_log_file.setLevel(logging.DEBUG)
            handler_log_file.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s:%(message)s'))
            self.logger.addHandler(handler_log_file)
            # Handler nivel warning con salida a consola
            console_handler = logging.StreamHandler(stream=sys.stdout)
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s:%(message)s'))
            self.logger.addHandler(console_handler)

        self.web_driver_dir = web_driver_dir
        try:
            self.logger.info(" Validating browser type " + browser_type)
            self.browser_type = self.BrowserType.mro()[0][browser_type.lower()]
        except Exception as e:
            self.logger.error(" Not supported Browser: " + str(e))
            raise Exception("Not supported Browser")
        self.driver_path = self.web_driver_dir + os.sep + self.get_driver_filename()

    def get_driver_filename(self):
        """
            Returns the filename of the binary for the current platform.

            :return: Binary filename
        """
        return self.browser_type.value['driver'] + ('.exe' if sys.platform.startswith('win') else "")

    def get_driver_version(self):
        """
            Returns the version of the binary webdriver for the current platform.

            :return: Binary filename version
        """
        self.logger.info(f'Obtaining {self.browser_type.value["driver"]} webdriver version.')
        version = subprocess.check_output([self.driver_path, '-V'])
        version = re.match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        return version

    def get_navigator_version(self, browser_name: str, platform: str, logger: logging):
        """
            Returns the version of navigator installed on client.

            :param browser_name: Name of navigator
            :param platform: Platform (Linux, Windows, ...)
            :param logger: Logger
            :return: Navigator version
        """
        try:
            logger.info(f'Obtaining {browser_name} navigator version.')
            return eval("self.get_nav_version_"+platform[0:3])(browser_name)
        except Exception as e:
            raise e

    def get_nav_version(self):
        """
            Returns the version of navigator installed on client.

            :return: Navigator version
        """
        try:
            platform, _ = get_platform_architecture()
            return self.get_navigator_version(platform, self.browser_type.name, self.logger)
        except Exception as e:
            self.logger.error(e)
            sys.exit(-14)

    @staticmethod
    def get_nav_version_lin(browser_name: str):
        # ToDo: desarrollar esto. Encontrar forma de obtener las versiones de
        #       navegadores en linux de forma eficiente y escalable para todos
        # browser_name = str.lower(browser_name)
        # version = ""
        # if version:
        #     return version
        # else:
        raise RuntimeError(" Version of '" + browser_name + "' Navigator could not be obtained for this Linux OS")

    @staticmethod
    def get_nav_version_mac(browser_name: str):
        # ToDo: desarrollar esto, no tengo un MAC XD
        # browser_name = str.lower(browser_name)
        # version = ""
        # if browser_name == "chrome":
        #     process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        #                                 '--version'], stdout=subprocess.PIPE)
        #     version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
        # if version:
        #     return version
        # else:
        raise RuntimeError(" Version of '" + browser_name + "' Navigator could not be obtained for this MAC OS")

    @staticmethod
    def get_nav_version_win(browser_name: str):
        browser_name = str.lower(browser_name)
        path_uninstall = "\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'"
        registry_paths = "@('HKLM:\\Software" + path_uninstall + ",'HKLM:\\Software\\WOW6432Node" + path_uninstall + \
                         ",'HKCU:\\Software" + path_uninstall + ",'HKCU:\\Software\\WOW6432Node" + path_uninstall + ")"

        comando = ""
        if browser_name == "chrome":
            comando = 'Get-ItemProperty ' + registry_paths + \
                      ' -ErrorAction SilentlyContinue | Where-Object {$_.DisplayName' \
                      ' -like "*Chrome*" } | findstr "DisplayVersion"'
        elif browser_name == "firefox":
            comando = 'Get-ItemProperty ' + registry_paths + \
                      ' -ErrorAction SilentlyContinue | Where-Object {$_.DisplayName' \
                      ' -like "*Mozilla Firefox*" } | findstr "DisplayVersion"'
        elif browser_name == "edge":
            comando = 'Get-ItemProperty ' + registry_paths + \
                      ' -ErrorAction SilentlyContinue | Where-Object {$_.InstallLocation -like' \
                      ' "*Microsoft\Edge\Application*" } | findstr "DisplayVersion"'
        if comando:
            process = subprocess.Popen(
                ['powershell', '-command', comando],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            # ToDo: poner comprobación de que el comando ha ido ok y tal
            version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
        else:
            raise Exception("Not supported navigator: " + browser_name)
        if version:
            return version
        else:
            raise RuntimeError(" Version of '" + browser_name + "' Navigator could not be obtained for this Windows OS")

    def download_webdriver(self, nav_version=None):
        """
            Downloads, unzips and installs webdriver.
            If a webdriver binary is found in PATH it will be copied, otherwise downloaded.

            :return: The file path of webdriver
        """
        self.logger.warning(f'Downloading webdriver...')
        browser_name = self.browser_type.value["name"]
        if not nav_version:
            nav_version = self.get_nav_version()

        try:
            navdrive_version = self.get_matched_navdrive_version(browser_name, nav_version)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(f'Can not find driver for currently {browser_name} installed version.')
            sys.exit(-7)

        if os.path.isfile(self.driver_path):
            self.logger.info(f'Deleting file {self.driver_path} ...')
            os.remove(self.driver_path)
        elif not os.path.isdir(self.web_driver_dir):
            self.logger.info(f'Creating directory {self.web_driver_dir})...')
            os.makedirs(self.web_driver_dir)

        self.logger.info(f'Downloading {self.browser_type.value["driver"]} ({navdrive_version})...')
        url = self.get_driver_url(nav=self.browser_type.name, version=navdrive_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError('Not Found')
        except urllib.error.URLError:
            self.logger.error(f'Failed to download {self.browser_type.value["driver"]} archive: {url}')
            raise RuntimeError(f'Failed to download {self.browser_type.value["driver"]} archive: {url}')
        archive = BytesIO(response.read())
        self.logger.info(f'Extracting files of {archive}...')
        with zipfile.ZipFile(archive) as zip_file:
            self.logger.info(f'Extracting {self.get_driver_filename()} in {self.web_driver_dir}...')
            zip_file.extract(self.get_driver_filename(), self.web_driver_dir)
        if not os.access(self.driver_path, os.X_OK):
            os.chmod(self.driver_path, 0o744)
        return self.driver_path

    @staticmethod
    def get_matched_navdrive_version(nav: str, version: str):
        """
           Method to get the version of the given navigator.

            :param nav: name of navigator string
            :param version: webdriver version string
            :return: the version of chromedriver
        """
        try:
            if str.lower(nav) == "chrome":
                doc = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
                root = elemTree.fromstring(doc)
                for k in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
                    if k.text.find(version.split('.')[0] + '.') == 0:
                        return k.text.split('/')[0]
            elif str.lower(nav) == "firefox":   # Nota: este navegador es especialito
                return "v0.29.0"        # Se elige la versión a pedalete
            elif str.lower(nav) == "edge":
                with urllib.request.urlopen('https://msedgedriver.azureedge.net') as response:
                    doc = response.read()
                    root = elemTree.fromstring(doc)
                    for k in root[0].iter("Name"):
                        if k.text.find(version.split('.')[0] + '.') == 0:
                            return k.text.split('/')[0]
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def get_driver_url(nav: str, version: str):
        """
            Generates the download URL for current platform , architecture and the given version.
            Supports Linux, MacOS and Windows.

            :param nav: name of navigator string
            :param version: webdriver version string
            :return: Download URL for webdriver
        """
        platform, architecture = get_platform_architecture()
        base_url = ""
        nav_indicator = ""
        if str.lower(nav) == "chrome":
            base_url = 'https://chromedriver.storage.googleapis.com/'
            nav_indicator = '/chromedriver_'
        elif str.lower(nav) == "firefox":   # Nota: este navegador es especialito
            version = "v0.29.0"     # Se elige la versión a pedalete
            base_url = 'https://github.com/mozilla/geckodriver/releases/download/'
            nav_indicator = '/geckodriver-' + version + '-'
        elif str.lower(nav) == "edge":
            base_url = 'https://msedgedriver.azureedge.net/'
            nav_indicator = '/edgedriver_'
        return base_url + version + nav_indicator + platform + architecture + '.zip'

    def verify_nav_driver(self):
        try:
            self.logger.info(f'Verifying {self.browser_type.value["driver"]} webdriver version.')
            driver_major_version = ""
            driver_exists = os.path.isfile(self.driver_path)
            if driver_exists:
                driver_major_version = self.get_driver_version().split('.')[0]
            else:   # Nota: el driver de firefox y su navegador no coinciden en version
                self.logger.warning(f'Webdriver for {self.browser_type.value["driver"]} navigator is not in the path.')

            self.logger.info(f'Verifying {self.browser_type.value["driver"]} navigator version.')
            platform, _ = get_platform_architecture()
            if platform == 'win':   # ToDo: desarrollor para otras plataformas (Linux) y quitar el if
                nav_version = self.get_navigator_version(self.browser_type.name, platform, self.logger)
                major_version = nav_version.split('.')[0]
                if major_version != driver_major_version:
                    self.logger.warning(f'Webdriver major version ({driver_major_version}) does not match'
                                        f' with navigator major version ({major_version}).')
                    if self.browser_type.name == 'firefox':
                        if not driver_exists:
                            self.logger.error(f'Webdriver for Firefox navigator is not allowed to auto download.')
                            # ToDo: hacer en exit del programa
                    else:
                        self.download_webdriver(nav_version=nav_version)
        except Exception as e:
            raise e


def get_platform_architecture():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('The platform achitecture is not supported')
    return platform, architecture
