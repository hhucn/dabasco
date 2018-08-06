#!/usr/bin/env python3

import unittest

from dabasco.af.af_graph import AF

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestAFGraph(unittest.TestCase):

    def test_equivalence1(self):
        af1 = AF(0)
        af2 = AF(0)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence2(self):
        af1 = AF(1)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_1')
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence3(self):
        af1 = AF(1)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_a')
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        self.assertTrue(af1.is_equivalent_to(af2))

    def test_equivalence4(self):
        af1 = AF(1)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_1')
        af2.set_attack(0, 0, AF.NO_ATTACK)
        self.assertFalse(af1.is_equivalent_to(af2))

    def test_equivalence5(self):
        af1 = AF(2)
        af1.set_argument_name(0, 'arg_1')
        af1.set_attack(0, 0, AF.DEFINITE_ATTACK)
        af2 = AF(1)
        af2.set_argument_name(0, 'arg_1')
        af2.set_attack(0, 0, AF.DEFINITE_ATTACK)
        self.assertFalse(af1.is_equivalent_to(af2))

    def test_equivalence6(self):
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


if __name__ == '__main__':
    unittest.main()
