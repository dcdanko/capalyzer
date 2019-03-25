
from os.path import join

AMR_DIR = 'antimicrobial_resistance'
CARD_RPKM = join(AMR_DIR, 'card_amr_rpkm.csv')
CARD_RPKMG = join(AMR_DIR, 'card_amr_rpkmg.csv')
MEGARES_CLASS_RPKM = join(AMR_DIR, 'megares_amr_class_rpkm.csv')
MEGARES_CLASS_RPKMG = join(AMR_DIR, 'megares_amr_class_rpkmg.csv')
MEGARES_GENE_RPKM = join(AMR_DIR, 'megares_amr_gene_rpkm.csv')
MEGARES_GENE_RPKMG = join(AMR_DIR, 'megares_amr_gene_rpkmg.csv')
MEGARES_GROUP_RPKM = join(AMR_DIR, 'megares_amr_group_rpkm.csv')
MEGARES_GROUP_RPKMG = join(AMR_DIR, 'megares_amr_group_rpkmg.csv')
MEGARES_MECH_RPKM = join(AMR_DIR, 'megares_amr_mech_rpkm.csv')
MEGARES_MECH_RPKMG = join(AMR_DIR, 'megares_amr_mech_rpkmg.csv')

OTHER_DIR = 'other'
AVE_GENOME_SIZE = join(OTHER_DIR, 'average_genome_size.csv')
HMP_COMPARISON = join(OTHER_DIR, 'human_microbiome_project_comparison.csv')
MACROBES = join(OTHER_DIR, 'macrobe_abundances.csv')
READ_PROPORTIONS = join(OTHER_DIR, 'read_classification_proportions.csv')

PATHWAYS_DIR = 'pathways'
UNIREF90_COV = join(PATHWAYS_DIR, 'uniref90.humann2.pathways_coverage.csv')
UNIREF90_RELAB = join(PATHWAYS_DIR, 'uniref90.humann2.pathways_relab.csv')

TAXA_DIR = 'taxonomy'
MPA_RELAB = join(TAXA_DIR, 'metaphlan2.relabund.csv')
KRAKENHLL_REFSEQ = join(TAXA_DIR, 'refseq.krakenhll_species.csv')
KRAKENHLL_REFSEQ_MEDIUM = join(TAXA_DIR, 'refseq.krakenhll_species.medium.csv')
KRAKENHLL_REFSEQ_STRICT = join(TAXA_DIR, 'refseq.krakenhll_species.strict.csv')
KRAKENHLL_REFSEQ_LONG = join(TAXA_DIR, 'refseq.krakenhll_longform.csv.gz')
