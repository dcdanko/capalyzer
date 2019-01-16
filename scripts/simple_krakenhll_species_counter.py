"""A deliberately simple script to count species in KrakenHLL Reports.

Used to gut check a fancier parser.

Written Jan 16, 2019
"""

import click



def process_one_file(k, a, filename):
    """Return a set of species over thresholds."""
    with open(filename) as f:
        f.readline()
        species = set()
        for line in f:
            tkns = [tkn.strip() for tkn in line.split('\t')]
            abund, _, _, kmers, _, _, _, rank, taxa_name = tkns
            if rank != 'species':
                continue
            if float(abund) >= a and int(kmers) >= k:
                species.add(taxa_name)
    return species



@click.command()
@click.option('-k', '--kmer', type=int)
@click.option('-a', '--min-abund', type=float)
@click.argument('filenames', nargs=-1)
def main(kmer, min_abund, filenames):
    """Count the number of species in the krakenhll reports."""
    all_species = set()
    for filename in filenames:
        all_species |= process_one_file(kmer, min_abund, filename)
    click.echo(f'{len(all_species)} species')


if __name__ == '__main__':
    main()
