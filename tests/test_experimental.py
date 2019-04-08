"""Test suite for experimental functions."""

import pandas as pd

from unittest import TestCase
from os.path import join, dirname

from capalyzer.packet_parser import DataTableFactory
from capalyzer.packet_parser.experimental import umap, fractal_dimension

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
