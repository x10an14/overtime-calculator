#!/usr/bin/env python

from setuptools import setup

setup(
    name='Overtime-Calculator',
    version='0.1',
    # description='Python Distribution Utilities',
    # author='Greg Ward',
    # author_email='gward@python.net',
    # url='https://www.python.org/sigs/distutils-sig/',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=['src'],)
