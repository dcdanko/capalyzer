from .subfactory import SubFactory
from pandas import DataFrame


def get_ags_from_file(fname):
    with open(fname) as f:
        for line in f:
            parts = line.strip().split()
            if (len(parts) > 0) and ('average_genome_size' in parts[0]):
                return float(parts[1])
    assert False and 'No Value Found in AGS (MicrobeCensus) Result'


class AGSFactory(SubFactory):

    def tbl(self):
        agsfs = self.factory.get_results(module='microbe_census',
                                         result='stats')
        tbl = {sname: get_ags_from_file(fname)
               for sname, fname in agsfs}
        tbl = DataFrame({'average_genome_size': tbl})
        return tbl
