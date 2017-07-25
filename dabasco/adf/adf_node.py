class ADFNode(object):
    """
    Data structure that represents a single node in an acceptance condition tree for a statement in an ADF.
    """

    LEAF = 0
    """constant that represents 'leaf' type for nodes."""
    NOT = 1
    """constant that represents unary 'not' type for nodes."""
    AND = 2
    """constant that represents binary 'and' type for nodes."""
    OR = 3
    """constant that represents binary 'or' type for nodes."""

    CONSTANT_FALSE = 0
    """constant representing value 'false'."""
    CONSTANT_TRUE = 1
    """constant representing value 'true'."""

    def __init__(self, node_type, children):
        self.operator = node_type
        """(int) operator of this node (LEAF, NOT, AND, or OR)."""
        if children and type(children) is list:
            self.children = children
            """(list) list of child nodes."""
        else:
            self.children = [children]

