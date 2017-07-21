class DBASUser(object):
    """
    Data structure representing a single user opinion data set obtained from D-BAS export

    Attributes:
        discussion_id                   id of the context discussion
        user_id                         id of the user
        accepted_statements_explicit    list of statements explicitly accepted by user
        accepted_statements_implicit    list of statements implicitly accepted by user
        rejected_statements_implicit    list of statements implicitly rejected by user
        accepted_arguments_explicit     list of arguments explicitly accepted by user
        rejected_arguments_explicit     list of arguments explicitly rejected by user
    """

    def __init__(self, discussion_id, user_id):
        self.discussion_id = discussion_id
        self.user_id = user_id

        self.accepted_statements_explicit = []
        self.accepted_statements_implicit = []
        self.rejected_statements_implicit = []

        self.accepted_arguments_explicit = []
        self.rejected_arguments_explicit = []
