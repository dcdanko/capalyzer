from .subfactory import SubFactory
from pandas import DataFrame
from json import loads
from numpy import percentile


def jloads(fname):
    return loads(open(fname).read())


class MacrobeFactory(SubFactory):

    def table(self):
        macrobefs = self.factory.get_results(
            module='quantify_macrobial',
            result='tbl'
        )
        tbl = DataFrame.from_dict({
            sname: {
                taxa: vals['rpkm'] for taxa, vals in jloads(fname).items()
            } for sname, fname in macrobefs
        }, orient='index')
        return tbl
