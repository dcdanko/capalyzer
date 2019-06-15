import click

from .summary_table_factory import SummaryTableFactory
from .api import make_all_tables


@click.command('read-stats')
@click.argument('dirname')
@click.argument('outname')
def cli_make_read_stats(dirname, outname):
    dff = SummaryTableFactory(dirname)
    dff.readstats.table().to_csv(outname)


@click.command('long-taxa')
@click.argument('dirname')
@click.argument('outname', type=click.File('w'))
def long_taxa(dirname, outname):
    """Make a bunch of tables."""
    dff = SummaryTableFactory(dirname)
    dff.taxonomy.krakenhll_long().to_csv(outname)


@click.command('make-tables')
@click.option('--overwrite/--no-overwrite', default=False)
@click.argument('dirname')
@click.argument('tables')
def all_tables(overwrite, dirname, tables):
    """Make a bunch of tables."""
    filenames = make_all_tables(dirname, tables, overwrite=overwrite)
    for filename in filenames:
        click.echo(filename, err=True)
