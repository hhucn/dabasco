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

    def is_equivalent_to(self, other):
        if isinstance(other, self.__class__):
            if other == self:
                return True
            if self.operator != other.operator:
                return False
            if len(self.children) != len(other.children):
                return False
            if self.operator == ADFNode.LEAF:
                return self.children == other.children
            for child in self.children:
                if isinstance(child, str) or isinstance(child, int):
                    if child not in other.children:
                        return False
                    continue  # equal string was found, continue outer loop
                if not isinstance(child, self.__class__):
                    return False
                none_equal = True
                for child_other in other.children:
                    if child.is_equivalent_to(child_other):
                        none_equal = False
                        break  # equal subtree was found, continue outer loop
                if none_equal:
                    return False
            return True
        else:
            return False
