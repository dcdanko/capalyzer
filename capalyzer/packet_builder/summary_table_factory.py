
from os.path import abspath, isfile
from .sub_factories import *
from pandas import DataFrame
from glob import glob


class SummaryTableFactory:
    '''A class that creates useful data tables from the MetaSUB CAP'''

    def __init__(self, dirname, metadata_hooks=[]):
        self.parsed = []
        self.samples = set()
        self._parse_core_dir(dirname)

        self.metadata = {}
        self._run_metadata_hooks(metadata_hooks)

        self.amr = AMRFactory(self)
        self.ags = AGSFactory(self)
        self.hmp = HMPFactory(self)
        self.pathways = PathwayFactory(self)
        self.taxonomy = TaxonomyFactory(self)
        self.macrobes = MacrobeFactory(self)
        self.readprops = ReadPropsFactory(self)
        self.microbe_directory = MicrobeDirectoryFactory(self)

    def get_results(self, module=None, result=None):
        '''Return [(<sample-name>, <file-type>, <file-name>)] for rtype.'''
        for sample, recModule, recResult, fname in self.parsed:
            if (module is None) and (result is None):
                rec = (sample, recModule, recResult, fname)
            elif result is None and recModule == module:
                rec = (sample, recResult, fname)
            elif (recModule == module) and (recResult == result):
                rec = (sample, fname)
            else:
                rec = None
            if rec is not None:
                yield rec

    def get_metadata(self):
        return DataFrame(self.metadata).transpose()

    def _parse_core_dir(self, dirname):
        files = [f for f in glob(dirname + '/*/*') if isfile(f)]
        for fname in files:
            try:
                sample, module, result = self._parse_core_file(fname)
                fpath = abspath(fname)
                self.samples.add(sample)
                self.parsed.append((sample, module, result, fpath))
            except ValueError:
                pass

    def _parse_core_file(self, filename):
        basename = filename.split('/')[-1]
        tkns = basename.split('.')
        try:
            sample, module, result = tkns[:3]
            return sample, module, result
        except ValueError:
            raise

    def _run_metadata_hooks(self, hooks):
        for sample in self.samples:
            self.metadata[sample] = {}
            for hook in hooks:
                key, val = hook(sample)
                self.metadata[sample][key] = val
