import click
from sys import stdout
from .data_table_factory import DataTableFactory


@click.group()
def main():
    pass


@main.group()
@click.argument('dirname')
def parse(dirname):
    pass


@parse.command()
@click.option('--topn', type=int, default=10)
def kraken(topn):
    fact = DataTableFactory(dirname)
    tbl = fact.taxonomy.kraken(top_n=topn)
    stdout.write(tbl.to_csv())
