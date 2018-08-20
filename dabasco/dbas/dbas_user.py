class DBASUser(object):
    """
    Data structure representing a single user opinion data set obtained from D-BAS export.

    Attributes:
          discussion_id (int): id of the context discussion.
          user_id (int): id of the user.
          accepted_statements_explicit (set): statements explicitly accepted by user.
          accepted_statements_implicit (set): statements implicitly accepted by user.
          rejected_statements_implicit (set): statements implicitly rejected by user.
          accepted_arguments_explicit (set): arguments explicitly accepted by user.
          rejected_arguments_explicit (set): arguments explicitly rejected by user.
    """

    def __init__(self, discussion_id, user_id):
        self.discussion_id = discussion_id
        self.user_id = user_id

        self.accepted_statements_explicit = set()
        self.accepted_statements_implicit = set()
        self.rejected_statements_implicit = set()

        self.accepted_arguments_explicit = set()
        self.rejected_arguments_explicit = set()
