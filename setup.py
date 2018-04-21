#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='capalyzer',
    version='1.0.2',
    description="Parsing functionality for the metasub CAP",
    author="David C. Danko",
    author_email='dcdanko@gmail.com',
    url='https://github.com/dcdanko/capalyzer',

    packages=['capalyzer'],
    package_dir={'capalyzer': 'capalyzer'},

    install_requires=[],

    entry_points={
        'console_scripts': [
            'capalyzer=capalyzer.cli:main'
        ]
    },

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
