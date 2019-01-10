from .subfactory import SubFactory
from ..utils import parse_key_val_file
from pandas import DataFrame
from .utils import parse_gene_table


class AMRFactory(SubFactory):

    def generic_megares(self, result, rpkmg=False):
        classfs = self.factory.get_results(module='resistome_amrs',
                                           result=result + '_normalized')
        classfs = [el for el in classfs]
        val_col = 2
        if rpkmg:
            val_col = 3
        tbl = {sname: parse_key_val_file(fname,
                                         key_column=0,
                                         val_column=val_col,
                                         sep=',',
                                         kind=float,
                                         skip=1)
               for sname, fname in classfs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def gene(self, rpkmg=False):
        return self.generic_megares('gene', rpkmg=rpkmg)

    def group(self, rpkmg=False):
        return self.generic_megares('group', rpkmg=rpkmg)

    def classus(self, rpkmg=False):
        return self.generic_megares('classus', rpkmg=rpkmg)

    def mech(self, rpkmg=False):
        return self.generic_megares('mech', rpkmg=rpkmg)

    def generic_card(self, metric):
        genefs = self.factory.get_results(module='align_to_amr_genes',
                                          result='table')
        tbl = {sname: parse_gene_table(fname, metric)
               for sname, fname in genefs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def card_rpkm(self):
        return self.generic_card('rpkm')

    def card_rpkmg(self):
        return self.generic_card('rpkmg')
