from metasub_cap_downstream.data_table_factory import SubFactory
from pandas import DataFrame
from json import loads
from numpy import percentile


def jloads(fname):
    return loads(open(fname).read())


def as_dist(raw_vals):
    vals = percentile(raw_vals, [0, 25, 50, 75, 100])
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
               for sname, raw_vals in self.raw.items()}
        tbl = DataFrame(tbl).transpose()
        return tbl
