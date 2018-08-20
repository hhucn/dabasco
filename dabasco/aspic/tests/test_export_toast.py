#!/usr/bin/env python3

import unittest

from dabasco.aspic.export_toast import export_toast
from dabasco.dbas.dbas_import import import_dbas_user, import_dbas_graph

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestASPICExport(unittest.TestCase):

    def test_discussion1_weak_user1_no_assumptions(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "weak"
        assumptions_type = None
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy=>2",
            "[ur3] opinion_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[ua2] < [i1]",
            "[ua2] < [i2]",
            "[ur3] < [i1]",
            "[ur3] < [i2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_no_user_weak_assumptions_no_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "weak"
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = None

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[r1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[r2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [i1]",
            "[a1] < [i2]",
            "[r1] < [i1]",
            "[r1] < [i2]",
            "[a2] < [i1]",
            "[a2] < [i2]",
            "[r2] < [i1]",
            "[r2] < [i2]",
            "[a3] < [i1]",
            "[a3] < [i2]",
            "[r3] < [i1]",
            "[r3] < [i2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_no_user_weak_assumptions_positive_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "weak"
        assumptions_bias = "positive"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = None

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [i1]",
            "[a1] < [i2]",
            "[a2] < [i1]",
            "[a2] < [i2]",
            "[a3] < [i1]",
            "[a3] < [i2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_no_user_weak_assumptions_negative_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "weak"
        assumptions_bias = "negative"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = None

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[r1] assumptions_dummy=>~1",
            "[r2] assumptions_dummy=>~2",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[r1] < [i1]",
            "[r1] < [i2]",
            "[r2] < [i1]",
            "[r2] < [i2]",
            "[r3] < [i1]",
            "[r3] < [i2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_no_user_strong_assumptions_no_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "strong"
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = None

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[r1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[r2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_no_user_strong_assumptions_positive_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "strong"
        assumptions_bias = "positive"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = None

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_no_user_strong_assumptions_negative_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "strong"
        assumptions_bias = "negative"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = None

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[r1] assumptions_dummy=>~1",
            "[r2] assumptions_dummy=>~2",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_strong_user1_weak_assumptions_no_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy=>2",
            "[ur3] opinion_dummy=>~3",
            "[a1] assumptions_dummy=>1",
            "[r1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[r2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [i1]",
            "[a1] < [i2]",
            "[r1] < [i1]",
            "[r1] < [i2]",
            "[a2] < [i1]",
            "[a2] < [i2]",
            "[r2] < [i1]",
            "[r2] < [i2]",
            "[a3] < [i1]",
            "[a3] < [i2]",
            "[r3] < [i1]",
            "[r3] < [i2]",
            "[a1] < [ua2]",
            "[a1] < [ur3]",
            "[r1] < [ua2]",
            "[r1] < [ur3]",
            "[a2] < [ua2]",
            "[a2] < [ur3]",
            "[r2] < [ua2]",
            "[r2] < [ur3]",
            "[a3] < [ua2]",
            "[a3] < [ur3]",
            "[r3] < [ua2]",
            "[r3] < [ur3]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_strong_user1_weak_assumptions_positive_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = "positive"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy=>2",
            "[ur3] opinion_dummy=>~3",
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [i1]",
            "[a1] < [i2]",
            "[a2] < [i1]",
            "[a2] < [i2]",
            "[a3] < [i1]",
            "[a3] < [i2]",
            "[a1] < [ua2]",
            "[a1] < [ur3]",
            "[a2] < [ua2]",
            "[a2] < [ur3]",
            "[a3] < [ua2]",
            "[a3] < [ur3]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_strong_user1_weak_assumptions_negative_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = "negative"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy=>2",
            "[ur3] opinion_dummy=>~3",
            "[r1] assumptions_dummy=>~1",
            "[r2] assumptions_dummy=>~2",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = {
            "[r1] < [i1]",
            "[r1] < [i2]",
            "[r2] < [i1]",
            "[r2] < [i2]",
            "[r3] < [i1]",
            "[r3] < [i2]",
            "[r1] < [ua2]",
            "[r1] < [ur3]",
            "[r2] < [ua2]",
            "[r2] < [ur3]",
            "[r3] < [ua2]",
            "[r3] < [ur3]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_strict_user1_strong_assumptions_no_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy->2",
            "[ur3] opinion_dummy->~3",
            "[a1] assumptions_dummy=>1",
            "[r1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[r2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_strict_user1_strong_assumptions_positive_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = "positive"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy->2",
            "[ur3] opinion_dummy->~3",
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion1_strict_user1_strong_assumptions_negative_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = "negative"
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }
        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua2] opinion_dummy->2",
            "[ur3] opinion_dummy->~3",
            "[r1] assumptions_dummy=>~1",
            "[r2] assumptions_dummy=>~2",
            "[r3] assumptions_dummy=>~3",
            "[i1] 2=>1",
            "[i2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion2_weak_user2_no_assumptions(self):
        discussion_id = 2
        user_id = 2
        opinion_type = "weak"
        assumptions_type = None
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]},
                {"conclusion": 2, "id": 3, "is_supportive": False, "premises": [4]}
            ],
            "nodes": [1, 2, 3, 4, 5],
            "undercuts": [
                {"conclusion": 2, "id": 4, "premises": [5]}
            ]
        }
        dbas_user_json = {
            "accepted_statements_via_click": [3],
            "marked_arguments": [],
            "marked_statements": [4],
            "rejected_arguments": [],
            "rejected_statements_via_click": [5],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua3] opinion_dummy=>3",
            "[ua4] opinion_dummy=>4",
            "[ur5] opinion_dummy=>~5",
            "[i1] 2=>1",
            "[i2] 3=>~1",
            "[i3] 4=>~2",
            "[i4] 5=>~[i2]"
        }
        reference_rulePrefs = {
            "[ua3] < [i1]",
            "[ua3] < [i2]",
            "[ua3] < [i3]",
            "[ua3] < [i4]",
            "[ua4] < [i1]",
            "[ua4] < [i2]",
            "[ua4] < [i3]",
            "[ua4] < [i4]",
            "[ur5] < [i1]",
            "[ur5] < [i2]",
            "[ur5] < [i3]",
            "[ur5] < [i4]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion2_strong_user2_weak_assumptions_no_bias(self):
        discussion_id = 2
        user_id = 2
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]},
                {"conclusion": 2, "id": 3, "is_supportive": False, "premises": [4]}
            ],
            "nodes": [1, 2, 3, 4, 5],
            "undercuts": [
                {"conclusion": 2, "id": 4, "premises": [5]}
            ]
        }
        dbas_user_json = {
            "accepted_statements_via_click": [3],
            "marked_arguments": [],
            "marked_statements": [4],
            "rejected_arguments": [],
            "rejected_statements_via_click": [5],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[ua3] opinion_dummy=>3",
            "[ua4] opinion_dummy=>4",
            "[ur5] opinion_dummy=>~5",
            "[a1] assumptions_dummy=>1",
            "[r1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[r2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[r3] assumptions_dummy=>~3",
            "[a4] assumptions_dummy=>4",
            "[r4] assumptions_dummy=>~4",
            "[a5] assumptions_dummy=>5",
            "[r5] assumptions_dummy=>~5",
            "[i1] 2=>1",
            "[i2] 3=>~1",
            "[i3] 4=>~2",
            "[i4] 5=>~[i2]"
        }
        reference_rulePrefs = {
            "[a1] < [i1]",
            "[a1] < [i2]",
            "[a1] < [i3]",
            "[a1] < [i4]",
            "[r1] < [i1]",
            "[r1] < [i2]",
            "[r1] < [i3]",
            "[r1] < [i4]",
            "[a2] < [i1]",
            "[a2] < [i2]",
            "[a2] < [i3]",
            "[a2] < [i4]",
            "[r2] < [i1]",
            "[r2] < [i2]",
            "[r2] < [i3]",
            "[r2] < [i4]",
            "[a3] < [i1]",
            "[a3] < [i2]",
            "[a3] < [i3]",
            "[a3] < [i4]",
            "[r3] < [i1]",
            "[r3] < [i2]",
            "[r3] < [i3]",
            "[r3] < [i4]",
            "[a4] < [i1]",
            "[a4] < [i2]",
            "[a4] < [i3]",
            "[a4] < [i4]",
            "[r4] < [i1]",
            "[r4] < [i2]",
            "[r4] < [i3]",
            "[r4] < [i4]",
            "[a5] < [i1]",
            "[a5] < [i2]",
            "[a5] < [i3]",
            "[a5] < [i4]",
            "[r5] < [i1]",
            "[r5] < [i2]",
            "[r5] < [i3]",
            "[r5] < [i4]",
            "[a1] < [ua3]",
            "[a1] < [ua4]",
            "[a1] < [ur5]",
            "[r1] < [ua3]",
            "[r1] < [ua4]",
            "[r1] < [ur5]",
            "[a2] < [ua3]",
            "[a2] < [ua4]",
            "[a2] < [ur5]",
            "[r2] < [ua3]",
            "[r2] < [ua4]",
            "[r2] < [ur5]",
            "[a3] < [ua3]",
            "[a3] < [ua4]",
            "[a3] < [ur5]",
            "[r3] < [ua3]",
            "[r3] < [ua4]",
            "[r3] < [ur5]",
            "[a4] < [ua3]",
            "[a4] < [ua4]",
            "[a4] < [ur5]",
            "[r4] < [ua3]",
            "[r4] < [ua4]",
            "[r4] < [ur5]",
            "[a5] < [ua3]",
            "[a5] < [ua4]",
            "[a5] < [ur5]",
            "[r5] < [ua3]",
            "[r5] < [ua4]",
            "[r5] < [ur5]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)
        self.assertEqual(aspic_result["semantics"], semantics)

    def test_discussion2_strict_user2_strong_assumptions_no_bias(self):
        discussion_id = 2
        user_id = 2
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = None
        semantics = "preferred"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]},
                {"conclusion": 2, "id": 3, "is_supportive": False, "premises": [4]}
            ],
            "nodes": [1, 2, 3, 4, 5],
            "undercuts": [
                {"conclusion": 2, "id": 4, "premises": [5]}
            ]
        }
        dbas_user_json = {
            "accepted_statements_via_click": [3],
            "marked_arguments": [],
            "marked_statements": [4],
            "rejected_arguments": [],
            "rejected_statements_via_click": [5],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        aspic_result = export_toast(dbas_graph=dbas_discussion,
                                    opinion_type=opinion_type,
                                    opinion=dbas_user,
                                    assumptions_type=assumptions_type,
                                    assumptions_bias=assumptions_bias,
                                    semantics=semantics)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kb_prefs = set()
        reference_rules = {
            "[ua3] opinion_dummy->3",
            "[ua4] opinion_dummy->4",
            "[ur5] opinion_dummy->~5",
            "[a1] assumptions_dummy=>1",
            "[r1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[r2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[r3] assumptions_dummy=>~3",
            "[a4] assumptions_dummy=>4",
            "[r4] assumptions_dummy=>~4",
            "[a5] assumptions_dummy=>5",
            "[r5] assumptions_dummy=>~5",
            "[i1] 2=>1",
            "[i2] 3=>~1",
            "[i3] 4=>~2",
            "[i4] 5=>~[i2]"
        }
        reference_rule_prefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kb_prefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rule_prefs)
        self.assertEqual(aspic_result["semantics"], semantics)


if __name__ == '__main__':
    unittest.main()
