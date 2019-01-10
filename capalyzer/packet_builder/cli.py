import click

from .api import make_all_tables


@click.command('make-tables')
@click.option('--overwrite/--no-overwrite', default=False)
@click.argument('dirname')
@click.argument('tables')
def all_tables(overwrite, dirname, tables):
    """Make a bunch of tables."""
    filenames = make_all_tables(dirname, tables, overwrite=overwrite)
    for filename in filenames:
        click.echo(filename, err=True)
