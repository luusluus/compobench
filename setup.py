import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='compositions', 
    version='1.0',
    install_requires=required
)

setup(
    name='experiments',
    version='1.0',
    install_requires=required
)