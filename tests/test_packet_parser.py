"""Test suite for packet building."""

import pandas as pd

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

    def test_metadata_filter_general(self):
        """Test that a basic table is metadata filtered."""
        metadata = pd.DataFrame({'foo': {'haib18CEM5332_HMGTJCCXY_SL342402': 1}})
        table_factory = DataTableFactory(PACKET_DIR, metadata_tbl=metadata)
        tbl = table_factory.macrobes()
        self.assertEqual(tbl.shape, (1, 38))

    def test_metadata_filter_hmp(self):
        """Test that a basic table is metadata filtered."""
        table_factory = DataTableFactory(PACKET_DIR)
        hmp1 = table_factory.hmp()

        metadata = pd.DataFrame({'foo': {'haib18CEM5332_HMGTJCCXY_SL342402': 1}})
        table_factory.set_metadata(metadata)
        hmp2 = table_factory.hmp()

        self.assertEqual(hmp1.shape[0], hmp2.shape[0] // 2)
