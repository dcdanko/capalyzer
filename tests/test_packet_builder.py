"""Test suite for packet building."""

from unittest import TestCase
from os.path import isfile, join, dirname

from capalyzer.packet_builder import make_all_tables

from capalyzer.constants import (
    CARD_RPKM,
    CARD_RPKMG,
    MEGARES_CLASS_RPKM,
    MEGARES_CLASS_RPKMG,
    MEGARES_GENE_RPKM,
    MEGARES_GENE_RPKMG,
    MEGARES_GROUP_RPKM,
    MEGARES_GROUP_RPKMG,
    MEGARES_MECH_RPKM,
    MEGARES_MECH_RPKMG,
    AVE_GENOME_SIZE,
    HMP_COMPARISON,
    MACROBES,
    READ_PROPORTIONS,
    UNIREF90_COV,
    UNIREF90_RELAB,
    MPA_RELAB,
    KRAKENHLL_REFSEQ,
    KRAKENHLL_REFSEQ_MEDIUM,
    KRAKENHLL_REFSEQ_STRICT,
)

ALL_FILES = [
    CARD_RPKM,
    CARD_RPKMG,
    MEGARES_CLASS_RPKM,
    MEGARES_CLASS_RPKMG,
    MEGARES_GENE_RPKM,
    MEGARES_GENE_RPKMG,
    MEGARES_GROUP_RPKM,
    MEGARES_GROUP_RPKMG,
    MEGARES_MECH_RPKM,
    MEGARES_MECH_RPKMG,
    AVE_GENOME_SIZE,
    HMP_COMPARISON,
    MACROBES,
    READ_PROPORTIONS,
    UNIREF90_COV,
    UNIREF90_RELAB,
    MPA_RELAB,
    KRAKENHLL_REFSEQ,
    KRAKENHLL_REFSEQ_MEDIUM,
    KRAKENHLL_REFSEQ_STRICT,
]


PACKET_DIR = join(dirname(__file__), 'built_packet')
CAP_OUT_DIR = join(dirname(__file__), 'cap_output')


class TestPacketBuilder(TestCase):
    """Test suite for packet building."""

    def test_make_all(self):
        """Test that we can build a datapacket from CAP output."""
        filenames = make_all_tables(
            CAP_OUT_DIR,
            PACKET_DIR,
            overwrite=True,
        )
        files_made = set()
        for filename in filenames:
            files_made.add(filename)
            self.assertTrue(isfile(filename))

        for intended_file in ALL_FILES:
            self.assertIn(join(PACKET_DIR, intended_file), files_made)
