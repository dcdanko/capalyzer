Building a Data Packet
======================

Capalyzer contains a command line tool to build a summary data packet from the outputs of the MetaSUB Core Analysis Pipeline

This packet contains a series of nested data folders and tables for each sample in your project, all of which are described below. Unless otherwise specified, data tables are in a comma-delimited format. Samples are stored in rows, while features (like genes, or species) are in columns.

The root folder has files and folders for all data from all samples as follows:

 - README.md
 - /antimicrobial_resistance
 - /city_packets
 - /metadata
 - /other
 - /pathways
 - /taxonomy
 - /teaching_packet


Key Abbreviations in the files:
 - RPKM, Reads per Kilobase Millions
 - RPKMG, Reads per Kilobase Millions per Genome Megabases

 To build a packet run the following command

 .. code-block:: bash 

    capalyzer make-tables <cap result dir> <data packet dir>

Antimicrobial Resistance
------------------------

All reads per sample were aligned to reference sequences in the Comprehensive Antibiotic Resistance Database (CARD). This was done using Bowtie2 to CARD (ca. April 2018)  
Output includes metrics of RPKM and RPKMG for:

 - *card_amr_rpkm[g].csv:*  alignments to all genes in CARD in units of either RPKM or RPKMG
 - *megares_amr_\*.csv:* summaries of metrics  for the specified AMR category(*), including: 
     - megares_amr_class: class (n=20, e.g. Aminocoumarins)
     - megares_amr_gene: specific gene (n=1,429, e.g. Aminoglycoside_N-acetyltransferases)
     - megares_amr_group: AMR group (n=345, e.g. AAC2-PRIME)
     - megares_amr_mech: mechanism (n=76, e.g. 16S rRNA methyltransferases)

Pathways
--------

This folder holds all the reads mapped to the HuMaNN2 pathways, both in terms of raw coverage and the relative abundances:
 - *uniref90.humann2.pathways_relab.csv:* The relative abundance of DNA mapped to each pathway
 - *uniref90.humann2.pathways_coverage.csv:* The fraction of genes covered in each pathway

Taxonomy
--------

This folder holds the output from MetaPhlAn2 (version 2.2) as well as reads mapped using KrakenHLL (v0.3.2) to RefSeq Microbial (ca. April 2018), including:
 - *refseq.krakenhll_wide.read_counts.csv:* Raw read counts for all taxa obtained by running KrakenUniq on RefSeq Microbial. Headers include taxa name, mpa string, taxa rank, and taxa id. All taxa have at least 256 unique kmers.
 - *refseq.krakenhll_longform.csv.gz:* Raw read counts, coverage, kmer counts, and percent abundance for all taxa. Taxa includes taxa name, mpa string, taxa rank, and taxa id. This table is in a long format suitable for search with tools like *grep*. This table is not replicated in the city packets.
 - *metaphlan2.relabund.csv:* Percent abundances of different taxa identified by MetaSUB.
 - *refseq.krakenhll_species.csv:* Raw read counts for each species in each sample. Taxa have at least 256 unique kmers.

Other
-----

This folder has other annotation files and data references that were used for the calculation of all statistics. This includes:
 - *average_genome_size.csv:* estimated average bacterial genome size for each sample obtained with Microbe Census
 - *human_microbiome_project_comparison.csv:* similarity between MetaSUB samples and representative samples from the human body from the `HMP <https://www.hmpdacc.org>`_ This table has three columns: MetaSUB UUID, Human Body Site, Cosine Similarity between samples. Cosine Similarity is based off of the MetaPhlAn2 taxonomic profile.
 - *macrobe_abundances.csv:* the estimated RPKM values for the genomes of various non-human, non-microbial organisms.
 - *read_classification_proportions.csv:* the proportion of reads assigned to major categories (e.g. Human, Unknown)

