
import pandas as pd
import click
from math import log10


@click.command()
@click.option('-k', '--min-kmers', default=64, type=int)
@click.option('-r', '--min-reads', default=3, type=int)
@click.option('-s', '--slope', default=(100 / 250), type=float)
@click.argument('longform_table', type=click.File('r'))
@click.argument('table_out', type=click.File('w'))
def main(min_kmers, min_reads, slope, longform_table, table_out):
    """Filter taxa according to the ratio of reads to kmers."""
    long_taxa = pd.read_csv(longform_table)
    long_taxa.columns = [
        'uuid', 'taxa', 'taxid', 'rank', 'mpa',
        'cov', 'dup', 'kmers', 'percent', 'reads', 'tax_reads'
    ]
    long_taxa = long_taxa.query('rank == "species"')
    long_taxa = long_taxa.query('reads >= @min_reads')
    long_taxa = long_taxa.query('kmers >= @min_kmers')
    
    def below_slope(row):
        my_slope = log10(row['reads']) / log10(row['kmers'])
        return my_slope <= slope

    rows_below = long_taxa.apply(lambda r: below_slope(r), axis=1)
    long_taxa = long_taxa.loc[rows_below]
    long_taxa = long_taxa[['uuid', 'taxa', 'reads']]
    wide_taxa = pd.pivot_table(long_taxa, values='reads', index=['uuid'], columns=['taxa'])
    wide_taxa.to_csv(table_out)


if __name__ == '__main__':
    main()
