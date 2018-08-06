#!/usr/bin/env python3

import unittest

from dabasco.af.af_graph import AF
from dabasco.af.export import export_aspartix

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestAFExport(unittest.TestCase):

    def test_1arg_1(self):
        af = AF(1)
        af.set_argument_name(0, "name")
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        outputs = ['arg(name).']
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_1arg_2(self):
        af = AF(1)
        af.set_argument_name(0, "name")
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 0, AF.DEFINITE_ATTACK)
        outputs = ['arg(name).', 'att(name,name).']
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_1arg_3(self):
        af = AF(1)
        af.set_argument_name(0, "name")
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        outputs = []
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_1arg_4(self):
        af = AF(1)
        af.set_argument_name(0, "name")
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_attack(0, 0, AF.DEFINITE_ATTACK)
        outputs = []
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2args_1(self):
        af = AF(2)
        af.set_argument_name(0, "name1")
        af.set_argument_name(1, "name2")
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        af.set_attack(0, 1, AF.NO_ATTACK)
        af.set_attack(1, 0, AF.NO_ATTACK)
        af.set_attack(1, 1, AF.NO_ATTACK)
        outputs = ['arg(name1).', 'arg(name2).']
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2args_2(self):
        af = AF(2)
        af.set_argument_name(0, "name1")
        af.set_argument_name(1, "name2")
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 0, AF.DEFINITE_ATTACK)
        af.set_attack(1, 1, AF.NO_ATTACK)
        outputs = ['arg(name1).', 'arg(name2).', 'att(name1,name2).', 'att(name2,name1).']
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2args_3(self):
        af = AF(2)
        af.set_argument_name(0, "name1")
        af.set_argument_name(1, "name2")
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_argument(1, AF.DEFINITE_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 0, AF.DEFINITE_ATTACK)
        af.set_attack(1, 1, AF.NO_ATTACK)
        outputs = ['arg(name2).']
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2args_4(self):
        af = AF(2)
        af.set_argument_name(0, "name1")
        af.set_argument_name(1, "name2")
        af.set_argument(0, AF.DEFINITE_ARGUMENT)
        af.set_argument(1, AF.NO_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 0, AF.DEFINITE_ATTACK)
        af.set_attack(1, 1, AF.NO_ATTACK)
        outputs = ['arg(name1).']
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)

    def test_2args_5(self):
        af = AF(2)
        af.set_argument_name(0, "name1")
        af.set_argument_name(1, "name2")
        af.set_argument(0, AF.NO_ARGUMENT)
        af.set_argument(1, AF.NO_ARGUMENT)
        af.set_attack(0, 0, AF.NO_ATTACK)
        af.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af.set_attack(1, 0, AF.DEFINITE_ATTACK)
        af.set_attack(1, 1, AF.NO_ATTACK)
        outputs = []
        export = export_aspartix(af)
        export_list = export.split('\n')
        export_list.remove('')  # Discard empty new line at the end
        self.assertEqual(len(outputs), len(export_list))
        for output in outputs:
            logging.debug('%s in %s', output, export_list)
            self.assertTrue(output in export)


if __name__ == '__main__':
    unittest.main()
