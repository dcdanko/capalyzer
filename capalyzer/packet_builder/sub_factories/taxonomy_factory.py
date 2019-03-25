from .subfactory import SubFactory
from ..utils import parse_key_val_file
from pandas import DataFrame
from .constants import (
    BRACKEN,
    KRAKEN,
    KRAKENHLL,
    METAPHLAN2,
)
from .toxonomy_long_form import longform_taxa


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
        final_key = key.split('|')[-1]
        rank, next_rank = rank_map[rank]
        rank = rank + '__'
        next_rank = next_rank + '__'
        return (rank in final_key) and (next_rank not in final_key)
    except KeyError:
        assert False, f'Rank {rank} not supported.'


def is_top_taxa(key, top_taxa):
    assert top_taxa in ['all', 'bacteria', 'virus', 'eukaryote', 'fungi']
    tkns = [tkn.lower() for tkn in key.split('|')]
    if top_taxa == 'all':
        return True
    elif top_taxa == 'bacteria' and 'bacteria' in tkns[0]:
        return True
    elif top_taxa == 'virus' and ('virus' in key.lower() or 'viridae' in key.lower()):
        return True
    elif top_taxa == 'fungi' and 'fungi' in key.lower():
        return True
    elif top_taxa == 'eukaryote' and 'eukaryote' in tkns[0]:
        return True
    return False


def clean_taxa(taxa):
    return taxa.split('|')[-1].split('__')[-1]


class TaxonomyFactory(SubFactory):

    def generic(
            self, mod_name,
            top_n=0, cutoff=0, rank='species', top_taxa='all', proportions=False, rname='mpa'
    ):
        taxafs = self.factory.get_results(module=mod_name,
                                          result=rname)
        taxafs = list(taxafs)

        def parse(fname):
            vec = {}
            tot = 0
            for k, v in parse_key_val_file(fname, kind=float).items():
                if is_rank(k, rank) and is_top_taxa(k, top_taxa):
                    tot += v
                    vec[clean_taxa(k)] = v
            if proportions:
                vec = {
                    k: v / tot
                    for k, v in vec.items()
                    if (v / tot) >= cutoff
                }
            return get_top_n(vec, top_n)

        tbl = {sname: parse(fname)
               for sname, fname in taxafs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def kraken(self, top_n=0, cutoff=0, rank='species', top_taxa='all', proportions=False, level=None):
        return self.generic(
            KRAKEN,
            top_n=top_n,
            cutoff=cutoff,
            rank=rank,
            top_taxa=top_taxa,
            proportions=proportions,
        )

    def krakenhll(self, top_n=0, cutoff=0, rank='species', top_taxa='all', proportions=False, level=None):
        rname = 'report'
        if level:
            if 'm' in level:
                rname = 'report_medium'
            elif 's' in level:
                rname = 'report_strict'

        return self.generic(
            KRAKENHLL,
            top_n=top_n,
            cutoff=cutoff,
            rank=rank,
            top_taxa=top_taxa,
            proportions=proportions,
            rname=rname,
        )

    def krakenhll_long(self):
        taxafs = self.factory.get_results(module=KRAKENHLL, result='read_assignments')
        return longform_taxa(taxafs)

    def metaphlan2(self, top_n=0, cutoff=0, rank='species', top_taxa='all', proportions=True, level=None):
        return self.generic(
            METAPHLAN2,
            top_n=top_n,
            cutoff=cutoff,
            rank=rank,
            top_taxa=top_taxa,
            proportions=proportions,
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
