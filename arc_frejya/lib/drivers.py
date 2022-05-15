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
        edge = {'name': "Edge", 'driver': "msedge"}

    def __init__(self, web_driver_dir: str, browser_type: str):
        self.web_driver_dir = web_driver_dir
        self.browser_type = self.BrowserType.mro()[0][browser_type.lower()]
        self.driver_path = self.web_driver_dir + os.sep + self.get_driver_filename()

    def get_driver_filename(self):
        """
        Returns the filename of the binary for the current platform.
        :return: Binary filename
        """
        return self.browser_type.value['driver'] + ('.exe' if sys.platform.startswith('win') else "")

    def get_driver_version(self):
        version = subprocess.check_output([self.driver_path, '-v'])
        version = re.match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        return version

    def get_nav_version(self):
        """
        :return: the version of chrome installed on client
        """
        # ToDo: hacerlo para el resto de navegadores (ahora está solo para chrome)
        version = "No está aún desarrollado"
        platform, _ = get_platform_architecture()
        if platform == 'linux':
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
            if self.browser_type.name == "chrome":
                process = subprocess.Popen(
                    ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                )
                output = process.communicate()
                if output:
                    version = output[0].decode('UTF-8').strip().split()[-1]
                else:
                    process = subprocess.Popen(
                        ['powershell', '-command', '$(Get-ItemProperty -Path Registry::'
                                                   'HKEY_CURRENT_USER\\Software\\Google\\chrome\\BLBeacon).version'],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
                    )
                    version = process.communicate()[0].decode('UTF-8').strip()
        else:
            return
        return version

    @staticmethod
    def get_linux_executable_path():
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
        Downloads, unzips and installs chromedriver.
        If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.
        :return: The file path of chromedriver
        """
        # ToDo: hacerlo para el resto de navegadores (ahora está solo para chrome)
        nav_version = self.get_nav_version()
        if not nav_version:
            logging.debug(f'{self.browser_type.value["name"]} is not installed.')
            return
        navdrive_version = self.get_matched_navdrive_version(nav_version)
        if not navdrive_version:
            logging.warning(f'Can not find driver for currently installed {self.browser_type.value["name"]} version.')
            return

        if os.path.isfile(self.driver_path):
            os.remove(self.driver_path)
        elif not os.path.isdir(self.web_driver_dir):
            os.makedirs(self.web_driver_dir)

        logging.info(f'Downloading {self.browser_type.value["driver"]} ({navdrive_version})...')
        url = self.get_chromedriver_url(version=navdrive_version)
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
    def get_matched_navdrive_version(version):
        """
        :param version: the version of chrome
        :return: the version of chromedriver
        """
        # ToDo: hacerlo para el resto de navegadores (ahora está solo para chrome)
        doc = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
        root = elemTree.fromstring(doc)
        for k in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
            if k.text.find(version.split('.')[0] + '.') == 0:
                return k.text.split('/')[0]
        return

    @staticmethod
    def get_chromedriver_url(version):
        """
        Generates the download URL for current platform , architecture and the given version.
        Supports Linux, MacOS and Windows.
        :param version: chromedriver version string
        :return: Download URL for chromedriver
        """
        # ToDo: hacerlo para el resto de navegadores (ahora está solo para chrome)
        base_url = 'https://chromedriver.storage.googleapis.com/'
        platform, architecture = get_platform_architecture()
        return base_url + version + '/chromedriver_' + platform + architecture + '.zip'

    def verify_current_driver(self):
        if not os.path.isfile(self.driver_path) or \
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
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform, architecture
