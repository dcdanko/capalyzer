from .subfactory import SubFactory
from ..utils import parse_key_val_file
from pandas import DataFrame
from .constants import HUMANN2, HUMANN2_NORMALIZED


class PathwayFactory(SubFactory):

    def pathways(self, show_unmapped=False):
        pathfs = self.factory.get_results(module=HUMANN2,
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
                    for k, v in parse_key_val_file(fname).items()
                    if filter_keys(k)}

        tbl = {sname: parse(fname)
               for sname, fname in pathfs}

        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def rpkm(self):
        rpkmfs = self.factory.get_results(
            module=HUMANN2_NORMALIZED,
            result='read_depth_norm_genes'
        )
        tbl = {sname: parse_key_val_file(fname)
               for sname, fname in rpkmfs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def rpkmg(self):
        rpkmgfs = self.factory.get_results(
            module=HUMANN2_NORMALIZED,
            result='ags_norm_genes'
        )
        tbl = {sname: parse_key_val_file(fname)
               for sname, fname in rpkmgfs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

