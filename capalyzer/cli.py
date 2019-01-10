import click

from os import makedirs
from os.path import join, isfile, getsize
from sys import stdout, stderr
from .data_table_factory import DataTableFactory
from json import dumps


def write_json(tbl, filename):
    with open(filename, 'w') as f:
        f.write(dumps(tbl))


@click.group()
def main():
    pass


@main.command()
@click.argument('dirname')
def macrobes(dirname):
    dff = DataTableFactory(dirname)
    stdout.write(dff.macrobes.table().to_csv())


@main.command()
@click.argument('dirname')
def microbedir(dirname):
    dff = DataTableFactory(dirname)
    stdout.write(dff.microbe_directory.raw_table().to_csv())


@main.command()
@click.argument('dirname')
def readprops(dirname):
    dff = DataTableFactory(dirname)
    stdout.write(dff.readprops.table().to_csv())


@main.command()
@click.argument('prefix')
@click.argument('dirname')
def pathways(prefix, dirname):

    dff = DataTableFactory(dirname)

    def my_write_csv(dffunc, args, fname, **kwargs):
        fname = f'{prefix}{fname}'
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

    my_write_csv(dff.pathways.pathways, (), 'pathways.csv')
    my_write_csv(dff.pathways.rpkm, (), 'functional_genes_rpkm.csv')


@main.command()
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
              type=click.Choice(['metaphlan2', 'kraken', 'krakenhll']),
              default='krakenhll')
@click.option('-s', '--strictness',
              type=click.Choice(['permissive', 'medium', 'strict']),
              default='permissive',
              help='Choose permissiveness, only applies to krakenhll')
@click.argument('dirname')
def taxonomy(topn, min_cutoff, rank, taxa, proportions, classifier, strictness, dirname):
    dff = DataTableFactory(dirname)
    if classifier == 'metaphlan2':
        classifier = dff.taxonomy.metaphlan2
    elif classifier == 'kraken':
        classifer = dff.taxonomy.kraken
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

        

@main.command()
@click.option('--overwrite/--no-overwrite', default=False)
@click.option('--pathways/--no-pathways', default=False)
@click.argument('dirname')
@click.argument('tables')
def tables(overwrite, pathways, dirname, tables):
    """Make a bunch of tables."""
    makedirs(tables, exist_ok=True)

    dff = DataTableFactory(dirname)

    def my_write_csv(dffunc, args, fname, **kwargs):
        fname = f'{tables}/{fname}'
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

    def my_write_json(tbl, filename):
        fname = f'{tables}/{filename}'
        if (isfile(fname) and getsize(fname) > 0)  and not overwrite:
            print(f'{fname} exists, skipping.', file=stderr)
            return
        print(f'building {fname}...', file=stderr)
        with open(fname, 'w') as f:
            f.write(dumps(tbl))

            
    print('Making taxonomy tables...')
    my_write_csv(dff.taxonomy.kraken, (), 'minikraken.kraken_species_top100.csv', top_n=100)
    my_write_csv(dff.taxonomy.kraken, (), 'minikraken.kraken_species_1percent_cutoff.csv', cutoff=0.01)
    my_write_csv(dff.taxonomy.krakenhll, (), 'refseq.krakenhll_species.csv', top_n=250)
    my_write_csv(dff.taxonomy.krakenhll, (), 'refseq.bacteria.krakenhll_species.read_counts.csv',
                 level='strict', top_taxa='bacteria', proportions=False)
    my_write_csv(dff.taxonomy.krakenhll, (), 'refseq.virus.krakenhll_species.read_counts.csv',
                 level='medium', top_taxa='virus', proportions=False)
    my_write_csv(dff.taxonomy.krakenhll, (), 'refseq.fungi.krakenhll_species.read_counts.csv',
                 level='strict', top_taxa='fungi', proportions=False)
    my_write_csv(dff.taxonomy.metaphlan2, (), 'metaphlan2_species.csv')
    my_write_csv(dff.taxonomy.bracken, (), 'minikraken.bracken_species.csv', rank='species')
    my_write_csv(dff.taxonomy.bracken, (), 'minikraken.bracken_genus.csv', rank='genus')
    my_write_csv(dff.taxonomy.bracken, (), 'minikraken.bracken_phylum.csv', rank='phylum')

    print('Making AMR tables...')
    my_write_csv(dff.amr.mech, (), 'megares_amr_mech_rpkm.csv')
    my_write_csv(dff.amr.gene, (), 'megares_amr_gene_rpkm.csv')
    my_write_csv(dff.amr.classus, (), 'megares_amr_class_rpkm.csv')
    my_write_csv(dff.amr.group, (), 'megares_amr_group_rpkm.csv')

    my_write_csv(dff.amr.mech, (), 'megares_amr_mech_rpkmg.csv', rpkmg=True)
    my_write_csv(dff.amr.gene, (), 'megares_amr_gene_rpkmg.csv', rpkmg=True)
    my_write_csv(dff.amr.classus, (), 'megares_amr_class_rpkmg.csv', rpkmg=True)
    my_write_csv(dff.amr.group, (), 'megares_amr_group_rpkmg.csv', rpkmg=True)

    my_write_csv(dff.amr.card_rpkm, (), 'card_amr_rpkm.csv')
    my_write_csv(dff.amr.card_rpkmg, (), 'card_amr_rpkmg.csv')

    print('Making macrobe table...')
    my_write_csv(dff.macrobes.table, (), 'macrobe_abundances.csv')

    print('Making ags tables...')
    my_write_csv(dff.ags.tbl, (), 'ags.csv')

    print('Making alpha diversity tables...')
    my_write_csv(dff.alpha.shannon, (), 'alpha_diversity_shannon_kraken.csv')
    my_write_csv(dff.alpha.chao1, (), 'alpha_diversity_chao1_kraken.csv')
    my_write_csv(dff.alpha.richness, (), 'alpha_diversity_richness_kraken.csv')
    my_write_csv(dff.alpha.shannon, (), 'alpha_diversity_shannon_mphlan2.csv', tool='metaphlan2')
    my_write_csv(dff.alpha.chao1, (), 'alpha_diversity_chao1_mphlan2.csv', tool='metaphlan2')
    my_write_csv(dff.alpha.richness, (), 'alpha_diversity_richness_mphlan2.csv', tool='metaphlan2')

    if pathways:
        print('Making pathway tables...')
        my_write_csv(dff.pathways.pathways, (), 'pathways.csv')
        my_write_csv(dff.pathways.rpkm, (), 'functional_genes_rpkm.csv')
        my_write_csv(dff.pathways.rpkmg, (), 'functional_genes_rpkmg.csv()')

    print('Making virulence tables...')
    my_write_csv(dff.vir.rpkm, (), 'virulence_factors_rpkm.csv')
    my_write_csv(dff.vir.rpkmg, (), 'virulence_factors_rpkmg.csv')

    print('Making methyltransferase tables...')
    my_write_csv(dff.methyls.rpkm, (), 'methyltransferases_rpkm.csv')
    my_write_csv(dff.methyls.rpkmg, (), 'methyltransferases_rpkmg.csv')

    print('Making HMP tables...')
    my_write_json(dff.hmp.raw(), 'hmp_raw.json')
    my_write_json(dff.hmp.dists(), 'hmp_dists.json')
    my_write_csv(dff.hmp.raw_table, (), 'hmp_raw.csv')
