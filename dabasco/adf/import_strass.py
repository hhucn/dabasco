from dabasco.config import *
from .adf_graph import ADF
from .adf_node import ADFNode


def import_adf(dbas_graph, user_opinion, assumptions_strong):
    """
    Create an ADF representation for given user's opinion in the given discussion.

    :param dbas_graph: DBASGraph to be used for ADF generation
    :type dbas_graph: DBASGraph
    :param user_opinion: DBASUser to be used for ADF generation
    :type user_opinion: DBASUser
    :param assumptions_strong: indicate whether assumptions shall be implemented as strict or defeasible
    :type assumptions_strong: bool
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
            statement_name = LITERAL_PREFIX_STATEMENT + str(statement)
            adf.add_statement(statement_name, ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        else:
            acceptance_criteria = [ADFNode(ADFNode.LEAF, LITERAL_PREFIX_INFERENCE_RULE + str(inference.id))
                                   for inference in inferences_for]
            if statement_assumed:
                acceptance_criteria.append(ADFNode(ADFNode.LEAF, LITERAL_PREFIX_OPINION_ASSUME + str(statement)))
            adf.add_statement(LITERAL_PREFIX_STATEMENT + str(statement), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF,
                                             LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + str(statement))),
                ADFNode(ADFNode.OR, acceptance_criteria)
            ]))

        # Acceptance condition for the negative (negated) literal
        if not inferences_against and not statement_rejected:
            adf.add_statement(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + str(statement),
                              ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_FALSE))
        else:
            acceptance_criteria = [ADFNode(ADFNode.LEAF, LITERAL_PREFIX_INFERENCE_RULE + str(inference.id))
                                   for inference in inferences_against]
            if statement_rejected:
                acceptance_criteria.append(ADFNode(ADFNode.LEAF, LITERAL_PREFIX_OPINION_REJECT + str(statement)))
            adf.add_statement(LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + str(statement), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_STATEMENT + str(statement))),
                ADFNode(ADFNode.OR, acceptance_criteria)
            ]))

    if assumptions_strong:
        # Setup strict user assumption acceptance functions
        for assumption in user_accepted_statements:
            adf.add_statement(LITERAL_PREFIX_OPINION_ASSUME + str(assumption), ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
            adf.add_statement(LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_ASSUME + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_STATEMENT + str(assumption))),
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_ASSUME + str(assumption)))
            ]))
        for assumption in user_rejected_statements:
            adf.add_statement(LITERAL_PREFIX_OPINION_REJECT + str(assumption), ADFNode(ADFNode.LEAF, ADFNode.CONSTANT_TRUE))
            adf.add_statement(LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_REJECT + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + str(assumption))),
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_REJECT + str(assumption)))
            ]))
    else:
        # Setup defeasible user assumption acceptance functions
        for assumption in user_accepted_statements:
            adf.add_statement(LITERAL_PREFIX_OPINION_ASSUME + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + str(assumption))),
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_ASSUME + str(assumption)))
            ]))
            adf.add_statement(LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_ASSUME + str(assumption), ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_OPINION_ASSUME + str(assumption))))
        for assumption in user_rejected_statements:
            adf.add_statement(LITERAL_PREFIX_OPINION_REJECT + str(assumption), ADFNode(ADFNode.AND, [
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_STATEMENT + str(assumption))),
                ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_REJECT + str(assumption)))
            ]))
            adf.add_statement(LITERAL_PREFIX_NOT + LITERAL_PREFIX_OPINION_REJECT + str(assumption), ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, LITERAL_PREFIX_OPINION_REJECT + str(assumption))))

    # Setup defeasible inference acceptance functions
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        premises = [LITERAL_PREFIX_STATEMENT + str(premise) for premise in inference.premises]
        conclusion = LITERAL_PREFIX_STATEMENT + str(inference.conclusion)
        negated_conclusion = LITERAL_PREFIX_NOT + conclusion if inference.is_supportive \
            else conclusion
        rule_name = LITERAL_PREFIX_INFERENCE_RULE + str(inference.id)
        rule_name_negated = LITERAL_PREFIX_NOT + rule_name
        adf.add_statement(rule_name, ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, negated_conclusion)),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, rule_name_negated))
        ] + [ADFNode(ADFNode.LEAF, premise) for premise in premises]))
        adf.add_statement(rule_name_negated, ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, rule_name)))
    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        premises = [LITERAL_PREFIX_STATEMENT + str(premise) for premise in undercut.premises]
        negated_conclusion = LITERAL_PREFIX_INFERENCE_RULE + str(undercut.conclusion)
        rule_name = LITERAL_PREFIX_INFERENCE_RULE + str(undercut.id)
        rule_name_negated = LITERAL_PREFIX_NOT + rule_name
        adf.add_statement(rule_name, ADFNode(ADFNode.AND, [
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, negated_conclusion)),
            ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, rule_name_negated))
        ] + [ADFNode(ADFNode.LEAF, premise) for premise in premises]))
        adf.add_statement(rule_name_negated, ADFNode(ADFNode.NOT, ADFNode(ADFNode.LEAF, rule_name)))

    return adf
