"""Test suite for packet building."""

import pandas as pd

from unittest import TestCase
from os.path import join, dirname

from capalyzer.packet_parser import DataTableFactory
from capalyzer.packet_parser.data_utils import group_small_cols


PACKET_DIR = join(dirname(__file__), 'built_packet')


def basic_test_runner(tester, name, nrows=2, **kwargs):
    """Check that we can build a table."""
    table_factory = DataTableFactory(PACKET_DIR)
    tbl = getattr(table_factory, name)(**kwargs)
    if nrows >= 0:
        tester.assertEqual(tbl.shape[0], nrows)


class TestPacketParser(TestCase):
    """Test suite for packet building."""

    def test_make_taxonomy(self):
        """Test that we can build a taxonomy table."""
        basic_test_runner(self, 'taxonomy')

    def test_group_small_cols(self):
        """Test that we can build a taxonomy table."""
        taxa = DataTableFactory(PACKET_DIR).taxonomy()
        taxa = group_small_cols(taxa, top=2)
        self.assertEqual(taxa.shape[1], 3)

    def test_subsample_taxonomy(self):
        """Test that we can build a taxonomy table."""
        basic_test_runner(self, 'taxonomy', nrows=6, niter=3, normalize='subsample')

    def test_make_core_taxa(self):
        """Test that we can build a taxonomy table."""
        basic_test_runner(self, 'core_taxa', nrows=-1)

    def test_make_taxa_long(self):
        """Test that we can build a taxonomy table from longform."""
        basic_test_runner(self, 'taxonomy', rank='all')

    def test_make_amr(self):
        """Test we can make AMR table."""
        basic_test_runner(self, 'amrs', nrows=0)

    def test_make_pathways(self):
        """Test we can make pathways table."""
        basic_test_runner(self, 'pathways')

    def test_make_pathways_with_coverage_min(self):
        """Test we can make pathways table."""
        basic_test_runner(self, 'pathways', coverage_min=0.5)

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
        entropy = table_factory.taxa_alpha_diversity()
        self.assertTrue((entropy > 0).all())

    def test_taxa_alpha_div_genus(self):
        """Test we can make alpha div vec."""
        table_factory = DataTableFactory(PACKET_DIR)
        entropy = table_factory.taxa_alpha_diversity(rank='genus')
        self.assertTrue((entropy > 0).all())

    def test_taxa_chao1(self):
        """Test we can make alpha div vec."""
        table_factory = DataTableFactory(PACKET_DIR)
        chao1 = table_factory.taxa_alpha_diversity(metric='chao1', rarefy=1000 * 1000)
        self.assertTrue((chao1 > 0).all())

    def test_taxa_beta_div(self):
        """Test we can make beta div table."""
        basic_test_runner(self, 'taxa_beta_diversity')

    def test_taxa_rarefaction(self):
        table_factory = DataTableFactory(PACKET_DIR)
        rarefied = table_factory.taxa_rarefaction(ns=[1, 2, 3, 4], nsample=2)
        self.assertEqual(rarefied.shape[1], 2)
        self.assertEqual(rarefied.shape[0], 10)

    def test_metadata_filter_general(self):
        """Test that a basic table is metadata filtered."""
        metadata = pd.DataFrame({'foo': {'haib18CEM5332_HMGTJCCXY_SL342402': 1}})
        table_factory = DataTableFactory(PACKET_DIR, metadata_tbl=metadata)
        tbl = table_factory.macrobes()
        self.assertEqual(tbl.shape, (1, 37))

    def test_metadata_filter_hmp(self):
        """Test that a basic table is metadata filtered."""
        table_factory = DataTableFactory(PACKET_DIR)
        hmp1 = table_factory.hmp()

        metadata = pd.DataFrame({'foo': {'haib18CEM5332_HMGTJCCXY_SL342402': 1}})
        table_factory.set_metadata(metadata)
        hmp2 = table_factory.hmp()

        self.assertEqual(hmp1.shape[0] // 2, hmp2.shape[0])
