
from unittest import TestCase

from capalyzer.packet_parser import NCBITaxaTree


class TestTaxaTree(TestCase):

    def setUp(self):
        """Test that we can make a taxa tree."""
        self.tree = NCBITaxaTree.parse_files()

    def test_tree_sort(self):
        taxa = [
            'Cutibacterium acnes', 'Cutibacterium granulosum', 
            'Bacteria', 'Escherichia', 'Escherichia coli',
            'Cutibacterium'
        ]
        sort = self.tree.taxa_sort(taxa)
        self.assertEqual(len(taxa), len(sort))

    def test_get_phylum(self):
        self.tree.phyla('Escherichia coli')

    def test_get_parent(self):
        self.tree.parent('Cutibacterium acnes')

    def test_get_ancestors(self):
        ancestors = self.tree.ancestors('Cutibacterium acnes')
        true = [
            'Cutibacterium acnes',
            'Cutibacterium',
            'Propionibacteriaceae',
            'Propionibacteriales',
            'Actinobacteria',
            'Actinobacteria',
            'Terrabacteria group',
            'Bacteria',
            'cellular organisms',
            'root'
        ]
        for i, anc in enumerate(ancestors):
            self.assertEqual(anc, true[i])
