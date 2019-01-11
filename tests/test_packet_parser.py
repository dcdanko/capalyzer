"""Test suite for packet building."""

from unittest import TestCase
from os.path import join, dirname

from capalyzer.packet_parser import DataTableFactory


PACKET_DIR = join(dirname(__file__), 'built_packet')


def basic_test_runner(tester, name):
    """Check that we can build a table."""
    table_factory = DataTableFactory(PACKET_DIR)
    tbl = getattr(table_factory, name)()
    tester.assertEqual(tbl.shape[0], 2)


class TestPacketParser(TestCase):
    """Test suite for packet building."""

    def test_make_taxonomy(self):
        """Test that we can build a taxonomy table."""
        basic_test_runner(self, 'taxonomy')

    def test_make_amr(self):
        """Test we can make AMR table."""
        basic_test_runner(self, 'amrs')

    def test_make_pathways(self):
        """Test we can make pathways table."""
        basic_test_runner(self, 'pathways')

    def test_make_ags(self):
        """Test we can make AGS vec."""
        table_factory = DataTableFactory(PACKET_DIR)
        table_factory.ags()

    def test_make_hmp(self):
        """Test we can make HMP table."""
        table_factory = DataTableFactory(PACKET_DIR)
        table_factory.hmp()

    def test_make_macrobes(self):
        """Test we can make macrobe table."""
        basic_test_runner(self, 'macrobes')

    def test_read_props(self):
        """Test we can make read prop table."""
        basic_test_runner(self, 'read_props')

    def test_taxa_alpha_div(self):
        """Test we can make alpha div vec."""
        table_factory = DataTableFactory(PACKET_DIR)
        table_factory.taxa_alpha_diversity()

    def test_taxa_chao1(self):
        """Test we can make alpha div vec."""
        table_factory = DataTableFactory(PACKET_DIR)
        table_factory.taxa_alpha_diversity(metric='chao1', rarefy=1000)

    def test_taxa_beta_div(self):
        """Test we can make beta div table."""
        basic_test_runner(self, 'taxa_beta_diversity')
