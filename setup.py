#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools
setuptools.setup(
    name='capalyzer',
    version='2.15.5',
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
        'umap-learn',
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
    package_data={'capalyzer': [
        'packet_parser/ncbi_tree/*.dmp.gz',
        'packet_parser/microbe-directory.csv',
    ]},
)
