#!/usr/bin/env python3

import unittest

from dabasco.adf.adf_graph import ADF
from dabasco.adf.adf_node import ADFNode
from dabasco.adf.export_diamond import export_diamond

from os import path
import logging
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestADFExport(unittest.TestCase):

    def test_1statement_test1(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_FALSE]))
        outputs = ['s(s1).', 'ac(s1,c(f)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_1statement_test2(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        outputs = ['s(s1).', 'ac(s1,c(v)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    # -----------------------------------------------------
    def test_2statements_test1(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, ['s1']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,s1).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test2(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.NOT, ['s1']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,neg(s1)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test3(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, ['s2']))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, ['s1']))
        outputs = ['s(s1).', 'ac(s1,s2).', 's(s2).', 'ac(s2,s1).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test4(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.NOT, ['s1']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,neg(s1)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test5(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.NOT, ['s2']))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, ['s1']))
        outputs = ['s(s1).', 'ac(s1,neg(s2)).', 's(s2).', 'ac(s2,s1).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test6(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.NOT, ['s2']))
        adf.add_statement('s2', ADFNode(ADFNode.NOT, ['s1']))
        outputs = ['s(s1).', 'ac(s1,neg(s2)).', 's(s2).', 'ac(s2,neg(s1)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test7(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.AND, ['s1']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,s1).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2statements_test8(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.OR, ['s1']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,s1).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    # -----------------------------------------------------
    def test_3statements_test1(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s3', ADFNode(ADFNode.AND, ['s1', 's2']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,c(v)).', 's(s3).', 'ac(s3,and(s1,s2)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_3statements_test2(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s3', ADFNode(ADFNode.OR, ['s1', 's2']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,c(v)).', 's(s3).', 'ac(s3,or(s1,s2)).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    # -----------------------------------------------------
    def test_4statements_test1(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s3', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s4', ADFNode(ADFNode.AND, ['s1', 's2', 's3']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,c(v)).', 's(s3).', 'ac(s3,c(v)).', 's(s4).',
                   'ac(s4,and(s1,and(s2,s3))).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_4statements_test2(self):
        adf = ADF()
        adf.add_statement('s1', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s2', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s3', ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
        adf.add_statement('s4', ADFNode(ADFNode.OR, ['s1', 's2', 's3']))
        outputs = ['s(s1).', 'ac(s1,c(v)).', 's(s2).', 'ac(s2,c(v)).', 's(s3).', 'ac(s3,c(v)).', 's(s4).',
                   'ac(s4,or(s1,or(s2,s3))).']
        export = export_diamond(adf)
        export_list = export.split('\n')
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)


if __name__ == '__main__':
    unittest.main()
