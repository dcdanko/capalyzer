from .subfactory import SubFactory
from metasub_cap_downstream.utils import parse_key_val_file
from pandas import DataFrame


def get_top_n(vec, n):
    if n <= 0:
        return vec
    tups = vec.items()
    tups = sorted(tups, key=lambda x: -x[1])
    out = {k: v for k, v in tups[:n]}
    return out


def is_species(key):
    return ('s__' in key) and ('t__' not in key)


def clean_taxa(taxa):
    return taxa.split('|')[-1]


class TaxonomyFactory(SubFactory):
    kraken_mod = 'kraken_taxonomy_profiling'

    def kraken(self, top_n=0):
        taxafs = self.factory.get_results(module=self.kraken_mod,
                                          result='mpa')
        def parse(fname):
            vec = {}
            tot = 0
            for k, v in parse_key_val_file(fname, kind=int).items():
                if is_species(k):
                    tot += v
                    vec[clean_taxa(k)] = v
            vec = {k: v / tot for k, v in vec.items()}
            return get_top_n(vec, top_n)

        tbl = {sname: parse(fname)
               for sname, fname in taxafs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl
