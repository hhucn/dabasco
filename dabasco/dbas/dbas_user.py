class DBASUser(object):
    """
    Data structure representing a single user opinion data set obtained from D-BAS export.

    Attributes:
          discussion_id (int): id of the context discussion.
          user_id (int): id of the user.
          accepted_statements_explicit (set): statements explicitly accepted by user.
          rejected_statements_explicit (set): statements explicitly rejected by user.
          accepted_statements_implicit (set): statements implicitly accepted by user.
          rejected_statements_implicit (set): statements implicitly rejected by user.
          accepted_arguments_explicit (set): arguments explicitly accepted by user.
          rejected_arguments_explicit (set): arguments explicitly rejected by user.
    """

    def __init__(self, discussion_id, user_id):
        self.discussion_id = discussion_id
        self.user_id = user_id

        self.accepted_statements_explicit = set()
        self.rejected_statements_explicit = set()
        self.accepted_statements_implicit = set()
        self.rejected_statements_implicit = set()

        self.accepted_arguments_explicit = set()
        self.rejected_arguments_explicit = set()

    def get_accepted_statements(self):
        # Accept all explicitly accepted statements, if NOT expl. rejected
        # Accept all implicitly accepted statements, if NOT impl./expl. rejected
        return (self.accepted_statements_explicit.difference(self.rejected_statements_explicit) |
                self.accepted_statements_implicit.difference(self.rejected_statements_explicit |
                                                             self.rejected_statements_implicit))

    def get_rejected_statements(self):
        # Reject all explicitly rejected statements, if NOT expl. accepted
        # Reject all implicitly rejected statements, if NOT impl./expl. rejected
        return (self.rejected_statements_explicit.difference(self.accepted_statements_explicit) |
                self.rejected_statements_implicit.difference(self.accepted_statements_explicit |
                                                             self.accepted_statements_implicit))

    def is_equivalent_to(self, other):
        """
        Check equivalence of two DBAS user data structures.

        :param other: DBASUser to compare this DBASUser with.
        :type other: DBASUser
        :return: bool
        """
        if not isinstance(other, self.__class__):
            return False
        if self.discussion_id != other.discussion_id:
            return False
        if self.user_id != other.user_id:
            return False
        if self.accepted_statements_explicit != other.accepted_statements_explicit:
            return False
        if self.rejected_statements_explicit != other.rejected_statements_explicit:
            return False
        if self.accepted_statements_implicit != other.accepted_statements_implicit:
            return False
        if self.rejected_statements_implicit != other.rejected_statements_implicit:
            return False
        if self.accepted_arguments_explicit != other.accepted_arguments_explicit:
            return False
        if self.rejected_arguments_explicit != other.rejected_arguments_explicit:
            return False
        return True
