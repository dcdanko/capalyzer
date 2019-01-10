"""Test suite for packet building."""

from unittest import TestCase
from os.path import isfile, join, dirname

from capalyzer.packet_builder import make_all_tables


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
        for filename in filenames:
            self.assertTrue(isfile(filename))
