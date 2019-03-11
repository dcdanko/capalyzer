#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools
setuptools.setup(
    name='capalyzer',
    version='2.4.3',
    description="Parsing functionality for the metasub CAP",
    author="David C. Danko",
    author_email='dcdanko@gmail.com',
    url='https://github.com/dcdanko/capalyzer',
    packages=setuptools.find_packages(),
    package_dir={'capalyzer': 'capalyzer'},
    install_requires=[
        'click',
        'pandas',
        'scipy',
        'numpy',
    ],
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
