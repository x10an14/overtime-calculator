#!/usr/bin/env python

from setuptools import setup

setup(
    name='Overtime-Calculator',
    version='0.3',
    description='Python application to help calculate work overtime surplus/deficit.',
    author='Christian Chavez',
    author_email='x10an14@users.noreply.github.com',
    # url='https://www.non-existing.com',
    setup_requires=[
        'hug',
        'bcrypt',
        'pyjwt',
    ],
    tests_require=[
        'pytest',
        'hypothesis',
        'coveralls',
    ],
    packages=['overtime_calculator'],
)
