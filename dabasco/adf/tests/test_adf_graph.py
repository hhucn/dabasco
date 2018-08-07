#!/usr/bin/env python3

import unittest

from dabasco.adf.adf_graph import ADF
from dabasco.adf.adf_node import ADFNode

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestADFGraph(unittest.TestCase):

    def test_duplicate_statements(self):
        adf = ADF()
        adf.add_statement('name', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf.add_statement('name', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        reference_node = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE)

        self.assertTrue(reference_node.is_equivalent_to(adf.acceptance['name']))

    def test_equivalence_true1(self):
        adf1 = ADF()
        adf1.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf1.add_statement('name2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf2 = ADF()
        adf2.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf2.add_statement('name2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        self.assertTrue(adf1.is_equivalent_to(adf2))

    def test_equivalence_true2(self):
        adf1 = ADF()
        adf1.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf1.add_statement('name2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        self.assertTrue(adf1.is_equivalent_to(adf1))

    def test_equivalence_false1(self):
        adf1 = ADF()
        adf1.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf1.add_statement('name2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf2 = ADF()
        adf2.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf2.add_statement('different_name', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        self.assertFalse(adf1.is_equivalent_to(adf2))

    def test_equivalence_false2(self):
        adf1 = ADF()
        adf1.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf1.add_statement('name2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf2 = ADF()
        adf2.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf2.add_statement('name2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf2.add_statement('name3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        self.assertFalse(adf1.is_equivalent_to(adf2))

    def test_equivalence_false3(self):
        adf1 = ADF()
        adf1.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf2 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE)

        self.assertFalse(adf1.is_equivalent_to(adf2))

    def test_equivalence_false4(self):
        adf1 = ADF()
        adf1.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf2 = ADF()
        adf2.add_statement('name1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        self.assertFalse(adf1.is_equivalent_to(adf2))


if __name__ == '__main__':
    unittest.main()
