#!/usr/bin/env python3

import unittest

from dabasco.dbas.dbas_user import DBASUser

from os import path
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('test')


class TestASPICExport(unittest.TestCase):

    def test_equivalence_true(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=1)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertTrue(user1.is_equivalent_to(user2))

    def test_equivalence_empty_default(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = set()
        user1.accepted_statements_implicit = set()
        user1.rejected_statements_implicit = set()
        user1.accepted_arguments_explicit = set()
        user1.rejected_arguments_explicit = set()
        user1.rejected_statements_explicit = set()

        user2 = DBASUser(discussion_id=1, user_id=1)

        self.assertTrue(user1.is_equivalent_to(user2))

    def test_equivalence_wrong_type(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = set()

        user2 = {
            "accepted_statements_via_click": [2],
            "marked_arguments": [4],
            "marked_statements": [1],
            "rejected_arguments": [5],
            "rejected_statements_via_click": [3],
        }

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_wrong_discussionID(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=2, user_id=1)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_wrong_userID(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=2)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_different_accepted_explicit(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=1)
        user2.accepted_statements_explicit = {99}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_different_accepted_implicit(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=1)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {99}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_different_rejected_implicit(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=1)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {99}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_different_accepted_args(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=1)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {99}
        user2.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_equivalence_different_rejected_args(self):
        user1 = DBASUser(discussion_id=1, user_id=1)
        user1.accepted_statements_explicit = {1}
        user1.accepted_statements_implicit = {2}
        user1.rejected_statements_implicit = {3}
        user1.accepted_arguments_explicit = {4}
        user1.rejected_arguments_explicit = {5}
        user1.rejected_statements_explicit = {6}

        user2 = DBASUser(discussion_id=1, user_id=1)
        user2.accepted_statements_explicit = {1}
        user2.accepted_statements_implicit = {2}
        user2.rejected_statements_implicit = {3}
        user2.accepted_arguments_explicit = {4}
        user2.rejected_arguments_explicit = {99}
        user1.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))


if __name__ == '__main__':
    unittest.main()
