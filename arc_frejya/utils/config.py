#!/usr/bin/python3
# coding: utf-8
import configparser

__author__ = 'Adrián Rodríguez Carneiro'


class Config:

    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self, config_file=None):
        self.config_data = configparser.ConfigParser()
        self.config_data.read(config_file if config_file else self.config_file, encoding='utf8')
        return self.config_data

    def get_config_values(self, **kwargs):
        values = {}
        for key in kwargs.keys():
            if self.config_data.has_section(key):
                for var in kwargs[key]:
                    if self.config_data.has_option(key, var):
                        values[var] = self.config_data.get(key, var)
        return values

    def get_config_value(self, variable):
        sections = self.config_data.sections()
        value = None
        for section in sections:
            if self.config_data.has_option(section, variable):
                value = self.config_data.get(section, variable)
            if value:
                break
        return value
