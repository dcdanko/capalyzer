import click

from os import mkdir
from sys import stdout
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
    stdout.write(dff.macrobes.tables().to_csv())


@main.command()
@click.argument('dirname')
def taxonomy(dirname):
    dff = DataTableFactory(dirname)
    stdout.write(dff.taxonomy.kraken().to_csv())


@main.command()
@click.argument('dirname')
@click.argument('tables')
def tables(dirname, tables):
    mkdir(tables)

    dff = DataTableFactory(dirname)

    print('Making taxonomy tables...')
    dff.taxonomy.kraken(top_n=100).to_csv(tables + '/kraken_species_top100.csv')
    dff.taxonomy.kraken(top_n=0, cutoff=0.01).to_csv(tables + '/kraken_species_1perc_cutoff.tsv')

    print('Making AMR tables...')
    dff.amr.mech().to_csv(tables + '/amr_mech.csv')
    dff.amr.gene().to_csv(tables + '/amr_gene.csv')
    dff.amr.classus().to_csv(tables + '/amr_class.csv')
    dff.amr.group().to_csv(tables + '/amr_group.csv')

    print('Making ags tables...')
    dff.ags.tbl().to_csv(tables + '/ags.csv')

    print('Making alpha diversity tables...')
    dff.alpha.shannon()['100000'].to_csv(tables + '/alpha_diversity_shannon.csv')
    dff.alpha.chao1()['100000'].to_csv(tables + '/alpha_diversity_chao1.csv')
    dff.alpha.richness()['100000'].to_csv(tables + '/alpha_diversity_richness.csv')

    print('Making pathway tables...')
    dff.pathways.pathways().to_csv(tables + '/pathways.csv')

    print('Making virulence tables...')
    dff.vir.rpkm().to_csv(tables + '/virulence_factors_rpkm.csv')
    dff.vir.rpkmg().to_csv(tables + '/virulence_factors_rpkmg.csv')

    print('Making methyltransferase tables...')
    dff.methyls.rpkm().to_csv(tables + '/methyltransferases_rpkm.csv')
    dff.methyls.rpkmg().to_csv(tables + '/methyltransferases_rpkmg.csv')

    print('Making HMP tables...')
    write_json(dff.hmp.raw(), tables + '/hmp_raw.json')
    write_json(dff.hmp.dists(), tables + '/hmp_dists.json')
