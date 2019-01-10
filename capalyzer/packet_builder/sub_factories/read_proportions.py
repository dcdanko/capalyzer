from .subfactory import SubFactory
from pandas import DataFrame
from json import loads
from numpy import percentile


def jloads(fname):
    return loads(open(fname).read())


class ReadPropsFactory(SubFactory):

    def table(self):
        readfs = self.factory.get_results(
            module='read_classification_proportions',
            result='json'
        )

        tbl = DataFrame.from_dict({
            sname: jloads(fname)['proportions']
            for sname, fname in readfs
        }, orient='index')
        return tbl
