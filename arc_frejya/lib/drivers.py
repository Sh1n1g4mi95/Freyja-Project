# coding: utf-8
import logging
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as elemTree
import zipfile
from enum import Enum
from io import BytesIO


# ToDo: revisar y desarrollar esto bien
__author__ = 'Adrián Rodríguez Carneiro'


class VerWebDriver:
    class BrowserType(Enum):
        chrome = {'name': "Chrome", 'driver': "chromedriver"}
        firefox = {'name': "Firefox", 'driver': "geckodriver"}
        edge = {'name': "Edge", 'driver': "msedgedriver"}

    def __init__(self, web_driver_dir: str, browser_type: str):
        self.web_driver_dir = web_driver_dir
        try:
            self.browser_type = self.BrowserType.mro()[0][browser_type.lower()]
        except Exception as e:
            print("Not supported Browser")
            raise Exception("Not supported Browser")
        self.driver_path = self.web_driver_dir + os.sep + self.get_driver_filename()

    def get_driver_filename(self):
        """
        Returns the filename of the binary for the current platform.
        :return: Binary filename
        """
        return self.browser_type.value['driver'] + ('.exe' if sys.platform.startswith('win') else "")

    def get_driver_version(self):
        version = subprocess.check_output([self.driver_path, '-V'])
        version = re.match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        return version

    def get_nav_version(self):
        """
        :return: the version of navigator installed on client
        """
        # ToDo: hacerlo para el resto de so (ahora está solo para windows)
        #       Con esto también se verifica que el navegador está instalado en el sistema
        version = ""
        platform, _ = get_platform_architecture()
        if platform == 'linux':
            # ToDo: desarrollar esto bien en linux
            path = self.get_linux_executable_path()
            with subprocess.Popen([path, '--version'], stdout=subprocess.PIPE) as proc:
                if self.browser_type.name == "chrome":
                    version = proc.stdout.read().decode('utf-8').replace('Chromium',
                                                                         '').replace('Google Chrome', '').strip()
        elif platform == 'mac':
            if self.browser_type.name == "chrome":
                process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                                            '--version'], stdout=subprocess.PIPE)
                version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
        elif platform == 'win':
            version = self.get_nav_version_win(self.browser_type.name)
        else:
            return
        return version

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
        return version

    @staticmethod
    def get_linux_executable_path():
        # ToDo: probar y refinar esta parte de linux, da problemas en función de la distribución
        """
        Look through a list of candidates for Google Chrome executables that might
        exist, and return the full path to first one that does. Raise a ValueError
        if none do.
        :return: the full path to a Chrome executable on the system
        """
        # ToDo: hacerlo para el resto de navegadores (ahora está solo para chrome)
        for executable in (
                "google-chrome",
                "google-chrome-stable",
                "google-chrome-beta",
                "google-chrome-dev",
                "chromium-browser",
                "chromium",
        ):
            path = shutil.which(executable)
            if path is not None:
                return path
        raise ValueError("No chrome executable found on PATH")

    def download_webdriver(self):
        """
        Downloads, unzips and installs webdriver.
        If a webdriver binary is found in PATH it will be copied, otherwise downloaded.
        :return: The file path of webdriver
        """
        nav_version = self.get_nav_version()
        if not nav_version:
            logging.debug(f'{self.browser_type.value["name"]} is not installed.')
            return Exception(f'{self.browser_type.value["name"]} is not installed.')
        navdrive_version = self.get_matched_navdrive_version(self.browser_type.value["name"], nav_version)
        if not navdrive_version:
            logging.warning(f'Can not find driver for currently installed {self.browser_type.value["name"]} version.')
            return Exception(f'Can not find driver for currently installed {self.browser_type.value["name"]} version.')

        if os.path.isfile(self.driver_path):
            os.remove(self.driver_path)
        elif not os.path.isdir(self.web_driver_dir):
            os.makedirs(self.web_driver_dir)

        logging.info(f'Downloading {self.browser_type.value["driver"]} ({navdrive_version})...')
        url = self.get_driver_url(nav=self.browser_type.name, version=navdrive_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError('Not Found')
        except urllib.error.URLError:
            raise RuntimeError(f'Failed to download {self.browser_type.value["driver"]} archive: {url}')
        archive = BytesIO(response.read())
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extract(self.get_driver_filename(), self.web_driver_dir)
        if not os.access(self.driver_path, os.X_OK):
            os.chmod(self.driver_path, 0o744)
        return self.driver_path

    @staticmethod
    def get_matched_navdrive_version(nav: str, version: str):
        """
        :param nav: name of navigator string
        :param version: webdriver version string
        :return: the version of chromedriver
        """
        if str.lower(nav) == "chrome":
            doc = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
            root = elemTree.fromstring(doc)
            for k in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
                if k.text.find(version.split('.')[0] + '.') == 0:
                    return k.text.split('/')[0]
        elif str.lower(nav) == "firefox":   # Nota: este navegador es especialito
            return "v0.29.0"        # Se elige la versión a pedalete
        elif str.lower(nav) == "edge":
            doc = urllib.request.urlopen('https://msedgedriver.azureedge.net').read()
            root = elemTree.fromstring(doc)
            for k in root[0].iter("Name"):
                if k.text.find(version.split('.')[0] + '.') == 0:
                    return k.text.split('/')[0]
            return

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

    def verify_current_driver(self):
        # ToDo: poner logs informativos y tal, crear ficheros de logs de salida para tener mayor trazabilidad
        if self.browser_type.name == 'firefox':     # Nota: el driver de firefox y su navegador no coinciden en version
            if not os.path.isfile(self.driver_path):
                self.download_webdriver()
        elif not os.path.isfile(self.driver_path) or \
                (self.get_nav_version().split('.')[0] != self.get_driver_version().split('.')[0]):
            self.download_webdriver()


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
        raise RuntimeError('Could not determine webdriver download URL for this platform.')
    return platform, architecture
