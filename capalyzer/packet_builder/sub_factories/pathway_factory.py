from .subfactory import SubFactory
from ..utils import parse_key_val_file
from pandas import DataFrame


class PathwayFactory(SubFactory):

    def pathways(self, coverage=False, show_unmapped=False):
        """Return a table of pathway abundances or coverages."""
        def check_key(key):
            """Return True if a key is not blacklisted."""
            out = True
            for black in [] if show_unmapped else ['UNMAPPED', 'UNINTEGRATED']:
                out &= black not in key
            return out

        result = 'path_cov' if coverage else 'relab_path_abunds'
        path_fs = self.factory.get_results(module='humann2_functional_profiling', result=result)
        tbl = {
            sname: {
                k: v for k, v in parse_key_val_file(fname).items() if check_key(k)
            } for sname, fname in path_fs
        }
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl
