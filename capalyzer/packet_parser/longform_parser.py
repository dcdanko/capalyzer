import pandas as pd
import gzip
import csv


def parse_longform_taxa(filename, rank='all', strict=512, exclude_ranks=['assembly', 'sequence']):
    """Return a pandas dataframe."""
    tbl = {}
    with gzip.open(filename, 'r') as longform:
        longform.readline()
        for line in longform:
            tkns = list(csv.reader([line.decode('utf-8')]))[0]
            sample_name, taxa_name, taxa_rank = tkns[0], tkns[1], tkns[3]
            try:
                nkmers, nreads = int(tkns[7]), int(tkns[9])
            except ValueError:
                print(line)
                raise
            if rank and rank != 'all' and rank != taxa_rank:
                continue
            if strict and nkmers < strict:
                continue
            if taxa_rank in exclude_ranks:
                continue
            sample_tbl = tbl.get(sample_name, {})
            sample_tbl[taxa_name] = nreads
            tbl[sample_name] = sample_tbl
    return pd.DataFrame.from_dict(tbl, orient='index').fillna(0)
