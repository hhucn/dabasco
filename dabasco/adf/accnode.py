class ADFNode(object):
    """
    Data structure that represents a single node in an acceptance condition tree for a statement in an ADF
    """

    LEAF = 0
    NOT = 1
    AND = 2
    OR = 3

    CONSTANT_FALSE = 0
    CONSTANT_TRUE = 1

    def __init__(self, node_type, children):
        self.operator = node_type
        if children and type(children) is list:
            self.children = children
        else:
            self.children = [children]

