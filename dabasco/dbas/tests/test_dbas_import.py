#!/usr/bin/env python3

import unittest

from dabasco.dbas.dbas_graph import DBASGraph, Inference, Undercut
from dabasco.dbas.dbas_user import DBASUser
from dabasco.dbas.dbas_import import import_dbas_user, import_dbas_graph, import_dbas_user_v2, import_dbas_graph_v2

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestASPICExport(unittest.TestCase):

    def test_discussion1_apiv2(self):
        """Small discussion without undercut (Using API v2)."""
        discussion_id = 1

        dbas_statements_json = {
            "issue": {
                "statements": [
                    {"uid": 1},
                    {"uid": 2},
                    {"uid": 3},
                ]
            }
        }
        dbas_arguments_json = {
            "issue": {
                "arguments": [
                    {
                        "uid": 1,
                        "isSupportive": True,
                        "conclusionUid": 1,
                        "argumentUid": None,
                        "premisegroup": {
                            "premises": [
                                {"statementUid": 2}
                            ]
                        }
                    },
                    {
                        "uid": 2,
                        "isSupportive": False,
                        "conclusionUid": 1,
                        "argumentUid": None,
                        "premisegroup": {
                            "premises": [
                                {"statementUid": 3}
                            ]
                        }
                    },
                ]
            }
        }

        dbas_discussion = import_dbas_graph_v2(discussion_id, dbas_statements_json, dbas_arguments_json)

        dbas_discussion_reference = DBASGraph(discussion_id=discussion_id)
        dbas_discussion_reference.statements = {1, 2, 3}
        dbas_discussion_reference.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion_reference.undercuts = dict()

        self.assertTrue(dbas_discussion_reference.is_equivalent_to(dbas_discussion))

    def test_discussion2_apiv2(self):
        """Bigger discussion with undercut (Using API v2)"""
        discussion_id = 2

        dbas_statements_json = {
            "issue": {
                "statements": [
                    {"uid": 1},
                    {"uid": 2},
                    {"uid": 3},
                    {"uid": 4},
                    {"uid": 5},
                ]
            }
        }
        dbas_arguments_json = {
            "issue": {
                "arguments": [
                    {
                        "uid": 1,
                        "isSupportive": True,
                        "conclusionUid": 1,
                        "argumentUid": None,
                        "premisegroup": {
                            "premises": [
                                {"statementUid": 2}
                            ]
                        }
                    },
                    {
                        "uid": 2,
                        "isSupportive": False,
                        "conclusionUid": 1,
                        "argumentUid": None,
                        "premisegroup": {
                            "premises": [
                                {"statementUid": 3}
                            ]
                        }
                    },
                    {
                        "uid": 3,
                        "isSupportive": False,
                        "conclusionUid": 2,
                        "argumentUid": None,
                        "premisegroup": {
                            "premises": [
                                {"statementUid": 4}
                            ]
                        }
                    },
                    {
                        "uid": 4,
                        "conclusionUid": None,
                        "argumentUid": 2,
                        "premisegroup": {
                            "premises": [
                                {"statementUid": 5}
                            ]
                        }
                    },
                ]
            }
        }

        dbas_discussion = import_dbas_graph_v2(discussion_id, dbas_statements_json, dbas_arguments_json)

        dbas_discussion_reference = DBASGraph(discussion_id=discussion_id)
        dbas_discussion_reference.statements = {1, 2, 3, 4, 5}
        dbas_discussion_reference.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion_reference.undercuts = {
            4: Undercut(4, [5], 2)
        }

        self.assertTrue(dbas_discussion_reference.is_equivalent_to(dbas_discussion))

    def test_discussion1_user1_apiv2(self):
        discussion_id = 1
        user_id = 1

        dbas_user_json = {
            "user": {
                "clickedStatements": [
                    {"uid": 2, "isUpvote": True},
                    {"uid": 3, "isUpvote": False},
                ]
            }
        }

        dbas_user = import_dbas_user_v2(discussion_id=discussion_id, user_id=user_id, user_json=dbas_user_json)

        dbas_user_reference = DBASUser(discussion_id=discussion_id, user_id=user_id)
        dbas_user_reference.accepted_statements_explicit = {2}
        dbas_user_reference.accepted_statements_implicit = set()
        dbas_user_reference.rejected_statements_explicit = {3}
        dbas_user_reference.rejected_statements_implicit = set()
        dbas_user_reference.accepted_arguments_explicit = set()
        dbas_user_reference.rejected_arguments_explicit = set()

        self.assertTrue(dbas_user_reference.is_equivalent_to(dbas_user))

    def test_discussion2_user2_apiv2(self):
        discussion_id = 2
        user_id = 2

        dbas_user_json = {
            "user": {
                "clickedStatements": [
                    {"uid": 3, "isUpvote": True},
                    {"uid": 4, "isUpvote": True},
                    {"uid": 5, "isUpvote": False},
                ]
            }
        }

        dbas_user = import_dbas_user_v2(discussion_id=discussion_id, user_id=user_id, user_json=dbas_user_json)

        dbas_user_reference = DBASUser(discussion_id=discussion_id, user_id=user_id)
        dbas_user_reference.accepted_statements_explicit = {3, 4}
        dbas_user_reference.accepted_statements_implicit = set()
        dbas_user_reference.rejected_statements_explicit = {5}
        dbas_user_reference.rejected_statements_implicit = set()
        dbas_user_reference.accepted_arguments_explicit = set()
        dbas_user_reference.rejected_arguments_explicit = set()

        self.assertTrue(dbas_user_reference.is_equivalent_to(dbas_user))

    def test_discussion1(self):
        """Small discussion without undercut."""
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

        dbas_discussion_reference = DBASGraph(discussion_id=discussion_id)
        dbas_discussion_reference.statements = {1, 2, 3}
        dbas_discussion_reference.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion_reference.undercuts = dict()

        self.assertTrue(dbas_discussion_reference.is_equivalent_to(dbas_discussion))

    def test_discussion2(self):
        """Bigger discussion with undercut."""
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

        dbas_discussion_reference = DBASGraph(discussion_id=discussion_id)
        dbas_discussion_reference.statements = {1, 2, 3, 4, 5}
        dbas_discussion_reference.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion_reference.undercuts = {
            4: Undercut(4, [5], 2)
        }

        self.assertTrue(dbas_discussion_reference.is_equivalent_to(dbas_discussion))

    def test_discussion3(self):
        """Small discussion without redundant Statements."""
        discussion_id = 3

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]}
            ],
            "nodes": [1, 2, 3, 4, 1],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        dbas_discussion_reference = DBASGraph(discussion_id=discussion_id)
        dbas_discussion_reference.statements = {1, 2, 3}
        dbas_discussion_reference.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
        }
        dbas_discussion_reference.undercuts = dict()

        self.assertTrue(dbas_discussion_reference.is_equivalent_to(dbas_discussion))

    def test_discussion4(self):
        """Bigger discussion without redundant Statements."""
        discussion_id = 4

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 1, "id": 2, "is_supportive": False, "premises": [3]},
                {"conclusion": 2, "id": 3, "is_supportive": False, "premises": [4]}
            ],
            "nodes": [1, 2, 3, 4, 5, 6, 1],
            "undercuts": [
                {"conclusion": 2, "id": 4, "premises": [5]}
            ]
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)

        dbas_discussion_reference = DBASGraph(discussion_id=discussion_id)
        dbas_discussion_reference.statements = {1, 2, 3, 4, 5}
        dbas_discussion_reference.inferences = {
            1: Inference(1, [2], 1, True),
            2: Inference(2, [3], 1, False),
            3: Inference(3, [4], 2, False)
        }
        dbas_discussion_reference.undercuts = {
            4: Undercut(4, [5], 2)
        }

        self.assertTrue(dbas_discussion_reference.is_equivalent_to(dbas_discussion))

    def test_discussion1_user1(self):
        discussion_id = 1
        user_id = 1

        dbas_user_json = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [3],
        }

        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        dbas_user_reference = DBASUser(discussion_id=discussion_id, user_id=user_id)
        dbas_user_reference.accepted_statements_explicit = set()
        dbas_user_reference.accepted_statements_implicit = {2}
        dbas_user_reference.rejected_statements_implicit = {3}
        dbas_user_reference.accepted_arguments_explicit = set()
        dbas_user_reference.rejected_arguments_explicit = set()

        self.assertTrue(dbas_user_reference.is_equivalent_to(dbas_user))

    def test_discussion2_user2(self):
        discussion_id = 2
        user_id = 2

        dbas_user_json = {
            "accepted_statements_via_click": [3],
            "marked_arguments": [],
            "marked_statements": [4],
            "rejected_arguments": [],
            "rejected_statements_via_click": [5],
        }

        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)

        dbas_user_reference = DBASUser(discussion_id=discussion_id, user_id=user_id)
        dbas_user_reference.accepted_statements_explicit = {4}
        dbas_user_reference.accepted_statements_implicit = {3}
        dbas_user_reference.rejected_statements_implicit = {5}
        dbas_user_reference.accepted_arguments_explicit = set()
        dbas_user_reference.rejected_arguments_explicit = set()

        self.assertTrue(dbas_user_reference.is_equivalent_to(dbas_user))


if __name__ == '__main__':
    unittest.main()
