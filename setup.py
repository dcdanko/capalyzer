#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    # No requirements.
]

setup(
    name='capalyzer',
    version='1.0.2',
    description="Implementation of the popular node-archy tool in python",
    author="David C. Danko",

    author_email='dcdanko@gmail.com',
    url='https://github.com/dcdanko/pyarchy',
    packages=[
        'metasub_cap_downstream',
    ],
    package_dir={'metasub_cap_downstream':
                 'metasub_cap_downstream'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='metasub',
    entry_points={
        'console_scripts': [
            'capalyzer=metasub_cap_downstream.cli:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
