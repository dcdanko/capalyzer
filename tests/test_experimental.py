"""Test suite for experimental functions."""

import pandas as pd

from unittest import TestCase
from os.path import join, dirname

from capalyzer.packet_parser import DataTableFactory
from capalyzer.packet_parser.experimental import (
    umap,
    fractal_dimension,
    pca_sample_cross_val,
)

PACKET_DIR = join(dirname(__file__), 'built_packet')


class TestPacketParser(TestCase):
    """Test suite for packet building."""

    def test_umap(self):
        """Test that we can run UMAP."""
        taxa = DataTableFactory(PACKET_DIR).taxonomy()
        taxa = pd.DataFrame(pd.concat([taxa, taxa, taxa]))
        umap(taxa, n_neighbors=3)

    def test_fractal(self):
        """Test that we can run fractal."""
        taxa = DataTableFactory(PACKET_DIR).taxonomy()
        taxa = pd.DataFrame(pd.concat([taxa, taxa, taxa]))
        taxa = umap(taxa, n_neighbors=3)
        fractal_dimension(taxa, scales=range(1, 3))

    def test_pca_cross_val(self):
        taxa = DataTableFactory(PACKET_DIR).taxonomy()
        taxa = pd.DataFrame(pd.concat([taxa] * 10))
        taxa_copy = taxa.copy(deep=True)
        catch_losses = []  # demo of how to extract detailed loss info
        taxa_pca = pca_sample_cross_val(taxa, comp_step=10, losses=catch_losses)
        self.assertEqual(taxa.shape[0], taxa_pca.shape[0])
        self.assertEqual(taxa.shape[1], taxa_pca.shape[1])
        self.assertEqual((taxa - taxa_copy).sum().sum(), 0)