#!/usr/bin/env python3

import unittest

from dabasco.adf.adf_graph import ADF
from dabasco.adf.adf_node import ADFNode
from dabasco.adf.import_strass import import_adf
from dabasco.dbas.dbas_import import import_dbas_graph, import_dbas_user

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestADFImport(unittest.TestCase):

    def test_discussion1_objective(self):
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
        adf_result = import_adf(dbas_discussion, None, False)

        adf_reference = ADF()

        # D-BAS Statements
        adf_reference.add_statement('s1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i1'))
        ]))
        adf_reference.add_statement('ns1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i2'))
        ]))
        adf_reference.add_statement('s2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        # D-BAS Inferences
        adf_reference.add_statement('i1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni1')),
            ADFNode(ADFNode.LEAF, 's2')
        ]))
        adf_reference.add_statement('ni1', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i1')))
        adf_reference.add_statement('i2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni2')),
            ADFNode(ADFNode.LEAF, 's3')
        ]))
        adf_reference.add_statement('ni2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')))

        self.assertTrue(adf_reference.is_equivalent_to(adf_result))

    def test_discussion1_user1_defeasible(self):
        discussion_id = 1
        user_id = 1
        strict_opinion = False

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
        adf_result = import_adf(dbas_discussion, dbas_user, strict_opinion)

        adf_reference = ADF()

        # D-BAS Statements
        adf_reference.add_statement('s1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i1'))
        ]))
        adf_reference.add_statement('ns1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i2'))
        ]))
        adf_reference.add_statement('s2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns2')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ua2'))
        ]))
        adf_reference.add_statement('ns2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's3')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ur3'))
        ]))

        # User opinion
        adf_reference.add_statement('ua2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nua2'))
        ]))
        adf_reference.add_statement('nua2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ua2')))
        adf_reference.add_statement('ur3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's3')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nur3'))
        ]))
        adf_reference.add_statement('nur3', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ur3')))

        # D-BAS Inferences
        adf_reference.add_statement('i1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni1')),
            ADFNode(ADFNode.LEAF, 's2')
        ]))
        adf_reference.add_statement('ni1', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i1')))
        adf_reference.add_statement('i2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni2')),
            ADFNode(ADFNode.LEAF, 's3')
        ]))
        adf_reference.add_statement('ni2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')))

        self.assertTrue(adf_reference.is_equivalent_to(adf_result))

    def test_discussion1_user1_strict(self):
        discussion_id = 1
        user_id = 1
        strict_opinion = True

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
        adf_result = import_adf(dbas_discussion, dbas_user, strict_opinion)

        adf_reference = ADF()

        # D-BAS Statements
        adf_reference.add_statement('s1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i1'))
        ]))
        adf_reference.add_statement('ns1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i2'))
        ]))
        adf_reference.add_statement('s2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns2')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ua2'))
        ]))
        adf_reference.add_statement('ns2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's3')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ur3'))
        ]))

        # User opinion
        adf_reference.add_statement('ua2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf_reference.add_statement('nua2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nua2'))
        ]))
        adf_reference.add_statement('ur3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
        adf_reference.add_statement('nur3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns3')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nur3'))
        ]))

        # D-BAS Inferences
        adf_reference.add_statement('i1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni1')),
            ADFNode(ADFNode.LEAF, 's2')
        ]))
        adf_reference.add_statement('ni1', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i1')))
        adf_reference.add_statement('i2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni2')),
            ADFNode(ADFNode.LEAF, 's3')
        ]))
        adf_reference.add_statement('ni2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')))

        self.assertTrue(adf_reference.is_equivalent_to(adf_result))

    def test_discussion2_objective(self):
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
        adf_result = import_adf(dbas_discussion, None, False)

        adf_reference = ADF()

        # D-BAS Statements
        adf_reference.add_statement('s1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i1'))
        ]))
        adf_reference.add_statement('ns1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i2'))
        ]))
        adf_reference.add_statement('s2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's2')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i3'))
        ]))
        adf_reference.add_statement('s3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s4', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns4', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s5', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns5', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        # D-BAS Inferences
        adf_reference.add_statement('i1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni1')),
            ADFNode(ADFNode.LEAF, 's2')]))
        adf_reference.add_statement('ni1', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i1')))
        adf_reference.add_statement('i2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i4')),
            ADFNode(ADFNode.LEAF, 's3')]))
        adf_reference.add_statement('ni2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')))
        adf_reference.add_statement('i3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni3')),
            ADFNode(ADFNode.LEAF, 's4')]))
        adf_reference.add_statement('ni3', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i3')))
        adf_reference.add_statement('i4', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni4')),
            ADFNode(ADFNode.LEAF, 's5')]))
        adf_reference.add_statement('ni4', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i4')))

        self.assertTrue(adf_reference.is_equivalent_to(adf_result))

    def test_discussion2_user1_defeasible(self):
        discussion_id = 2
        user_id = 1
        strict_opinion = False

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
            "accepted_statements_via_click": [3, 4],
            "marked_arguments": [],
            "marked_statements": [],
            "rejected_arguments": [],
            "rejected_statements_via_click": [5],
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        dbas_user = import_dbas_user(discussion_id=discussion_id, user_id=user_id, user_export=dbas_user_json)
        adf_result = import_adf(dbas_discussion, dbas_user, strict_opinion)

        adf_reference = ADF()

        # D-BAS Statements
        adf_reference.add_statement('s1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i1'))
        ]))
        adf_reference.add_statement('ns1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i2'))
        ]))
        adf_reference.add_statement('s2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's2')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i3'))
        ]))
        adf_reference.add_statement('s3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns3')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ua3'))
        ]))
        adf_reference.add_statement('ns3', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s4', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns4')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ua4'))
        ]))
        adf_reference.add_statement('ns4', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s5', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('ns5', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's5')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'ur5'))
        ]))

        # User opinion
        adf_reference.add_statement('ua3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns3')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nua3'))]))
        adf_reference.add_statement('nua3', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ua3')))
        adf_reference.add_statement('ua4', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns4')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nua4'))]))
        adf_reference.add_statement('nua4', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ua4')))
        adf_reference.add_statement('ur5', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's5')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'nur5'))]))
        adf_reference.add_statement('nur5', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ur5')))

        # D-BAS Inferences
        adf_reference.add_statement('i1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni1')),
            ADFNode(ADFNode.LEAF, 's2')]))
        adf_reference.add_statement('ni1', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i1')))
        adf_reference.add_statement('i2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i4')),
            ADFNode(ADFNode.LEAF, 's3')]))
        adf_reference.add_statement('ni2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')))
        adf_reference.add_statement('i3', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 's2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni3')),
            ADFNode(ADFNode.LEAF, 's4')]))
        adf_reference.add_statement('ni3', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i3')))
        adf_reference.add_statement('i4', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni4')),
            ADFNode(ADFNode.LEAF, 's5')]))
        adf_reference.add_statement('ni4', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i4')))

        self.assertTrue(adf_reference.is_equivalent_to(adf_result))

    def test_discussion3_objective(self):
        discussion_id = 3

        dbas_discussion_json = {
            "inferences": [
                {"conclusion": 1, "id": 1, "is_supportive": True, "premises": [2]},
                {"conclusion": 2, "id": 2, "is_supportive": True, "premises": [1]}
            ],
            "nodes": [1, 2],
            "undercuts": []
        }

        dbas_discussion = import_dbas_graph(discussion_id=discussion_id, graph_export=dbas_discussion_json)
        adf_result = import_adf(dbas_discussion, None, False)

        adf_reference = ADF()

        # D-BAS Statements
        adf_reference.add_statement('s1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i1'))
        ]))
        adf_reference.add_statement('ns1', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        adf_reference.add_statement('s2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns2')),
            ADFNode(ADFNode.OR, ADFNode(ADFNode.LEAF, 'i2'))
        ]))
        adf_reference.add_statement('ns2', ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))

        # D-BAS Inferences
        adf_reference.add_statement('i1', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns1')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni1')),
            ADFNode(ADFNode.LEAF, 's2')
        ]))
        adf_reference.add_statement('ni1', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i1')))
        adf_reference.add_statement('i2', ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ns2')),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'ni2')),
            ADFNode(ADFNode.LEAF, 's1')
        ]))
        adf_reference.add_statement('ni2', ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, 'i2')))

        self.assertTrue(adf_reference.is_equivalent_to(adf_result))


if __name__ == '__main__':
    unittest.main()
