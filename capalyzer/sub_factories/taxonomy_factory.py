from .subfactory import SubFactory
from capalyzer.utils import parse_key_val_file
from pandas import DataFrame
from .constants import (
    BRACKEN,
    KRAKEN,
    KRAKENHLL,
    METAPHLAN2,
)

def get_top_n(vec, n):
    if n <= 0:
        return vec
    tups = vec.items()
    tups = sorted(tups, key=lambda x: -x[1])
    out = {k: v for k, v in tups[:n]}
    return out


def is_rank(key, rank):
    rank_map = {
        'species': ('s', 't'),
        'genus': ('g', 's'),
        'phylum': ('p', 'c'),
        'kingdom': ('k', 'p')
    }
    try:
        rank, next_rank = rank_map[rank]
        rank = rank + '__'
        next_rank = next_rank + '__'
        return (rank in key) and (next_rank not in key)
    except KeyError:
        assert False, f'Rank {rank} not supported.'


def clean_taxa(taxa):
    return taxa.split('|')[-1]


class TaxonomyFactory(SubFactory):

    def generic(self, mod_name, top_n=0, cutoff=0, rank='species'):
        taxafs = self.factory.get_results(module=mod_name,
                                          result='report')

        def parse(fname):
            vec = {}
            tot = 0
            for k, v in parse_key_val_file(fname, kind=int).items():
                if is_rank(k, rank):
                    tot += v
                    vec[clean_taxa(k)] = v
            vec = {k: v / tot
                   for k, v in vec.items()
                   if (v / tot) >= cutoff}
            return get_top_n(vec, top_n)

        tbl = {sname: parse(fname)
               for sname, fname in taxafs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def kraken(self, top_n=0, cutoff=0, rank='species'):
        return self.generic(
            KRAKEN,
            top_n=top_n,
            cutoff=cutoff,
            rank=rank
        )

    def krakenhll(self, top_n=0, cutoff=0, rank='species'):
        return self.generic(
            KRAKENHLL,
            top_n=top_n,
            cutoff=cutoff,
            rank=rank
        )

    def metaphlan2(self, top_n=0, cutoff=0, rank='species'):
        return self.generic(
            METAPHLAN2,
            top_n=top_n,
            cutoff=cutoff,
            rank=rank
        )

    def bracken(self, rank='species'):
        assert rank in ['species', 'genus', 'phylum'], f'Rank {rank} not supported.'
        result = rank + '_report'
        taxafs = self.factory.get_results(module=BRACKEN, result=result)

        def parse(fname):
            return parse_key_val_file(fname, skip=1, val_column=6)

        tbl = {sname: parse(fname)
               for sname, fname in taxafs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl
