from .subfactory import SubFactory
import pandas as pd
from json import loads
from numpy import percentile


def jloads(fname):
    return loads(open(fname).read())


def as_dist(raw_vals):
    vals = {
        site: list(percentile(measures, [0, 25, 50, 75, 100]))
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

    def raw_table(self):
        cols = {
            'sample_name': [],
            'body_site': [],
            'distance': [],
        }
        for sname, raw_vals in self.raw().items():
            for site, measurements in raw_vals.items():
                for measurement in measurements:
                    cols['sample_name'].append(sname)
                    cols['body_site'].append(site)
                    cols['distance'].append(measurement)
        tbl = pd.DataFrame.from_dict(cols, orient='columns')
        return tbl
