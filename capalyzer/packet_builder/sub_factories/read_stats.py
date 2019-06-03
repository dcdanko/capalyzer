from .subfactory import SubFactory
from pandas import DataFrame
from json import loads


def jloads(fname):
    blob = loads(open(fname).read())
    return {
        'num_reads': blob['num_reads'],
        'gc_content': blob['gc_content'],
    }


class ReadStatsFactory(SubFactory):

    def table(self):
        readfs = self.factory.get_results(
            module='read_stats',
            result='json'
        )

        tbl = DataFrame.from_dict({
            sname: jloads(fname)
            for sname, fname in readfs
        }, orient='index')
        return tbl
