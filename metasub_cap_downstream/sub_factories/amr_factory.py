from metasub_cap_downstream.data_table_factory import SubFactory
from metasub_cap_downstream.utils import parse_key_val_file
from pandas import DataFrame


class AMRFactory(SubFactory):

    def generic(self, result):
        classfs = self.factory.get_results(module='resistome_amrs',
                                           result=result)
        tbl = {sname: parse_key_val_file(fname,
                                         key_column=1,
                                         val_column=2,
                                         kind=int)
               for sname, fname in classfs}
        tbl = DataFrame(tbl).fillna(0).transpose()
        return tbl

    def classus(self):
        return self.generic('classus')

    def mech(self):
        return self.generic('mech')
