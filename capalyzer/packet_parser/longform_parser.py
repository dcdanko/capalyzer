import pandas as pd
import gzip
import csv


def parse_longform_taxa(filename, rank='all', strict=512, min_reads=0, min_cov=0, max_read_slope=0,
                        exclude_ranks=['assembly', 'sequence']):
    """Return a pandas dataframe."""
    tbl = {}
    with gzip.open(filename, 'r') as longform:
        longform.readline()
        for line in longform:
            tkns = list(csv.reader([line.decode('utf-8')]))[0]
            sample_name, taxa_name, taxa_rank = tkns[0], tkns[1], tkns[3]
            try:
                nkmers, nreads, cov = int(tkns[6]), int(tkns[5]), tkns[8]
                try:
                    cov = float(cov)
                except ValueError:
                    cov = 0
                read_slope = nreads / nkmers
            except ValueError:
                print(line)
                raise
            if rank and rank != 'all' and rank != taxa_rank:
                continue
            if strict and nkmers < strict:
                continue
            if min_cov and cov < min_cov:
                continue
            if min_reads and nreads < min_reads:
                continue
            if max_read_slope and read_slope > max_read_slope:
                if cov < 0.9:
                    continue
            if taxa_rank in exclude_ranks:
                continue
            sample_tbl = tbl.get(sample_name, {})
            sample_tbl[taxa_name] = nreads
            tbl[sample_name] = sample_tbl
    return pd.DataFrame.from_dict(tbl, orient='index').fillna(0)
