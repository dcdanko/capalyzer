import pandas as pd
from os.path import join

from scipy.spatial.distance import pdist, squareform
from .diversity_metrics import (
    shannon_entropy,
    richness,
    chao1,
    jensen_shannon_dist,
    rho_proportionality,
    rarefaction_analysis,
)
from .longform_parser import parse_longform_taxa
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
    KRAKENHLL_REFSEQ_MEDIUM,
    KRAKENHLL_REFSEQ_STRICT,
    KRAKENHLL_REFSEQ_LONG,
)


class DataTableFactory:

    def __init__(self, packet_dir, metadata_tbl=None):
        self.packet_dir = packet_dir
        self.metadata = None
        if metadata_tbl is not None:
            self.set_metadata(metadata_tbl)

    def set_metadata(self, metadata_tbl):
        """Set the internal metadata table which will be used to filter samples in tables."""
        if isinstance(metadata_tbl, str):
            try:
                metadata_tbl = pd.read_csv(metadata_tbl, index_col=0)
            except FileNotFoundError:
                metadata_tbl = self.csv_in_dir(
                    metadata_tbl, remove_zero_cols=False, remove_zero_rows=False
                )
        self.metadata = metadata_tbl

    def copy(self, new_metadata=None):
        """Return a deep copy, with a new metadata table. if specified"""
        if new_metadata is None:
            new_metadata = self.metadata
        return DataTableFactory(self.packet_dir, metadata_tbl=new_metadata)

    def csv_in_dir(self, fname, **kwargs):
        tbl = pd.read_csv(
            join(self.packet_dir, fname),
            header=0,
            index_col=0,
        )
        if self.metadata is not None and kwargs.get('metadata_filter', True):
            tbl = tbl.loc[set(self.metadata.index) & set(tbl.index)]
        if not kwargs.get('no_fill_na', False):
            tbl = tbl.fillna(kwargs.get('fillna', 0))
        if kwargs.get('remove_zero_cols', True):
            tbl = tbl.T.loc[tbl.sum(axis=0) > 0].T
        if kwargs.get('remove_zero_rows', True):
            tbl = tbl.loc[tbl.sum(axis=1) > 0]
        if kwargs.get('normalize', False):
            tbl = (tbl.T / tbl.T.sum()).T

        return tbl

    def taxonomy(self, **kwargs):
        """Return a taxonomy table."""
        tool = kwargs.get('tool', 'krakenhll').lower()
        if tool in ['metaphlan2']:
            return self.csv_in_dir(MPA_RELAB, **kwargs)

        if tool in ['krakenhll', 'krakenuniq']:
            strict = kwargs.get('strict', 'permissive')
            rank = kwargs.get('rank', 'species')
            if rank == 'species' and not isinstance(strict, int):
                fname = KRAKENHLL_REFSEQ
                if strict.lower() == 'strict':
                    fname = KRAKENHLL_REFSEQ_STRICT
                elif strict.lower() == 'medium':
                    fname = KRAKENHLL_REFSEQ_MEDIUM
                return self.csv_in_dir(fname, **kwargs)
            else:
                if isinstance(strict, str):
                    strict = {'strict': 512, 'medium': 256, 'permissive': 4}[strict]
                return parse_longform_taxa(join(
                    self.packet_dir, KRAKENHLL_REFSEQ_LONG),
                    strict=strict, rank=rank
                )

    def amrs(self, **kwargs):
        """Return an AMR table."""
        tool = kwargs.get('tool', 'megares').lower()
        unit = kwargs.get('unit', 'rpkm').lower()
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
            }[(unit, kind)], **kwargs)
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
        tbl = self.csv_in_dir(HMP_COMPARISON,
                              metadata_filter=False, remove_zero_rows=False, remove_zero_cols=False,
                              **kwargs)
        if self.metadata is not None:
            tbl = tbl.loc[tbl['sample_name'].isin(self.metadata.index)]
        return tbl

    def macrobes(self, **kwargs):
        """Return a table of macrobe abundances."""
        return self.csv_in_dir(MACROBES, **kwargs)

    def read_props(self, **kwargs):
        """Return a table of the proportion of reads assigned to macro categories."""
        return self.csv_in_dir(READ_PROPORTIONS, **kwargs)

    def taxa_alpha_diversity(self, **kwargs):
        """Return a Series of diversities."""
        taxa = self.taxonomy(**kwargs)
        print(taxa)
        return self.alpha_diversity(taxa, **kwargs)

    def amr_alpha_diversity(self, **kwargs):
        """Return a Series of diversities."""
        amr = self.amrs(**kwargs)
        return self.alpha_diversity(amr, **kwargs)

    def alpha_diversity(self, tbl, **kwargs):
        """Return generic alpha diversity table."""
        metric = kwargs.get('metric', 'shannon_entropy').lower()
        rarefy = kwargs.get('rarefy', 0)
        if metric == 'shannon_entropy':
            return tbl.apply(shannon_entropy, rarefy=rarefy, axis=1)
        elif metric == 'richness':
            return tbl.apply(richness, rarefy=rarefy, axis=1)
        elif metric == 'chao1':
            return tbl.apply(chao1, rarefy=rarefy, axis=1)

    def taxa_beta_diversity(self, **kwargs):
        """Return a distance matrix between taxa."""
        taxa = self.taxonomy(**kwargs)
        return self.beta_diversity(taxa, **kwargs)

    def amr_beta_diversity(self, **kwargs):
        """Return a distance matrix between taxa."""
        amr = self.amrs(**kwargs)
        return self.beta_diversity(amr, **kwargs)

    def beta_diversity(self, tbl, **kwargs):
        """Return generic beta diversity table."""
        metric = kwargs.get('metric', 'jsd').lower()
        if metric == 'jsd':
            metric = jensen_shannon_dist
        elif metric == 'rho':
            metric = rho_proportionality
        distm = squareform(pdist(tbl, metric))
        distm = pd.DataFrame(distm, index=tbl.index, columns=tbl.index)
        return distm

    def taxa_rarefaction(self, **kwargs):
        """Return a rarefaction analysis of taxa."""
        taxa = self.taxonomy(**kwargs)
        return self.rarefaction(taxa, **kwargs)

    def amr_rarefaction(self, **kwargs):
        """Return a rarefaction analysis of taxa."""
        amr = self.amrs(**kwargs)
        return self.rarefaction(amr, **kwargs)

    def rarefaction(self, tbl, **kwargs):
        ns = kwargs.get('ns', [])
        nsample = kwargs.get('nsample', 16)
        include_all = kwargs.get('include_all', True)
        return rarefaction_analysis(tbl, ns=ns, nsample=nsample, include_all=include_all)
