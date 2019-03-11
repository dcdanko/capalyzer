"""Count the total number of species found at given kmer thresholds.

Uses the output of a longform krakenhll summary file as input.
"""

import click
import pandas as pd

def get_kmer_counts(myfile):
    tbl = {}
    for line in myfile:
        tkns = line.split(',')
        sp = tkns[1]
        k = int(tkns[7])
        if int(k) > tbl.get(sp, 0):
            tbl[sp] = int(k)
    ks = []
    for _, k in tbl.items():
        ks.append(k)

    counts = {}
    for thresh in range(2, 30):
        pthresh = 2 ** thresh
        for k in ks:
            if k >= pthresh:
                counts[thresh] = 1 + counts.get(thresh, 0)
    return counts


def get_kmer_counts_by_city(myfile):
    outer_tbl = {}
    for line in myfile:
        tkns = line.split(',')
        sample = tkns[0]
        sp = tkns[1]
        k = int(tkns[7])
        try:
            tbl = outer_tbl[sample]
        except KeyError:
            tbl = {}
            outer_tbl[sample] = tbl
        if int(k) > tbl.get(sp, 0):
            tbl[sp] = int(k)
    ks = {}
    for sname, tbl in outer_tbl.items():
        ks[sname] = []
        for _, k in tbl.items():
            ks[sname].append(k)

    counts = {}
    for sname, myks in ks.items():
        counts[sname] = {}
        for thresh in range(2, 30):
            pthresh = 2 ** thresh
            for k in myks:
                if k >= pthresh:
                    counts[sname][thresh] = 1 + counts[sname].get(thresh, 0)

    return counts




@click.command()
@click.option('-s/-a', '--by-sample/--all', default=False)
@click.argument('long_krakenhll', type=click.File('r'))
def main(by_sample, long_krakenhll):
    """Count the total number of species found at given kmer thresholds."""
    long_krakenhll.readline()
    if by_sample:
        counts = get_kmer_counts_by_city(long_krakenhll)
        tbl = pd.DataFrame.from_dict(counts, orient='index')
        click.echo(tbl.to_csv())
    else:
        counts = get_kmer_counts(long_krakenhll)
        for thresh, count in counts.items():
            print(f'2^{thresh}\t{count}')


if __name__ == '__main__':
    main()
