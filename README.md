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
hmp-tbl = table_factory.hmp()
```

### Getting diversity scores

You can generate alpha diversity metrics using this package.

Available metrics
- shannon entropy
- richness
- chao1 richness

All metrics can be rarefied to a certain number of reads with the `rarefy` parameter. 
```
from capalyzer.packet_parser import DataTableFactory

table_factory = DataTableFactory(<data packet dir>)

krakenhll_richness = table_factory.taxa_alpha_diversity(metric='richness', rarefy=1000000)  # krakenhll is the default tool
metaphlan2_entropy = table_factory.taxa_alpha_diversity(tool='metaphlan2')  # entropy is the default metric
```

Generally `krakenhll` is prefereable to `metaphlan2` as it captures more diversity.

beta diversity scores are also supported
```
from capalyzer.packet_parser import DataTableFactory

table_factory = DataTableFactory(<data packet dir>)

jensen_shannon = table_factory.taxa_beta_diversity(metric='jsd')
rho_proportionality = table_factory.taxa_beta_diversity(metric='rho')
```

Diversity metrics may also be generated using the CLI.
```
capalyzer diversity alpha --help
capalyzer diversity beta --help
```

## Credits

This package is written and maintained by [David C. Danko](mailto:dcdanko@gmail.com)
