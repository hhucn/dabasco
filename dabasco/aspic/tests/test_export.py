#!/usr/bin/env python3

import unittest

from dabasco.aspic.export import export_toast
from dabasco.dbas_import import import_dbas_graph, import_dbas_user

from os import path
import logging
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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[o2] opinion_dummy=>2",
            "[o3] opinion_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[o2] < [r1]",
            "[o2] < [r2]",
            "[o3] < [r1]",
            "[o3] < [r2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_no_user_weak_assumptions_no_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "weak"
        assumptions_bias = None

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        aspic_result = export_toast(dbas_discussion, opinion_type, None, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[an1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[an2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [r1]",
            "[a1] < [r2]",
            "[an1] < [r1]",
            "[an1] < [r2]",
            "[a2] < [r1]",
            "[a2] < [r2]",
            "[an2] < [r1]",
            "[an2] < [r2]",
            "[a3] < [r1]",
            "[a3] < [r2]",
            "[an3] < [r1]",
            "[an3] < [r2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_no_user_weak_assumptions_positive_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "weak"
        assumptions_bias = "positive"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        aspic_result = export_toast(dbas_discussion, opinion_type, None, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [r1]",
            "[a1] < [r2]",
            "[a2] < [r1]",
            "[a2] < [r2]",
            "[a3] < [r1]",
            "[a3] < [r2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_no_user_weak_assumptions_negative_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "weak"
        assumptions_bias = "negative"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        aspic_result = export_toast(dbas_discussion, opinion_type, None, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[an1] assumptions_dummy=>~1",
            "[an2] assumptions_dummy=>~2",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[an1] < [r1]",
            "[an1] < [r2]",
            "[an2] < [r1]",
            "[an2] < [r2]",
            "[an3] < [r1]",
            "[an3] < [r2]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_no_user_strong_assumptions_no_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "strong"
        assumptions_bias = None

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        aspic_result = export_toast(dbas_discussion, opinion_type, None, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[an1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[an2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_no_user_strong_assumptions_positive_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "strong"
        assumptions_bias = "positive"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        aspic_result = export_toast(dbas_discussion, opinion_type, None, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_no_user_strong_assumptions_negative_bias(self):
        discussion_id = 1
        opinion_type = None
        assumptions_type = "strong"
        assumptions_bias = "negative"

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        aspic_result = export_toast(dbas_discussion, opinion_type, None, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[an1] assumptions_dummy=>~1",
            "[an2] assumptions_dummy=>~2",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_strong_user1_weak_assumptions_no_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = None

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[o2] opinion_dummy=>2",
            "[o3] opinion_dummy=>~3",
            "[a1] assumptions_dummy=>1",
            "[an1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[an2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [r1]",
            "[a1] < [r2]",
            "[an1] < [r1]",
            "[an1] < [r2]",
            "[a2] < [r1]",
            "[a2] < [r2]",
            "[an2] < [r1]",
            "[an2] < [r2]",
            "[a3] < [r1]",
            "[a3] < [r2]",
            "[an3] < [r1]",
            "[an3] < [r2]",
            "[a1] < [o2]",
            "[a1] < [o3]",
            "[an1] < [o2]",
            "[an1] < [o3]",
            "[a2] < [o2]",
            "[a2] < [o3]",
            "[an2] < [o2]",
            "[an2] < [o3]",
            "[a3] < [o2]",
            "[a3] < [o3]",
            "[an3] < [o2]",
            "[an3] < [o3]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_strong_user1_weak_assumptions_positive_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = "positive"

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[o2] opinion_dummy=>2",
            "[o3] opinion_dummy=>~3",
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[a1] < [r1]",
            "[a1] < [r2]",
            "[a2] < [r1]",
            "[a2] < [r2]",
            "[a3] < [r1]",
            "[a3] < [r2]",
            "[a1] < [o2]",
            "[a1] < [o3]",
            "[a2] < [o2]",
            "[a2] < [o3]",
            "[a3] < [o2]",
            "[a3] < [o3]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_strong_user1_weak_assumptions_negative_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = "negative"

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[o2] opinion_dummy=>2",
            "[o3] opinion_dummy=>~3",
            "[an1] assumptions_dummy=>~1",
            "[an2] assumptions_dummy=>~2",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = {
            "[an1] < [r1]",
            "[an1] < [r2]",
            "[an2] < [r1]",
            "[an2] < [r2]",
            "[an3] < [r1]",
            "[an3] < [r2]",
            "[an1] < [o2]",
            "[an1] < [o3]",
            "[an2] < [o2]",
            "[an2] < [o3]",
            "[an3] < [o2]",
            "[an3] < [o3]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_strict_user1_strong_assumptions_no_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = None

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy", "3", "2"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[an1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[an2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_strict_user1_strong_assumptions_positive_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = "positive"

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy", "2", "3"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[a2] assumptions_dummy=>2",
            "[a3] assumptions_dummy=>3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion1_strict_user1_strong_assumptions_negative_bias(self):
        discussion_id = 1
        user_id = 1
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = "negative"

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy", "2", "3"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[an1] assumptions_dummy=>~1",
            "[an2] assumptions_dummy=>~2",
            "[an3] assumptions_dummy=>~3",
            "[r1] 2=>1",
            "[r2] 3=>~1"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion2_weak_user2_no_assumptions(self):
        discussion_id = 2
        user_id = 2
        opinion_type = "weak"
        assumptions_type = None
        assumptions_bias = None

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[o3] opinion_dummy=>3",
            "[o4] opinion_dummy=>4",
            "[o5] opinion_dummy=>~5",
            "[r1] 2=>1",
            "[r2] 3=>~1",
            "[r3] 4=>~2",
            "[r4] 5=>~[r2]"
        }
        reference_rulePrefs = {
            "[o3] < [r1]",
            "[o3] < [r2]",
            "[o3] < [r3]",
            "[o3] < [r4]",
            "[o4] < [r1]",
            "[o4] < [r2]",
            "[o4] < [r3]",
            "[o4] < [r4]",
            "[o5] < [r1]",
            "[o5] < [r2]",
            "[o5] < [r3]",
            "[o5] < [r4]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion2_strong_user2_weak_assumptions_no_bias(self):
        discussion_id = 2
        user_id = 2
        opinion_type = "strong"
        assumptions_type = "weak"
        assumptions_bias = None

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[o3] opinion_dummy=>3",
            "[o4] opinion_dummy=>4",
            "[o5] opinion_dummy=>~5",
            "[a1] assumptions_dummy=>1",
            "[an1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[an2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[an3] assumptions_dummy=>~3",
            "[a4] assumptions_dummy=>4",
            "[an4] assumptions_dummy=>~4",
            "[a5] assumptions_dummy=>5",
            "[an5] assumptions_dummy=>~5",
            "[r1] 2=>1",
            "[r2] 3=>~1",
            "[r3] 4=>~2",
            "[r4] 5=>~[r2]"
        }
        reference_rulePrefs = {
            "[a1] < [r1]",
            "[a1] < [r2]",
            "[a1] < [r3]",
            "[a1] < [r4]",
            "[an1] < [r1]",
            "[an1] < [r2]",
            "[an1] < [r3]",
            "[an1] < [r4]",
            "[a2] < [r1]",
            "[a2] < [r2]",
            "[a2] < [r3]",
            "[a2] < [r4]",
            "[an2] < [r1]",
            "[an2] < [r2]",
            "[an2] < [r3]",
            "[an2] < [r4]",
            "[a3] < [r1]",
            "[a3] < [r2]",
            "[a3] < [r3]",
            "[a3] < [r4]",
            "[an3] < [r1]",
            "[an3] < [r2]",
            "[an3] < [r3]",
            "[an3] < [r4]",
            "[a4] < [r1]",
            "[a4] < [r2]",
            "[a4] < [r3]",
            "[a4] < [r4]",
            "[an4] < [r1]",
            "[an4] < [r2]",
            "[an4] < [r3]",
            "[an4] < [r4]",
            "[a5] < [r1]",
            "[a5] < [r2]",
            "[a5] < [r3]",
            "[a5] < [r4]",
            "[an5] < [r1]",
            "[an5] < [r2]",
            "[an5] < [r3]",
            "[an5] < [r4]",
            "[a1] < [o3]",
            "[a1] < [o4]",
            "[a1] < [o5]",
            "[an1] < [o3]",
            "[an1] < [o4]",
            "[an1] < [o5]",
            "[a2] < [o3]",
            "[a2] < [o4]",
            "[a2] < [o5]",
            "[an2] < [o3]",
            "[an2] < [o4]",
            "[an2] < [o5]",
            "[a3] < [o3]",
            "[a3] < [o4]",
            "[a3] < [o5]",
            "[an3] < [o3]",
            "[an3] < [o4]",
            "[an3] < [o5]",
            "[a4] < [o3]",
            "[a4] < [o4]",
            "[a4] < [o5]",
            "[an4] < [o3]",
            "[an4] < [o4]",
            "[an4] < [o5]",
            "[a5] < [o3]",
            "[a5] < [o4]",
            "[a5] < [o5]",
            "[an5] < [o3]",
            "[an5] < [o4]",
            "[an5] < [o5]"
        }

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)

    def test_discussion2_strict_user2_strong_assumptions_no_bias(self):
        discussion_id = 2
        user_id = 2
        opinion_type = "strict"
        assumptions_type = "strong"
        assumptions_bias = None

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

        aspic_result = export_toast(dbas_discussion, opinion_type, dbas_user, assumptions_type, assumptions_bias)

        reference_assumptions = set()
        reference_axioms = {"assumptions_dummy", "opinion_dummy", "3", "4", "~5"}
        reference_contrariness = set()
        reference_kbPrefs = set()
        reference_rules = {
            "[a1] assumptions_dummy=>1",
            "[an1] assumptions_dummy=>~1",
            "[a2] assumptions_dummy=>2",
            "[an2] assumptions_dummy=>~2",
            "[a3] assumptions_dummy=>3",
            "[an3] assumptions_dummy=>~3",
            "[a4] assumptions_dummy=>4",
            "[an4] assumptions_dummy=>~4",
            "[a5] assumptions_dummy=>5",
            "[an5] assumptions_dummy=>~5",
            "[r1] 2=>1",
            "[r2] 3=>~1",
            "[r3] 4=>~2",
            "[r4] 5=>~[r2]"
        }
        reference_rulePrefs = set()

        self.assertEqual(set(aspic_result["assumptions"]), reference_assumptions)
        self.assertEqual(set(aspic_result["axioms"]), reference_axioms)
        self.assertEqual(set(aspic_result["contrariness"]), reference_contrariness)
        self.assertEqual(set(aspic_result["kbPrefs"]), reference_kbPrefs)
        self.assertEqual(set(aspic_result["rules"]), reference_rules)
        self.assertEqual(set(aspic_result["rulePrefs"]), reference_rulePrefs)


if __name__ == '__main__':
    unittest.main()
