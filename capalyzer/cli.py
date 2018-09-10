import click

from os import mkdir
from os.path import join, isfile
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
def taxonomy(dirname):
    dff = DataTableFactory(dirname)
    stdout.write(dff.taxonomy.kraken().to_csv())


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
    mkdir(tables)

    dff = DataTableFactory(dirname)

    def my_write_csv(dffunc, args, fname, **kwargs):
        try:
            df = dffunc(*args, **kwargs)
            write_csv(df, fname, tables, overwrite=overwrite)
        except Exception as exc:
            print(f'Function {dffunc} failed with args {args}\n{exc}', file=stderr)

    print('Making taxonomy tables...')
    my_write_csv(dff.taxonomy.kraken, (), 'minikraken.kraken_species_top100.csv', top_n=100)
    my_write_csv(dff.taxonomy.kraken, (), 'minikraken.kraken_species_1percent_cutoff.csv', cutoff=0.01)
    my_write_csv(dff.taxonomy.krakenhll, (), 'refseq.krakenhll_species.csv')
    my_write_csv(dff.taxonomy.metaphlan2, (), 'metaphlan2_species.csv')
    my_write_csv(dff.taxonomy.bracken, (), 'minikraken.bracken_species.csv', rank='species')
    my_write_csv(dff.taxonomy.bracken, (), 'minikraken.bracken_genus.csv', rank='genus')
    my_write_csv(dff.taxonomy.bracken, (), 'minikraken.bracken_phylum.csv', rank='phylum')

    print('Making AMR tables...')
    my_write_csv(dff.amr.mech, (), 'megares_amr_mech.csv')
    my_write_csv(dff.amr.gene, (), 'megares_amr_gene.csv')
    my_write_csv(dff.amr.classus, (), 'megares_amr_class.csv')
    my_write_csv(dff.amr.group, (), 'megares_amr_group.csv')
    my_write_csv(dff.amr.card_rpkm, (), 'card_amr_rpkm.csv')
    my_write_csv(dff.amr.card_rpkmg, (), 'card_amr_rpkmg.csv')

    print('Making macrobe table...')
    my_write_csv(dff.macrobes.table, (), 'macrobe_abundances.csv')

    print('Making ags tables...')
    my_write_csv(dff.ags.tbl, (), 'ags.csv')

    print('Making alpha diversity tables...')
    my_write_csv(dff.alpha.shannon, (), 'alpha_diversity_shannon.csv')
    my_write_csv(dff.alpha.chao1, (), 'alpha_diversity_chao1.csv')
    my_write_csv(dff.alpha.richness, (), 'alpha_diversity_richness.csv')

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
    write_json(dff.hmp.raw(), tables + '/hmp_raw.json')
    write_json(dff.hmp.dists(), tables + '/hmp_dists.json')
