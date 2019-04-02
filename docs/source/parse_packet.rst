Parsing a Data Packet
=====================


Capalyzer provides a class ``DataTableFactory`` to produce datatables, typically as `Pandas <https://pandas.pydata.org/>`_ ``DataFrames``. The class can parse tables for:

-   Taxonomy
-   Alpha Diversity
-   Beta Diversity
-   Rarefaction Analysis
-   Average Genome Size
-   Human Microbiome Project Similarity
-   Antimicrobial Resistance Genes
-   Pathways and Functional Profiling
-   Abundance of Common Macrobial Species
-   Proportions of Classified Reads


Alpha Diversity
---------------

The capalyzer supports a number of alpha diversity metrics including:

-   shannon entropy
-   richness
-   chao1 richness

Beta Diversity
--------------

The capalyzer supports the following beta diversity metrics:

-   Jensen Shannon Distance
-   Rho Proportionality