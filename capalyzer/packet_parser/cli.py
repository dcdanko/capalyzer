import click

from .dataframes import DataTableFactory


@click.group('diversity')
def diversity():
    """Various commands to make diversity tables."""
    pass


@diversity.command('alpha')
@click.option('-k', '--kind', default='taxa', type=click.Choice(['taxa', 'amrs']),
              help='Diversity for taxa or AMRs')
@click.option('-m', '--metric', default='shannon_entropy',
              type=click.Choice(['shannon_entropy', 'richness', 'chao1']), help='Metric to be used')
@click.option('-r', '--rarefaction', default=0,
              help='Probabilistically rarefy samples to desired number of reads.')
@click.argument('packet_dir')
@click.argument('out_file', type=click.File('w'))
def alpha_diversity(kind, metric, rarefaction, packet_dir, out_file):
    """Write a table of alpha diversity to <out_file>."""
    tabler = DataTableFactory(packet_dir)
    if kind == 'taxa':
        tbl = tabler.taxa_alpha_diversity(metric=metric, rarefy=rarefaction)
    elif kind == 'amrs':
        tbl = tabler.amr_alpha_diversity(metric=metric, rarefy=rarefaction)
    tbl.to_csv(out_file)


@diversity.command('beta')
@click.option('-k', '--kind', default='taxa', type=click.Choice(['taxa', 'amrs']),
              help='Diversity for taxa or AMRs')
@click.option('-m', '--metric', default='shannon_entropy',
              type=click.Choice(['jsd', 'rho']), help='Metric to be used')
@click.argument('packet_dir')
@click.argument('out_file', type=click.File('w'))
def beta_diversity(kind, metric, packet_dir, out_file):
    """Write a table of alpha diversity to <out_file>."""
    tabler = DataTableFactory(packet_dir)
    if kind == 'taxa':
        tbl = tabler.taxa_beta_diversity(metric=metric)
    elif kind == 'amrs':
        tbl = tabler.amr_beta_diversity(metric=metric)
    tbl.to_csv(out_file)
