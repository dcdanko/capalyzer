# Capalyzer

[![CircleCI](https://circleci.com/gh/dcdanko/capalyzer.svg?style=svg)](https://circleci.com/gh/dcdanko/capalyzer)

[![](https://img.shields.io/pypi/v/capalyzer.svg)](https://pypi.org/project/capalyzer/)

CAPalyzer provides two utilities connected to the [MetaSUB Core Analysis Pipeline](https://github.com/MetaSUB/MetaSUB_CAP). It condenses the results of the CAP into summary data tables and it provides utilities to parse those tables.

## Installation

From PyPi
```
pip install capalyzer
```

From source
```
git clone git@github.com:dcdanko/capalyzer.git
cd capalyzer
python setup.py install
```

## Building a data packet

From the command line
```
capalyzer make-tables <cap result dir> <data packet dir>
```

In Code
```
#! /bin/env python3

from capalyzer.packet_builder import make_all_tables


filenames = make_all_tables(<cap result dir>, <data packet dir>)
for filename in filenames:
    print(filename)
```

## Parsing a data packet
```
#! /bin/env python3

from capalyzer.packet_parser import DataTableFactory

table_factory = DataTableFactory(<data packet dir>)
taxa_tbl = table_factory.taxonomy()
amr_tbl = table_factory.amrs()
```

## Credits

This package is written and maintained by [David C. Danko](mailto:dcdanko@gmail.com)
