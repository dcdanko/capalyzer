import click

from os import makedirs
from os.path import join, isfile, getsize
from sys import stdout, stderr
from .summary_table_factory import SummaryTableFactory
from json import dumps

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


def write_json(tbl, filename):
    with open(filename, 'w') as f:
        f.write(dumps(tbl))


@click.group()
def tables():
    pass


@tables.command()
@click.argument('dirname')
def macrobes(dirname):
    dff = SummaryTableFactory(dirname)
    stdout.write(dff.macrobes.table().to_csv())


@tables.command()
@click.argument('dirname')
def microbedir(dirname):
    dff = SummaryTableFactory(dirname)
    stdout.write(dff.microbe_directory.raw_table().to_csv())


@tables.command()
@click.argument('dirname')
def readprops(dirname):
    dff = SummaryTableFactory(dirname)
    stdout.write(dff.readprops.table().to_csv())


@tables.command()
@click.argument('prefix')
@click.argument('dirname')
def pathways(prefix, dirname):
    dff = SummaryTableFactory(dirname)

    def my_write_csv(dffunc, args, fname, **kwargs):
        fname = f'{prefix}{fname}'
        if isfile(fname) and getsize(fname) > 0:
            print(f'{fname} exists, skipping.', file=stderr)
            return
        print(f'building {fname}...', file=stderr)
        try:
            df = dffunc(*args, **kwargs)
            if '.gz' in fname:
                df.to_csv(fname, compression='gzip')
            else:
                df.to_csv(fname)
        except Exception as exc:
            print(f'Function {dffunc} failed with args {args}\n{exc}', file=stderr)

    my_write_csv(dff.pathways.pathways, (), 'pathways.csv')
    my_write_csv(dff.pathways.rpkm, (), 'functional_genes_rpkm.csv')


@tables.command()
@click.option('-n', '--topn', default=0)
@click.option('-m', '--min-cutoff', default=0)
@click.option('-r', '--rank',
              type=click.Choice(['species', 'genus', 'phylum']),
              default='species')
@click.option('-t', '--taxa',
              type=click.Choice(['all', 'bacteria', 'virus', 'eukaryote', 'fungi']),
              default='all')
@click.option('--proportions/--read-counts', default=True)
@click.option('-c', '--classifier',
              type=click.Choice(['metaphlan2', 'krakenhll']),
              default='krakenhll')
@click.option('-s', '--strictness',
              type=click.Choice(['permissive', 'medium', 'strict']),
              default='permissive',
              help='Choose permissiveness, only applies to krakenhll')
@click.argument('dirname')
def taxonomy(topn, min_cutoff, rank, taxa, proportions, classifier, strictness, dirname):
    dff = SummaryTableFactory(dirname)
    if classifier == 'metaphlan2':
        classifier = dff.taxonomy.metaphlan2
    elif classifier == 'krakenhll':
        classifier = dff.taxonomy.krakenhll
    tbl = classifier(
        top_n=topn,
        cutoff=min_cutoff,
        rank=rank,
        top_taxa=taxa,
        proportions=proportions,
        level=strictness,
    )
    stdout.write(tbl.to_csv())


def write_csv(df, filename, dirname, overwrite=False):
    fname = join(dirname, filename)
    if overwrite or not isfile(fname):
        df.to_csv(fname)


@tables.command()
@click.option('--overwrite/--no-overwrite', default=False)
@click.option('--pathways/--no-pathways', default=False)
@click.argument('dirname')
@click.argument('tables')
def all_tables(overwrite, pathways, dirname, tables):
    """Make a bunch of tables."""
    makedirs(tables, exist_ok=True)
    dff = SummaryTableFactory(dirname)

    def my_write_csv(dffunc, args, fname, **kwargs):
        fname = f'{tables}/{fname}'
        makedirs(dirname(fname), exist_ok=True)
        if (isfile(fname) and getsize(fname) > 0) and not overwrite:
            print(f'{fname} exists, skipping.', file=stderr)
            return
        print(f'building {fname}...', file=stderr)
        try:
            df = dffunc(*args, **kwargs)
            if '.gz' in fname:
                df.to_csv(fname, compression='gzip')
            else:
                df.to_csv(fname)
        except Exception as exc:
            print(f'Function {dffunc} failed with args {args}\n{exc}', file=stderr)

    print('Making taxonomy tables...')
    my_write_csv(dff.taxonomy.krakenhll, (), KRAKENHLL_REFSEQ)
    my_write_csv(dff.taxonomy.metaphlan2, (), MPA_RELAB)

    print('Making AMR tables...')
    my_write_csv(dff.amr.mech, (), MEGARES_MECH_RPKM)
    my_write_csv(dff.amr.gene, (), MEGARES_GENE_RPKM)
    my_write_csv(dff.amr.classus, (), MEGARES_CLASS_RPKM)
    my_write_csv(dff.amr.group, (), MEGARES_GROUP_RPKM)

    my_write_csv(dff.amr.mech, (), MEGARES_MECH_RPKMG, rpkmg=True)
    my_write_csv(dff.amr.gene, (), MEGARES_GENE_RPKMG, rpkmg=True)
    my_write_csv(dff.amr.classus, (), MEGARES_CLASS_RPKMG, rpkmg=True)
    my_write_csv(dff.amr.group, (), MEGARES_GROUP_RPKMG, rpkmg=True)

    my_write_csv(dff.amr.card_rpkm, (), CARD_RPKM)
    my_write_csv(dff.amr.card_rpkmg, (), CARD_RPKMG)

    print('Making small tables...')
    my_write_csv(dff.macrobes.table, (), MACROBES)
    my_write_csv(dff.ags.tbl, (), AVE_GENOME_SIZE)
    my_write_csv(dff.hmp.raw_table, (), HMP_COMPARISON)

    if pathways:
        print('Making pathway tables...')
        my_write_csv(dff.pathways.pathways, (), 'pathways.csv')
        my_write_csv(dff.pathways.rpkm, (), 'functional_genes_rpkm.csv')
        my_write_csv(dff.pathways.rpkmg, (), 'functional_genes_rpkmg.csv()')
