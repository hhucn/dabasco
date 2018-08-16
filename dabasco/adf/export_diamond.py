from .adf_node import ADFNode


def export_diamond(adf):
    """
    Create a DIAMOND/YADF/QADF formatted string representation of the given adf.

    :param adf: ADF to be converted
    :type adf: ADF
    :return: DIAMOND/YADF/QADF formatted string representation of the given adf
    """
    output_list = []
    for statement in adf.statements:
        output_list.append('s(' + statement + ').')
        acceptance_condition = diamond_acc_condition_to_string(adf.acceptance[statement])
        output_list.append('ac(' + statement + ',' + acceptance_condition + ').')
    output_string = '\n'.join(output_list)
    return output_string


def diamond_acc_condition_to_string(acc_node):
    """
    Create a DIAMOND/YADF/QADF string representation of the acceptance function represented by the given tree node.

    :param acc_node: root node of acceptance tree
    :type acc_node: ADFNode, string
    :return: string representation
    """
    if not isinstance(acc_node, ADFNode):
        # Current node contains a single value without an operator
        return str(acc_node)
    else:
        if acc_node.operator == ADFNode.LEAF:
            # Current node contains a single value without an operator
            leaf = acc_node.children[0]
            if leaf == ADFNode.CONSTANT_FALSE:
                return 'c(f)'
            elif leaf == ADFNode.CONSTANT_TRUE:
                return 'c(v)'
            else:
                return str(leaf)
        elif acc_node.operator == ADFNode.NOT:
            # Current node contains a 1-ary 'neg' operator
            child = acc_node.children[0]
            return 'neg(' + diamond_acc_condition_to_string(child) + ')'
        else:
            # Current node contains an n-ary 'and' or 'or' operator (arbitrary n=>1)
            operator = 'and' if acc_node.operator == ADFNode.AND else 'or'
            n_children = len(acc_node.children)
            if n_children == 1:
                return diamond_acc_condition_to_string(acc_node.children[0])
            else:
                # Output operators must not have more than 2 arguments. Nest operators as necessary.
                output_string = operator + '(' + diamond_acc_condition_to_string(acc_node.children[n_children-2]) \
                                + ',' + diamond_acc_condition_to_string(acc_node.children[n_children-1]) + ')'
                n_children -= 2
                while n_children > 0:
                    output_string = operator + '(' + diamond_acc_condition_to_string(acc_node.children[n_children-1]) \
                                    + ',' + output_string + ')'
                    n_children -= 1
            return output_string
