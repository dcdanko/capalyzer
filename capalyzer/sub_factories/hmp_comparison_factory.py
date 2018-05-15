from .subfactory import SubFactory
from pandas import DataFrame
from json import loads
from numpy import percentile


def jloads(fname):
    return loads(open(fname).read())


def as_dist(raw_vals):
    vals = {
        site: percentile(measures, [0, 25, 50, 75, 100])
        for site, measures in raw_vals.items()
    }
    return vals


class HMPFactory(SubFactory):

    def raw(self):
        hmpfs = self.factory.get_results(module='hmp_site_dists',
                                         result='metaphlan2')
        tbl = {sname: jloads(fname)
               for sname, fname in hmpfs}
        return tbl

    def dists(self):
        tbl = {sname: as_dist(raw_vals)
               for sname, raw_vals in self.raw().items()}
        return tbl
