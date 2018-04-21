from .subfactory import SubFactory
from capalyzer.utils import readJSON
from pandas import DataFrame


class AlphaDiversityFactory(SubFactory):

    def get_generic(self, tool, metric, level='species'):
        adivfs = self.factory.get_results(module='alpha_diversity_stats',
                                          result='json')
        tbl = {}
        for sname, adivf in adivfs:
            adiv = readJSON(adivf)
            tbl[sname] = adiv[tool][level][metric]

        tbl = DataFrame(tbl).transpose()
        return tbl

    def chao1(self, tool='kraken', level='species'):
        return self.get_generic(tool, 'chao1', level=level)

    def shannon(self, tool='kraken', level='species'):
        return self.get_generic(tool, 'shannon_index', level=level)

    def richness(self, tool='kraken', level='species'):
        return self.get_generic(tool, 'richness', level=level)
