# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="hl7_messenger",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "hl7apy>=1.3.3",
        "tk",
        "pytest",
        "loguru"
    ],
    entry_points={
        "console_scripts": [
            "hl7-messenger = app.main:main"
        ]
    },
    author="Votre équipe",
    description="Projet HL7 Messenger pour communication hospitalière simplifiée",
)

