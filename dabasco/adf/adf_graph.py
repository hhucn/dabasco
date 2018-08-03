import logging
logger = logging.getLogger('root')


class ADF(object):
    """
    Abstract Dialectical Framework.
    """

    def __init__(self):
        """
        Create an initially empty ADF.
        """
        self.statements = []
        """(list) list of statements that exist in this ADF"""
        self.acceptance = {}
        """(dict) dict that maps each statement to its acceptance function (root ADFNode)"""

    def add_statement(self, statement, acc_tree):
        """
        Add a statement and corresponding acceptance tree to the ADF.

        :param statement: string identifier of the statement
        :type statement: str
        :param acc_tree: root node of acceptance tree
        :type acc_tree: ADFNode
        """
        if statement in self.statements:
            logging.warning('Add statement %s to ADF: already exists!', str(statement))
        else:
            self.statements.append(statement)
        self.acceptance[statement] = acc_tree

    def is_equivalent_to(self, other):
        if isinstance(other, self.__class__):
            if other == self:
                return True
            if self.statements != other.statements:
                return False
            for statement, acceptance_node in self.acceptance.items():
                print("start checking acc. condition for statement " + str(statement))
                if not acceptance_node.is_equivalent_to(other.acceptance[statement]):
                    return False
            return True
        else:
            return False
