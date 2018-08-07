#!/usr/bin/env python3

import unittest

from dabasco.adf.adf_node import ADFNode

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestADFNode(unittest.TestCase):

    def test_equivalence1(self):
        node1 = ADFNode(ADFNode.LEAF, 'name')
        node2 = ADFNode(ADFNode.LEAF, ['name'])

        self.assertTrue(node1.is_equivalent_to(node2))

    def test_equivalence2(self):
        node1 = ADFNode(ADFNode.LEAF, 'name')
        node2 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE)

        self.assertFalse(node1.is_equivalent_to(node2))

    def test_equivalence3(self):
        node1 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE)
        node2 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE)

        self.assertFalse(node1.is_equivalent_to(node2))

    def test_equivalence4(self):
        node0 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE)
        node1 = ADFNode(ADFNode.NOT, node0)
        node2 = ADFNode(ADFNode.NOT, [node0])

        self.assertTrue(node1.is_equivalent_to(node2))

    def test_equivalence5(self):
        node0 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE)
        node1 = ADFNode(ADFNode.NOT, node0)
        node2 = ADFNode(ADFNode.NOT, [node0, node0])

        self.assertFalse(node1.is_equivalent_to(node2))

    def test_equivalence6(self):
        node0 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE)
        node1 = ADFNode(ADFNode.NOT, node0)
        node2 = ADFNode(ADFNode.NOT, ADFNode.CONSTANT_FALSE)

        self.assertFalse(node1.is_equivalent_to(node2))

    def test_equivalence7(self):
        node0 = ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE)
        node1 = ADFNode(ADFNode.NOT, ADFNode.CONSTANT_FALSE)
        node2 = ADFNode(ADFNode.NOT, node0)

        self.assertFalse(node1.is_equivalent_to(node2))


if __name__ == '__main__':
    unittest.main()
