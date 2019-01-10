from .subfactory import SubFactory
from pandas import DataFrame
from .utils import parse_gene_table
from .constants import METHYLS


class MethylFactory(SubFactory):

    def generic(self, metric):
        genefs = self.factory.get_results(module=METHYLS,
                                          result='table')
        tbl = {sname: parse_gene_table(fname, metric)
               for sname, fname in genefs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def rpk(self):
        return self.generic('rpk')

    def rpkm(self):
        return self.generic('rpkm')

    def rpkmg(self):
        return self.generic('rpkmg')
