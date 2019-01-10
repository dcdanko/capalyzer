from .subfactory import SubFactory
import pandas as pd
from json import loads
from numpy import percentile


def jloads(fname):
    return loads(open(fname).read())

class MicrobeDirectoryFactory(SubFactory):

    def raw(self):
        mdfs = self.factory.get_results(module='microbe_directory_annotate',
                                         result='json')
        tbl = {sname: jloads(fname)
               for sname, fname in mdfs}
        return tbl

    def raw_table(self):
        tbl = []
        for sname, raw_vals in self.raw().items():
            for facet, facet_vals in raw_vals.items():
                for facet_val, val in facet_vals.items():
                    val = float(val)
                    tbl.append({
                        'sample_name': sname,
                        'category': facet,
                        'value': facet_val,
                        'proportion': val,
                    })
        tbl = {i: el for i, el in enumerate(tbl)}
        tbl = pd.DataFrame.from_dict(tbl, orient='index')
        return tbl

