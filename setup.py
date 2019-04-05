#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools
setuptools.setup(
    name='capalyzer',
<<<<<<< HEAD
    version='2.7.0',
=======
    version='2.6.0',
>>>>>>> 09eb04bc43ce473df38b02ec5141dd202ec90062
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
