from .adf_graph import ADF
from .adf_node import ADFNode


def import_adf(dbas_graph, user_opinion, rules_strict, assumptions_strict):
    """
    Create an ADF representation for given user's opinion in the given discussion.

    :param dbas_graph: DBASGraph to be used for ADF generation
    :type dbas_graph: DBASGraph
    :param user_opinion: DBASUser to be used for ADF generation
    :type user_opinion: DBASUser
    :param rules_strict: indicate whether rules shall be implemented as strict or defeasible
    :type rules_strict: Boolean
    :param assumptions_strict: indicate whether assumptions shall be implemented as strict or defeasible
    :type assumptions_strict: Boolean
    :return: ADF
    """
    adf = ADF()

    # Get accepted/rejected statements from opinion
    user_rejected_statements = user_opinion.rejected_statements_implicit
    user_accepted_statements = user_opinion.accepted_statements_explicit \
        + user_opinion.accepted_statements_implicit

    # Setup statement acceptance functions
    for statement in dbas_graph.statements:
        inferences_for = []
        inferences_against = []
        for inference_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference_id]
            if inference.conclusion == statement:
                if inference.is_supportive:
                    inferences_for.append(inference)
                else:
                    inferences_against.append(inference)
        statement_assumed = statement in user_accepted_statements
        statement_rejected = statement in user_rejected_statements

        # Acceptance condition for the positive (non-negated) literal
        if not inferences_for and not statement_assumed:
            adf.add_statement('s' + str(statement), ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_FALSE]))
        else:
            acceptance_criteria = ['i' + str(inference.id) for inference in inferences_for]
            if statement_assumed:
                acceptance_criteria.append('a' + str(statement))
            adf.add_statement('s' + str(statement), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['ns' + str(statement)]),
                ADFNode(ADFNode.OR, acceptance_criteria)
            ]))

        # Acceptance condition for the negative (negated) literal
        if not inferences_against and not statement_rejected:
            adf.add_statement('ns' + str(statement), ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_FALSE]))
        else:
            acceptance_criteria = ['i' + str(inference.id) for inference in inferences_against]
            if statement_rejected:
                acceptance_criteria.append('a' + str(statement))
            adf.add_statement('ns' + str(statement), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['s' + str(statement)]),
                ADFNode(ADFNode.OR, acceptance_criteria)
            ]))

    if assumptions_strict:
        # Setup strict user assumption acceptance functions
        for assumption in user_accepted_statements:
            adf.add_statement('a' + str(assumption), ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
            adf.add_statement('na' + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['s' + str(assumption)]),
                ADFNode(ADFNode.NOT, ['na' + str(assumption)])
            ]))
        for assumption in user_rejected_statements:
            adf.add_statement('a' + str(assumption), ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_TRUE]))
            adf.add_statement('na' + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['ns' + str(assumption)]),
                ADFNode(ADFNode.NOT, ['na' + str(assumption)])
            ]))
    else:
        # Setup defeasible user assumption acceptance functions
        for assumption in user_accepted_statements:
            adf.add_statement('a' + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['ns' + str(assumption)]),
                ADFNode(ADFNode.NOT, ['na' + str(assumption)])
            ]))
            adf.add_statement('na' + str(assumption), ADFNode(ADFNode.NOT, ['a' + str(assumption)]))
        for assumption in user_rejected_statements:
            adf.add_statement('a' + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['s' + str(assumption)]),
                ADFNode(ADFNode.NOT, ['na' + str(assumption)])
            ]))
            adf.add_statement('na' + str(assumption), ADFNode(ADFNode.NOT, ['a' + str(assumption)]))

    if rules_strict:
        # Setup strict inference acceptance functions
        for inference_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference_id]
            premises = ['s' + str(premise) for premise in inference.premises]
            conclusion = 's' + str(inference.conclusion) if inference.is_supportive \
                else 'ns' + str(inference.conclusion)
            rule_name = 'i' + str(inference.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, conclusion),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
        for undercut_id in dbas_graph.undercuts:
            undercut = dbas_graph.undercuts[undercut_id]
            premises = ['s' + str(premise) for premise in undercut.premises]
            negated_undercut_target = 'ni' + str(undercut.conclusion)
            rule_name = 'i' + str(undercut.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, negated_undercut_target),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
    else:
        # Setup defeasible inference acceptance functions
        for inference_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference_id]
            premises = ['s' + str(premise) for premise in inference.premises]
            conclusion = 's' + str(inference.conclusion)
            negated_conclusion = 'n' + conclusion if inference.is_supportive \
                else conclusion
            rule_name = 'i' + str(inference.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, negated_conclusion),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.NOT, rule_name))
        for undercut_id in dbas_graph.undercuts:
            undercut = dbas_graph.undercuts[undercut_id]
            premises = ['s' + str(premise) for premise in undercut.premises]
            negated_conclusion = 'i' + str(undercut.conclusion)
            rule_name = 'i' + str(undercut.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, negated_conclusion),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.NOT, rule_name))

    return adf


def import_adf_objective(dbas_graph, rules_strict):
    """
    Create an ADF representation in the given discussion.

    :param dbas_graph: DBASGraph to be used for ADF generation
    :type dbas_graph: DBASGraph
    :param rules_strict: indicate whether rules shall be implemented as strict or defeasible
    :type rules_strict: Boolean
    :return: ADF
    """
    adf = ADF()

    # Setup statement acceptance functions
    for statement in dbas_graph.statements:
        inferences_for = []
        inferences_against = []
        for inference_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference_id]
            if inference.conclusion == statement:
                if inference.is_supportive:
                    inferences_for.append(inference)
                else:
                    inferences_against.append(inference)

        # Acceptance condition for the positive (non-negated) literal
        if not inferences_for:
            adf.add_statement('s' + str(statement), ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_FALSE]))
        else:
            acceptance_criteria = ['i' + str(inference.id) for inference in inferences_for]
            adf.add_statement('s' + str(statement), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['ns' + str(statement)]),
                ADFNode(ADFNode.OR, acceptance_criteria)
            ]))

        # Acceptance condition for the negative (negated) literal
        if not inferences_against:
            adf.add_statement('ns' + str(statement), ADFNode(ADFNode.LEAF, [ADFNode.CONSTANT_FALSE]))
        else:
            acceptance_criteria = ['i' + str(inference.id) for inference in inferences_against]
            adf.add_statement('ns' + str(statement), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ['s' + str(statement)]),
                ADFNode(ADFNode.OR, acceptance_criteria)
            ]))

    if rules_strict:
        # Setup strict inference acceptance functions
        for inference_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference_id]
            premises = ['s' + str(premise) for premise in inference.premises]
            conclusion = 's' + str(inference.conclusion) if inference.is_supportive \
                else 'ns' + str(inference.conclusion)
            rule_name = 'i' + str(inference.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, conclusion),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
        for undercut_id in dbas_graph.undercuts:
            undercut = dbas_graph.undercuts[undercut_id]
            premises = ['s' + str(premise) for premise in undercut.premises]
            negated_undercut_target = 'ni' + str(undercut.conclusion)
            rule_name = 'i' + str(undercut.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, negated_undercut_target),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
    else:
        # Setup defeasible inference acceptance functions
        for inference_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference_id]
            premises = ['s' + str(premise) for premise in inference.premises]
            conclusion = 's' + str(inference.conclusion)
            negated_conclusion = 'n' + conclusion if inference.is_supportive \
                else conclusion
            rule_name = 'i' + str(inference.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, negated_conclusion),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.NOT, rule_name))
        for undercut_id in dbas_graph.undercuts:
            undercut = dbas_graph.undercuts[undercut_id]
            premises = ['s' + str(premise) for premise in undercut.premises]
            negated_conclusion = 'i' + str(undercut.conclusion)
            rule_name = 'i' + str(undercut.id)
            rule_name_negated = 'n' + rule_name
            adf.add_statement(rule_name, ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, negated_conclusion),
                ADFNode(ADFNode.NOT, rule_name_negated)
            ] + premises))
            adf.add_statement(rule_name_negated, ADFNode(ADFNode.NOT, rule_name))

    return adf
