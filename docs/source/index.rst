.. capalyzer documentation master file, created by
   sphinx-quickstart on Mon Apr  1 22:06:16 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Capalyzer!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Capalyzer is a python package to summarize and parse metagenomic data. Capalyzer takes output from the `MetaSUB Core Analysis Pipeline <https://github.com/MetaSUB/MetaSUB_CAP>`_ and builds summary data tables. After the data tables have been built capalyzer includes utilities to parse those tables.

Capalyzer aims to remove boilerplate code from metagenomic analyses and provide a consistent interface for secondary analyses. Capalyzer is a comkunity project and is easy to contribute to.

Capalyzer in three points:

-   Tidy and rich summaries of metagenomic analyses
-   Consistent and clean API for parsing files
-   Common statistical and ecological analyses built in

What does it look like?

.. code-block:: python 

    from capalyzer.packet_parser import DataTableFactory

    table_factory = DataTableFactory(<data packet dir>)

    taxa_richness = table_factory.taxa_alpha_diversity(metric='richness')
    taxa_tbl = table_factory.taxonomy()
    amr_tbl = table_factory.amrs()
    hmp_tbl = table_factory.hmp()


You can get the library directly from PyPI::

    pip install capalyzer


Documentation
-------------

This part of the documentation guides you through all of the library's
usage patterns.

.. toctree::
   :maxdepth: 2

   build_packet
   parse_packet

API Reference
-------------

If you are looking for information on a specific function, class, or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   capalyzer.packet_parser
   capalyzer.packet_builder
   capalyzer.packet_builder.sub_factories

Miscellaneous Pages
-------------------

.. toctree::
   :maxdepth: 2

   license

