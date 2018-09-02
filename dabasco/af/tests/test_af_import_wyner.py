#!/usr/bin/env python3

import unittest

from dabasco.config import *
from dabasco.af.af_graph import AF
from dabasco.af.import_wyner import import_af_wyner
from dabasco.dbas.dbas_import import import_dbas_graph, import_dbas_user

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestAFImport(unittest.TestCase):

    def test_discussion1_no_user(self):
        discussion_id = 1

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        af_result = import_af_wyner(dbas_discussion, opinion=None, opinion_strict=False)

        af_reference = AF(8)
        arg_1 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '1')
        arg_neg1 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '1')
        arg_2 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '2')
        arg_neg2 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '2')
        arg_3 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '3')
        arg_neg3 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '3')
        arg_r1 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '1')
        arg_r2 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '2')

        # Attacks between statement args
        af_reference.set_attack(arg_1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_3, AF.DEFINITE_ATTACK)

        # Undermining attacks by negated premises
        af_reference.set_attack(arg_neg2, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_r2, AF.DEFINITE_ATTACK)

        # Rebutting attacks between rules and negated conclusions
        af_reference.set_attack(arg_r1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_1, arg_r2, AF.DEFINITE_ATTACK)

        self.assertTrue(af_reference.is_equivalent_to(af_result))

    def test_discussion2_no_user(self):
        discussion_id = 2

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

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        af_result = import_af_wyner(dbas_discussion, opinion=None, opinion_strict=False)

        af_reference = AF(14)
        arg_1 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '1')
        arg_neg1 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '1')
        arg_2 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '2')
        arg_neg2 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '2')
        arg_3 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '3')
        arg_neg3 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '3')
        arg_4 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '4')
        arg_neg4 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '4')
        arg_5 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '5')
        arg_neg5 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '5')
        arg_r1 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '1')
        arg_r2 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '2')
        arg_r3 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '3')
        arg_r4 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '4')

        # Attacks between statement args
        af_reference.set_attack(arg_1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_4, arg_neg4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_5, arg_neg5, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg5, arg_5, AF.DEFINITE_ATTACK)

        # Undermining attacks by negated premises
        af_reference.set_attack(arg_neg2, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_r3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg5, arg_r4, AF.DEFINITE_ATTACK)

        # Rebutting attacks between rules and negated conclusions
        af_reference.set_attack(arg_r1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_1, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r3, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_r3, AF.DEFINITE_ATTACK)

        # Undercutting attacks
        af_reference.set_attack(arg_r4, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_r4, AF.DEFINITE_ATTACK)

        self.assertTrue(af_reference.is_equivalent_to(af_result))

    def test_discussion1_user1_weak_opinion(self):
        discussion_id = 1
        user_id = 1
        assumptions_strict = False

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
        af_result = import_af_wyner(dbas_discussion, opinion=dbas_user, opinion_strict=assumptions_strict)

        af_reference = AF(10)
        arg_1 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '1')
        arg_neg1 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '1')
        arg_2 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '2')
        arg_neg2 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '2')
        arg_3 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '3')
        arg_neg3 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '3')
        arg_r1 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '1')
        arg_r2 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '2')
        arg_u2 = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION + '_' + '2')
        arg_uneg3 = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION + '_' + LITERAL_PREFIX_NOT + '3')

        # Attacks between statement args
        af_reference.set_attack(arg_1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_3, AF.DEFINITE_ATTACK)

        # Undermining attacks by negated premises
        af_reference.set_attack(arg_neg2, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_r2, AF.DEFINITE_ATTACK)

        # Rebutting attacks between rules and negated conclusions
        af_reference.set_attack(arg_r1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_1, arg_r2, AF.DEFINITE_ATTACK)

        # Attacks between user opinion args and negated statements
        af_reference.set_attack(arg_u2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_u2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_uneg3, arg_3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_uneg3, AF.DEFINITE_ATTACK)

        self.assertTrue(af_reference.is_equivalent_to(af_result))

    def test_discussion2_user2_weak_opinion(self):
        discussion_id = 2
        user_id = 2
        assumptions_strict = False

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
        af_result = import_af_wyner(dbas_discussion, opinion=dbas_user, opinion_strict=assumptions_strict)

        af_reference = AF(17)
        arg_1 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '1')
        arg_neg1 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '1')
        arg_2 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '2')
        arg_neg2 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '2')
        arg_3 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '3')
        arg_neg3 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '3')
        arg_4 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '4')
        arg_neg4 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '4')
        arg_5 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '5')
        arg_neg5 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '5')
        arg_r1 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '1')
        arg_r2 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '2')
        arg_r3 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '3')
        arg_r4 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '4')
        arg_u3 = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION + '_' + '3')
        arg_u4 = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION + '_' + '4')
        arg_uneg5 = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION + '_' + LITERAL_PREFIX_NOT + '5')

        # Attacks between statement args
        af_reference.set_attack(arg_1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_4, arg_neg4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_5, arg_neg5, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg5, arg_5, AF.DEFINITE_ATTACK)

        # Undermining attacks by negated premises
        af_reference.set_attack(arg_neg2, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_r3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg5, arg_r4, AF.DEFINITE_ATTACK)

        # Rebutting attacks between rules and negated conclusions
        af_reference.set_attack(arg_r1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_1, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r3, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_r3, AF.DEFINITE_ATTACK)

        # Undercutting attacks
        af_reference.set_attack(arg_r4, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_r4, AF.DEFINITE_ATTACK)

        # Attacks between user opinion args and negated statements
        af_reference.set_attack(arg_u3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_u3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_u4, arg_neg4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_u4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_uneg5, arg_5, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_5, arg_uneg5, AF.DEFINITE_ATTACK)

        self.assertTrue(af_reference.is_equivalent_to(af_result))

    def test_discussion1_user1_strict_opinion(self):
        discussion_id = 1
        user_id = 1
        assumptions_strict = True

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
        af_result = import_af_wyner(dbas_discussion, opinion=dbas_user, opinion_strict=assumptions_strict)

        af_reference = AF(9)
        arg_1 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '1')
        arg_neg1 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '1')
        arg_2 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '2')
        arg_neg2 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '2')
        arg_3 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '3')
        arg_neg3 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '3')
        arg_r1 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '1')
        arg_r2 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '2')
        arg_u = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION)

        # Attacks between statement args
        af_reference.set_attack(arg_1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_3, AF.DEFINITE_ATTACK)

        # Undermining attacks by negated premises
        af_reference.set_attack(arg_neg2, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_r2, AF.DEFINITE_ATTACK)

        # Rebutting attacks between rules and negated conclusions
        af_reference.set_attack(arg_r1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_1, arg_r2, AF.DEFINITE_ATTACK)

        # Attacks from user opinion arg to negated statements
        af_reference.set_attack(arg_u, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_u, arg_3, AF.DEFINITE_ATTACK)

        self.assertTrue(af_reference.is_equivalent_to(af_result))

    def test_discussion2_user2_strict_opinion(self):
        discussion_id = 2
        user_id = 2
        assumptions_strict = True

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
        af_result = import_af_wyner(dbas_discussion, opinion=dbas_user, opinion_strict=assumptions_strict)

        af_reference = AF(15)
        arg_1 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '1')
        arg_neg1 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '1')
        arg_2 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '2')
        arg_neg2 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '2')
        arg_3 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '3')
        arg_neg3 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '3')
        arg_4 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '4')
        arg_neg4 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '4')
        arg_5 = af_result.get_argument_for_name(LITERAL_PREFIX_STATEMENT + '5')
        arg_neg5 = af_result.get_argument_for_name(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + '5')
        arg_r1 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '1')
        arg_r2 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '2')
        arg_r3 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '3')
        arg_r4 = af_result.get_argument_for_name(LITERAL_PREFIX_INFERENCE_RULE + '4')
        arg_u = af_result.get_argument_for_name(DUMMY_LITERAL_NAME_OPINION)

        # Attacks between statement args
        af_reference.set_attack(arg_1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_neg2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg2, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_3, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_4, arg_neg4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_5, arg_neg5, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg5, arg_5, AF.DEFINITE_ATTACK)

        # Undermining attacks by negated premises
        af_reference.set_attack(arg_neg2, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg3, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg4, arg_r3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg5, arg_r4, AF.DEFINITE_ATTACK)

        # Rebutting attacks between rules and negated conclusions
        af_reference.set_attack(arg_r1, arg_neg1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_neg1, arg_r1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_1, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_1, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r3, arg_2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_2, arg_r3, AF.DEFINITE_ATTACK)

        # Undercutting attacks
        af_reference.set_attack(arg_r4, arg_r2, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_r2, arg_r4, AF.DEFINITE_ATTACK)

        # Attacks between user opinion args and negated statements
        af_reference.set_attack(arg_u, arg_neg3, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_u, arg_neg4, AF.DEFINITE_ATTACK)
        af_reference.set_attack(arg_u, arg_5, AF.DEFINITE_ATTACK)

        self.assertTrue(af_reference.is_equivalent_to(af_result))


if __name__ == '__main__':
    unittest.main()
