# -*- coding: utf-8 -*-
"""
Django site tools
===============================================

.. module:: django-sitetools
    :platform: Django
    :synopsis: Django site tools
.. moduleauthor:: (C) 2013 Oliver Gutiérrez
"""
# Python imports
import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sitetools',
    packages = find_packages(),
    version='0.1',
    description='Django site tools',
    long_description=README,
    license='MIT License',
    author="Oliver Gutiérrez",
    author_email="ogutsua@gmail.com",
    url = 'https://github.com/R3v1L/django-sitetools',
    keywords = ['sitetools', 'django', 'utility', ],
    classifiers = [],
    # download_url = '',
)
