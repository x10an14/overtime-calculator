#!/usr/bin/env python

from setuptools import setup

setup(
    name='Overtime-Calculator',
    version='0.1',
    description='Python application to help calculate work overtime surplus/deficit.',
    author='Christian Chavez',
    author_email='x10an14@gmail.com',
    # url='https://www.non-existing.com',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'hypothesis'],
    packages=['src'],
)
