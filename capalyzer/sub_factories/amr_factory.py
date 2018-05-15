from .subfactory import SubFactory
from capalyzer.utils import parse_key_val_file
from pandas import DataFrame
from .utils import parse_gene_table


class AMRFactory(SubFactory):

    def generic_megares(self, result):
        classfs = self.factory.get_results(module='resistome_amrs',
                                           result=result)
        tbl = {sname: parse_key_val_file(fname,
                                         key_column=1,
                                         val_column=2,
                                         kind=int,
                                         skip=1)
               for sname, fname in classfs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def gene(self):
        return self.generic_megares('gene')

    def group(self):
        return self.generic_megares('group')

    def classus(self):
        return self.generic_megares('classus')

    def mech(self):
        return self.generic_megares('mech')

    def generic_card(self, metric):
        genefs = self.factory.get_results(module='align_to_amr_genes',
                                          result='table')
        tbl = {sname: parse_gene_table(fname, metric)
               for sname, fname in genefs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def card_rpkm(self):
        return self.generic_card('RPKM')

    def card_rpkmg(self):
        return self.generic_card('RPKMG')
