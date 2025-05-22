#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction rapide du fichier de configuration
"""

def fix_config_file():
    """Corrige le fichier app/config.py"""
    
    config_content = '''# -*- coding: utf-8 -*-
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
'''
    
    with open("app/config.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("✅ Fichier config.py corrigé")

if __name__ == "__main__":
    fix_config_file()
    print("🎯 Configuration corrigée - Relancez l'application")