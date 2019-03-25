
from os import makedirs
from os.path import isfile, getsize, dirname, join
from .summary_table_factory import SummaryTableFactory

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


def write_csv(df_func, fname, overwrite=False, **kwargs):
    """Build a dataframe and write a csv."""
    makedirs(dirname(fname), exist_ok=True)
    if (isfile(fname) and getsize(fname) > 0) and not overwrite:
        raise FileExistsError(f'{fname} exists, set overwrite to True to overwrite.')
    df = df_func(**kwargs)
    if '.gz' in fname:
        df.to_csv(fname, compression='gzip')
    else:
        df.to_csv(fname)
    return fname


def make_all_tables(dirname, tables, overwrite=False):
    """Make a bunch of tables."""
    makedirs(tables, exist_ok=True)
    dff = SummaryTableFactory(dirname)

    def my_write_csv(df_func, fname, **kwargs):
        return write_csv(df_func, join(tables, fname), overwrite=overwrite, **kwargs)

    yield my_write_csv(dff.taxonomy.krakenhll, KRAKENHLL_REFSEQ)
    yield my_write_csv(dff.taxonomy.krakenhll, KRAKENHLL_REFSEQ_STRICT, level='strict')
    yield my_write_csv(dff.taxonomy.krakenhll, KRAKENHLL_REFSEQ_MEDIUM, level='medium')
    yield my_write_csv(dff.taxonomy.krakenhll_long, KRAKENHLL_REFSEQ_LONG)
    yield my_write_csv(dff.taxonomy.metaphlan2, MPA_RELAB)

    yield my_write_csv(dff.amr.mech, MEGARES_MECH_RPKM)
    yield my_write_csv(dff.amr.gene, MEGARES_GENE_RPKM)
    yield my_write_csv(dff.amr.classus, MEGARES_CLASS_RPKM)
    yield my_write_csv(dff.amr.group, MEGARES_GROUP_RPKM)

    yield my_write_csv(dff.amr.mech, MEGARES_MECH_RPKMG, rpkmg=True)
    yield my_write_csv(dff.amr.gene, MEGARES_GENE_RPKMG, rpkmg=True)
    yield my_write_csv(dff.amr.classus, MEGARES_CLASS_RPKMG, rpkmg=True)
    yield my_write_csv(dff.amr.group, MEGARES_GROUP_RPKMG, rpkmg=True)

    yield my_write_csv(dff.amr.card_rpkm, CARD_RPKM)
    yield my_write_csv(dff.amr.card_rpkmg, CARD_RPKMG)

    yield my_write_csv(dff.macrobes.table, MACROBES)
    yield my_write_csv(dff.ags.tbl, AVE_GENOME_SIZE)
    yield my_write_csv(dff.hmp.raw_table, HMP_COMPARISON)
    yield my_write_csv(dff.readprops.table, READ_PROPORTIONS)

    yield my_write_csv(dff.pathways.pathways, UNIREF90_RELAB)
    yield my_write_csv(dff.pathways.pathways, UNIREF90_COV, coverage=True)
