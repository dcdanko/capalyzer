import click
from sys import stdout
from .data_table_factory import DataTableFactory

@click.group()
def main():
    pass


@main.command()
@click.option('--topn', type=int, default=10)
@click.argument('dirname')
def dump_kraken(topn, dirname):
    fact = DataTableFactory(dirname)
    tbl = fact.taxonomy.kraken(top_n=topn)
    stdout.write(tbl.to_csv())
