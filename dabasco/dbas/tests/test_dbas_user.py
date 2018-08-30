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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

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
        user2.rejected_statements_explicit = {6}

        self.assertFalse(user1.is_equivalent_to(user2))

    def test_accepted_args_both_empty(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = set()
        user.accepted_statements_implicit = set()
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_accepted_statements()

        reference = set()

        self.assertEquals(result, reference)

    def test_accepted_args_only_explicit(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = set()
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_accepted_statements()

        reference = {1}

        self.assertEquals(result, reference)

    def test_accepted_args_only_implicit(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = set()
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_accepted_statements()

        reference = {2}

        self.assertEquals(result, reference)

    def test_accepted_args_both(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_accepted_statements()

        reference = {1, 2}

        self.assertEquals(result, reference)

    def test_accepted_args_both_identical(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1, 99}
        user.accepted_statements_implicit = {2, 99}
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_accepted_statements()

        reference = {1, 2, 99}

        self.assertEquals(result, reference)

    def test_rejected_args_both_empty(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = set()
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = set()
        result = user.get_rejected_statements()

        reference = set()

        self.assertEquals(result, reference)

    def test_rejected_args_only_explicit(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = set()
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_rejected_statements()

        reference = {6}

        self.assertEquals(result, reference)

    def test_rejected_args_only_implicit(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = set()
        result = user.get_rejected_statements()

        reference = {3}

        self.assertEquals(result, reference)

    def test_rejected_args_both(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = {3}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result = user.get_rejected_statements()

        reference = {3, 6}

        self.assertEquals(result, reference)

    def test_rejected_args_both_identical(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2}
        user.rejected_statements_implicit = {99}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {99}
        result = user.get_rejected_statements()

        reference = {99}

        self.assertEquals(result, reference)

    def test_accepted_and_rejected_args_conflict_canceled_out1(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1, 99}
        user.accepted_statements_implicit = {2, 999}
        user.rejected_statements_implicit = {3, 999}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6, 99}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2}
        reference_rejected = {3, 6}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)

    def test_accepted_and_rejected_args_conflict_canceled_out2(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1, 99}
        user.accepted_statements_implicit = {2, 999}
        user.rejected_statements_implicit = {3, 999}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2, 99}
        reference_rejected = {3, 6}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)

    def test_accepted_and_rejected_args_conflict_canceled_out3(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2, 999}
        user.rejected_statements_implicit = {3, 999}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6, 99}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2}
        reference_rejected = {3, 6, 99}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)

    def test_accepted_and_rejected_args_conflict_canceled_out4(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1}
        user.accepted_statements_implicit = {2, 999}
        user.rejected_statements_implicit = {3, 999}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2}
        reference_rejected = {3, 6}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)

    def test_accepted_and_rejected_args_conflict_overruled1(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1, 99}
        user.accepted_statements_implicit = {2, 999}
        user.rejected_statements_implicit = {3, 99}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6, 999}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2, 99}
        reference_rejected = {3, 6, 999}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)

    def test_accepted_and_rejected_args_conflict_overruled2(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1, 99}
        user.accepted_statements_implicit = {2, 999}
        user.rejected_statements_implicit = {3, 999}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6, 999}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2, 99}
        reference_rejected = {3, 6, 999}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)

    def test_accepted_and_rejected_args_conflict_overruled3(self):
        user = DBASUser(discussion_id=1, user_id=1)
        user.accepted_statements_explicit = {1, 99}
        user.accepted_statements_implicit = {2, 99}
        user.rejected_statements_implicit = {3, 99}
        user.accepted_arguments_explicit = {4}
        user.rejected_arguments_explicit = {5}
        user.rejected_statements_explicit = {6, 999}
        result_accepted = user.get_accepted_statements()
        result_rejected = user.get_rejected_statements()

        reference_accepted = {1, 2, 99}
        reference_rejected = {3, 6, 999}

        self.assertEquals(result_accepted, reference_accepted)
        self.assertEquals(result_rejected, reference_rejected)


if __name__ == '__main__':
    unittest.main()
