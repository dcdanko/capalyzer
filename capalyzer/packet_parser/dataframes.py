import pandas as pd
from os.path import join

from scipy.spatial.distance import pdist, squareform
from .diversity_metrics import (
    shannon_entropy,
    richness,
    jensen_shannon_dist,
    rho_proportionality
)
from ..constants import (
    CARD_RPKM,
    CARD_RPKMG,
    MEGARES_CLASS_RPKM,
    MEGARES_CLASS_RPKMG,
    MEGARES_GENE_RPKM,
    MEGARES_GENE_RPKMG,
    MEGARES_GROUP_RPKM,
    MEGARES_GROUP_RPKMG,
    MEGARES_MECH_RPKM,
    MEGARES_MECH_RPKMG,
    AVE_GENOME_SIZE,
    HMP_COMPARISON,
    MACROBES,
    READ_PROPORTIONS,
    UNIREF90_COV,
    UNIREF90_RELAB,
    MPA_RELAB,
    KRAKENHLL_REFSEQ,
)


class DataTableFactory:

    def __init__(self, packet_dir):
        self.packet_dir = packet_dir

    def csv_in_dir(self, fname, **kwargs):
        tbl = pd.read_csv(
            join(self.packet_dir, fname),
            header=0,
            index_col=0,
        )
        if kwargs.get('fillna', None) is not None:
            tbl = tbl.fillna(kwargs['fillna'])
        if kwargs.get('normalize', False):
            tbl = (tbl.T / tbl.T.sum()).T
        return tbl

    def taxonomy(self, **kwargs):
        """Return a taxonomy table."""
        tool = kwargs.get('tool', 'krakenhll').lower()
        if tool in ['krakenhll', 'krakenuniq']:
            return self.csv_in_dir(KRAKENHLL_REFSEQ, **kwargs)
        elif tool in ['metaphlan2']:
            return self.csv_in_dir(MPA_RELAB, **kwargs)

    def amrs(self, **kwargs):
        """Return an AMR table."""
        tool = kwargs.get('tool', 'megares').lower()
        metric = kwargs.get('metric', 'rpkm').lower()
        if tool in ['megares']:
            kind = kwargs.get('kind', 'class').lower()
            return self.csv_in_dir({
                ('rpkm', 'class'): MEGARES_CLASS_RPKM,
                ('rpkm', 'gene'): MEGARES_GENE_RPKM,
                ('rpkm', 'group'): MEGARES_GROUP_RPKM,
                ('rpkm', 'mech'): MEGARES_MECH_RPKM,
                ('rpkmg', 'class'): MEGARES_CLASS_RPKMG,
                ('rpkmg', 'gene'): MEGARES_GENE_RPKMG,
                ('rpkmg', 'group'): MEGARES_GROUP_RPKMG,
                ('rpkmg', 'mech'): MEGARES_MECH_RPKMG,
            }[(metric, kind)], **kwargs)
        elif tool in ['card']:
            return self.csv_in_dir({
                'rpkm': CARD_RPKM,
                'rpkmg': CARD_RPKMG,
            }[tool], **kwargs)

    def pathways(self, **kwargs):
        """Return a table of pathways."""
        kind = kwargs.get('kind', 'relab').lower()
        return self.csv_in_dir({
            'relab': UNIREF90_RELAB,
            'cov': UNIREF90_COV,
        }[kind], **kwargs)

    def ags(self, **kwargs):
        """Return a Series of Ave Genome Size estimates."""
        return self.csv_in_dir(AVE_GENOME_SIZE, **kwargs)

    def hmp(self, **kwargs):
        """Return a table of HMP distances."""
        return self.csv_in_dir(HMP_COMPARISON, **kwargs)

    def macrobes(self, **kwargs):
        """Return a table of macrobe abundances."""
        return self.csv_in_dir(MACROBES, **kwargs)

    def read_props(self, **kwargs):
        """Return a table of the proportion of reads assigned to macro categories."""
        return self.csv_in_dir(READ_PROPORTIONS, **kwargs)

    def taxa_alpha_diversity(self, **kwargs):
        """Return a Series of diversities."""
        taxa = self.taxonomy(**kwargs)
        return self.alpha_diversity(taxa, **kwargs)

    def alpha_diversity(self, tbl, **kwargs):
        """Return generic alpha diversity table."""
        metric = kwargs.get('metric', 'shannon_entropy').lower()
        if metric == 'shannon_entropy':
            return tbl.apply(shannon_entropy)
        elif metric == 'richness':
            return tbl.apply(richness)

    def taxa_beta_diversity(self, **kwargs):
        """Return a distance matrix between taxa."""
        taxa = self.taxonomy(**kwargs)
        return self.beta_diversity(taxa, **kwargs)

    def beta_diversity(self, tbl, **kwargs):
        """Return generic beta diversity table."""
        metric_name = kwargs.get('metric', 'jsd').lower()
        if metric_name == 'jsd':
            metric = jensen_shannon_dist
        elif metric_name == 'rho':
            metric = rho_proportionality
        distm = squareform(pdist(tbl, metric))
        distm = pd.DataFrame(distm, index=tbl.index, columns=tbl.index)
        return distm