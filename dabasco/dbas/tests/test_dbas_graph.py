#!/usr/bin/env python3

import unittest

from dabasco.dbas.dbas_graph import DBASGraph, Inference, Undercut

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestASPICExport(unittest.TestCase):

    def test_add_statement_empty(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = set()
        dbas_discussion.inferences = dict()
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_statement(1)

        self.assertEqual(dbas_discussion.statements, {1})

    def test_add_statement_nonempty(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1}
        dbas_discussion.inferences = dict()
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_statement(2)

        self.assertEqual(dbas_discussion.statements, {1, 2})

    def test_add_statement_already_exists(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1}
        dbas_discussion.inferences = dict()
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_statement(1)

        self.assertEqual(dbas_discussion.statements, {1})

    def test_add_inference_empty(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1, 2}
        dbas_discussion.inferences = dict()
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_inference(inference_id=1, premises=[2], conclusion=1, is_supportive=True)

        self.assertEqual(dbas_discussion.inferences, {
            1: Inference(1, [2], 1, True)
        })

    def test_add_inference_nonempty(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1, 2, 3}
        dbas_discussion.inferences = {
            2: Inference(2, [3], 1, False)
        }
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_inference(inference_id=1, premises=[2], conclusion=1, is_supportive=True)

        self.assertEqual(dbas_discussion.inferences, {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False)
        })

    def test_add_inference_already_exists(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1, 2, 3}
        dbas_discussion.inferences = {
            1: Inference(1, [3], 1, False)
        }
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_inference(inference_id=1, premises=[2], conclusion=1, is_supportive=True)

        self.assertEqual(dbas_discussion.inferences, {
            1: Inference(1, [2], 1, True)
        })

    def test_add_undercut_empty(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1, 2, 3}
        dbas_discussion.inferences = {
            1: Inference(1, [2], 1, True)
        }
        dbas_discussion.undercuts = dict()

        dbas_discussion.add_undercut(inference_id=2, premises=[3], conclusion=1)

        self.assertEqual(dbas_discussion.undercuts, {
            2: Undercut(2, [3], 1)
        })

    def test_add_undercut_nonempty(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1, 2, 3}
        dbas_discussion.inferences = {
            1: Inference(1, [2], 1, True)
        }
        dbas_discussion.undercuts = {
            3: Undercut(3, [1], 1)
        }

        dbas_discussion.add_undercut(inference_id=2, premises=[3], conclusion=1)

        self.assertEqual(dbas_discussion.undercuts, {
            2: Undercut(2, [3], 1),
            3: Undercut(3, [1], 1)
        })

    def test_add_undercut_already_exists(self):
        dbas_discussion = DBASGraph(discussion_id=1)
        dbas_discussion.statements = {1, 2, 3}
        dbas_discussion.inferences = {
            1: Inference(1, [2], 1, True)
        }
        dbas_discussion.undercuts = {
            2: Undercut(2, [1], 1)
        }

        dbas_discussion.add_undercut(inference_id=2, premises=[3], conclusion=1)

        self.assertEqual(dbas_discussion.undercuts, {
            2: Undercut(2, [3], 1)
        })

    def test_equivalence_true_discussion1(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            2: Inference(2, [3], 1, False),
            1: Inference(1, [2], 1, True),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {3, 2, 1}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertTrue(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_true_discussion2(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
            4: Undercut(4, [5], 2)
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.undercuts = {
            4: Undercut(4, [5], 2)
        }
        dbas_discussion2.inferences = {
            3: Inference(3, [4], 2, False),
            2: Inference(2, [3], 1, False),
            1: Inference(1, [2], 1, True)
        }
        dbas_discussion2.statements = {5, 4, 3, 2, 1}

        self.assertTrue(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_IDs(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_wrong_type(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = {
            "nodes": [1, 2, 3],
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "undercuts": []
        }

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_statements(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3, 4}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_number_of_inferences1(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [1], 3, True),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_number_of_inferences2(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [1], 3, True),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_inferences1(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            2: Inference(2, [2], 1, True),
            1: Inference(1, [3], 1, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_inferences2(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            1: Inference(1, [3], 1, True),
            2: Inference(2, [2], 1, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_inferences3(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 2, False),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_inferences4(self):
        dbas_discussion1 = DBASGraph(discussion_id=1)
        dbas_discussion1.statements = {1, 2, 3}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion1.undercuts = dict()

        dbas_discussion2 = DBASGraph(discussion_id=1)
        dbas_discussion2.statements = {1, 2, 3}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, False),
            2: Inference(2, [3], 1, True),
        }
        dbas_discussion2.undercuts = dict()

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_number_of_undercuts1(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
            4: Undercut(4, [5], 2)
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3, 4, 5}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion2.undercuts = {}

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_number_of_undercuts2(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3, 4, 5}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion2.undercuts = {
            4: Undercut(4, [5], 2)
        }

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_undercuts1(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
            4: Undercut(4, [5], 2)
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3, 4, 5}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion2.undercuts = {
            5: Undercut(5, [5], 2)
        }

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_undercuts2(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
            4: Undercut(4, [5], 2)
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3, 4, 5}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion2.undercuts = {
            4: Undercut(4, [4], 2)
        }

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_undercuts3(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
            4: Undercut(4, [5], 2)
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3, 4, 5}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion2.undercuts = {
            4: Undercut(4, [5, 1], 2)
        }

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))

    def test_equivalence_different_undercuts4(self):
        dbas_discussion1 = DBASGraph(discussion_id=2)
        dbas_discussion1.statements = {1, 2, 3, 4, 5}
        dbas_discussion1.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion1.undercuts = {
            4: Undercut(4, [5], 2)
        }

        dbas_discussion2 = DBASGraph(discussion_id=2)
        dbas_discussion2.statements = {1, 2, 3, 4, 5}
        dbas_discussion2.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion2.undercuts = {
            4: Undercut(4, [5], 1)
        }

        self.assertFalse(dbas_discussion1.is_equivalent_to(dbas_discussion2))


if __name__ == '__main__':
    unittest.main()
