from .subfactory import SubFactory
from pandas import DataFrame
from .utils import parse_gene_table
from .constants import VFDB


class VirulenceFactory(SubFactory):

    def generic(self, metric):
        genefs = self.factory.get_results(module=VFDB,
                                          result='table')
        tbl = {sname: parse_gene_table(fname, metric)
               for sname, fname in genefs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def rpk(self):
        return self.generic('RPK')

    def rpkm(self):
        return self.generic('RPKM')

    def rpkmg(self):
        return self.generic('RPKMG')
