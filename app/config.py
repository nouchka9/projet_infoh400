# -*- coding: utf-8 -*-
"""
Configuration globale de l'application.
"""
class Config:
    def __init__(self):
        self.settings = {
            "hosts": {
                "ADMISSION_SYSTEM": {"host": "localhost", "port": 2575},
                "LAB_SYSTEM": {"host": "localhost", "port": 2575},
                "ORDER_SYSTEM": {"host": "localhost", "port": 2575},
                "PHARMACY_SYSTEM": {"host": "localhost", "port": 2575}
            }
        }

    def get(self, key):
        return self.settings.get(key)

    def get_section(self, section):
        return self.settings.get(section, {})
