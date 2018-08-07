#!/usr/bin/env python3

import unittest

from dabasco.af.af_graph import AF

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestAFGraph(unittest.TestCase):

    def test_names1(self):
        af = AF(1)
        arg = 0
        name = "name"
        af.set_argument_name(arg, name)
        self.assertEqual(af.get_name_for_argument(arg), name)

    def test_names2(self):
        af = AF(1)
        arg = 0
        name = "name"
        af.set_argument_name(arg, name)
        self.assertEqual(af.get_argument_for_name(name), arg)

    def test_names3(self):
        af = AF(1)
        arg = 0
        self.assertEqual(af.get_name_for_argument(arg), arg)

    def test_names4(self):
        af = AF(1)
        name = "name"
        self.assertEqual(af.get_argument_for_name(name), None)

    def test_equivalence1(self):
        af1 = AF(0)
        af2 = AF(0)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence2(self):
        af1 = AF(1)
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af1.set_argument(0, AF.DEFINITE_ARGUMENT)
        af2 = AF(1)
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2.set_argument(0, AF.NO_ARGUMENT)
        self.assertFalse(af1.is_equivalent_to(af2))

    def test_equivalence3(self):
        af1 = AF(1)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_1')
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence4(self):
        af1 = AF(1)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_a')
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence5(self):
        af1 = AF(1)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_1')
        af2.set_attack(0, 0, AF.NO_ATTACK)
        self.assertFalse(af1.is_equivalent_to(af2))

    def test_equivalence6(self):
        af1 = AF(2)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_1')
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        self.assertFalse(af1.is_equivalent_to(af2))

    def test_equivalence7(self):
        af1 = AF(2)
        af1.set_argument_name(0, 'arg_1')
        af1.set_argument_name(1, 'arg_2')
        af1.set_attack(0, 0, AF.NO_ATTACK)
        af1.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af1.set_attack(1, 0, AF.DEFINITE_ATTACK)
        af1.set_attack(1, 1, AF.NO_ATTACK)
        af2 = AF(2)
        af2.set_argument_name(0, 'arg_1')
        af2.set_argument_name(1, 'arg_2')
        af2.set_attack(0, 0, AF.NO_ATTACK)
        af2.set_attack(0, 1, AF.DEFINITE_ATTACK)
        af2.set_attack(1, 0, AF.DEFINITE_ATTACK)
        af2.set_attack(1, 1, AF.NO_ATTACK)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence8(self):
        af1 = AF(0)
        af2 = None
        self.assertFalse(af1.is_equivalent_to(af2))


if __name__ == '__main__':
    unittest.main()
