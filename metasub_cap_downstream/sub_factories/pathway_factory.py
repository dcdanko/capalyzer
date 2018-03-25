from metasub_cap_downstream.data_table_factory import SubFactory
from metasub_cap_downstream.utils import parse_key_val_file
from pandas import DataFrame


class PathwayFactory(SubFactory):
    humann2 = 'humann2_functional_profiling'

    def pathways(self, show_unmapped=False):
        pathfs = self.factory.get_results(module=self.humann2,
                                          result='path_abunds')

        def filter_keys(key):
            if show_unmapped:
                return True
            blacklist = ['UNMAPPED', 'UNINTEGRATED']
            for black in blacklist:
                if black in key:
                    return False
            return True

        def parse(fname):
            return {k: v
                    for k, v in parse_key_val_file(fname)
                    if filter_keys(k)}

        tbl = {sname: parse(fname)
               for sname, fname in pathfs}

        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl
