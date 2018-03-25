from metasub_cap_downstream.data_table_factory import SubFactory
from pandas import DataFrame


def parse_gene_table(gene_table, metric):
    '''Return a parsed gene quantification table.'''
    with open(gene_table) as gt:
        gene_names = gt.readline().strip().split(',')[1:]
        rpks = gt.readline().strip().split(',')[1:]
        rpkms = gt.readline().strip().split(',')[1:]
        rpkmgs = gt.readline().strip().split(',')[1:]

    data = {}
    for i, gene_name in enumerate(gene_names):
        row = {
            'RPK': rpks[i],
            'RPKM': rpkms[i],
            'RPKMG': rpkmgs[i],
        }
        data[gene_name] = row[metric]
    return data


class MethylFactory(SubFactory):

    def generic(self, metric):
        genefs = self.factory.get_results(module='align_to_methyltransferases',
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
