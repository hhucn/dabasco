
from dabasco.config import *


def create_toast_rule_representation(prefix, rule_id):
    return TOAST_SYMBOL_RULE_NAME_PREFIX + str(prefix) + str(rule_id) + TOAST_SYMBOL_RULE_NAME_SUFFIX


def create_toast_rule(rule_name, premises, conclusion, rule_symbol):
    return rule_name + ' ' + (','.join(map(str, list(premises)))) + rule_symbol + conclusion


def create_toast_rule_defeasible(rule_name, premises, conclusion):
    return create_toast_rule(rule_name, premises, conclusion, TOAST_SYMBOL_RULE_DEFEASIBLE)


def create_toast_rule_strict(rule_name, premises, conclusion):
    return create_toast_rule(rule_name, premises, conclusion, TOAST_SYMBOL_RULE_STRICT)


def create_toast_preference(item_lower, item_higher):
    return item_lower + ' ' + TOAST_SYMBOL_PREFERENCE + ' ' + item_higher


def export_toast(dbas_graph, opinion_type, opinion, assumptions_type, assumptions_bias, semantics=None):
    """
    Create an ASPIC representation formatted for TOAST from the given D-BAS data.

    :param dbas_graph: DBASGraph to be used for ASPIC generation
    :type dbas_graph: DBASGraph
    :param opinion_type: indicates whether an opinion is used, and with which strength
    :type opinion_type: str
    :param opinion: DBASUser user opinion
    :type opinion: DBASUser
    :param assumptions_type: indicates whether assumptions are used, and with which strength
    :type assumptions_type: str
    :param assumptions_bias: indicates whether assumptions are biased
    :type assumptions_bias: str
    :param semantics: allows to specify an evaluation semantics to be used for this ASPIC instance
    :type assumptions_bias: str
    :return: dict
    """
    aspic_assumptions = []
    aspic_axioms = []
    aspic_rules = []

    # Encode user opinion
    user_accepted_statements = set()
    user_rejected_statements = set()
    if opinion:
        aspic_axioms.append(DUMMY_LITERAL_NAME_OPINION)
        user_accepted_statements = opinion.get_accepted_statements()
        user_rejected_statements = opinion.get_rejected_statements()
    opinion_rule_names = []
    if opinion_type == DABASCO_INPUT_KEYWORD_OPINION_STRICT:
        for statement in user_accepted_statements:
            rule_name = create_toast_rule_representation(LITERAL_PREFIX_OPINION_ASSUME, statement)
            rule = create_toast_rule_strict(rule_name=rule_name,
                                            premises=[DUMMY_LITERAL_NAME_OPINION],
                                            conclusion=str(statement))
            aspic_rules.append(rule)
            opinion_rule_names.append(rule_name)
        for statement in user_rejected_statements:
            rule_name = create_toast_rule_representation(LITERAL_PREFIX_OPINION_REJECT, statement)
            rule = create_toast_rule_strict(rule_name=rule_name,
                                            premises=[DUMMY_LITERAL_NAME_OPINION],
                                            conclusion=TOAST_SYMBOL_NEGATION + str(statement))
            aspic_rules.append(rule)
            opinion_rule_names.append(rule_name)
    elif opinion_type in [DABASCO_INPUT_KEYWORD_OPINION_WEAK, DABASCO_INPUT_KEYWORD_OPINION_STRONG]:
        for statement in user_accepted_statements:
            rule_name = create_toast_rule_representation(LITERAL_PREFIX_OPINION_ASSUME, statement)
            rule = create_toast_rule_defeasible(rule_name=rule_name,
                                                premises=[DUMMY_LITERAL_NAME_OPINION],
                                                conclusion=str(statement))
            aspic_rules.append(rule)
            opinion_rule_names.append(rule_name)
        for statement in user_rejected_statements:
            rule_name = create_toast_rule_representation(LITERAL_PREFIX_OPINION_REJECT, statement)
            rule = create_toast_rule_defeasible(rule_name=rule_name,
                                                premises=[DUMMY_LITERAL_NAME_OPINION],
                                                conclusion=TOAST_SYMBOL_NEGATION + str(statement))
            aspic_rules.append(rule)
            opinion_rule_names.append(rule_name)

    # Encode assumptions
    assumption_rule_names = []
    if assumptions_type:
        aspic_axioms.append(DUMMY_LITERAL_NAME_ASSUMPTIONS)
        for statement in dbas_graph.statements:
            if assumptions_bias != 'negative':
                rule_name = create_toast_rule_representation(LITERAL_PREFIX_ASSUMPTION_ASSUME, statement)
                rule = create_toast_rule_defeasible(rule_name=rule_name,
                                                    premises=[DUMMY_LITERAL_NAME_ASSUMPTIONS],
                                                    conclusion=str(statement))
                aspic_rules.append(rule)
                assumption_rule_names.append(rule_name)
            if assumptions_bias != 'positive':
                rule_name = create_toast_rule_representation(LITERAL_PREFIX_ASSUMPTION_REJECT, statement)
                rule = create_toast_rule_defeasible(rule_name=rule_name,
                                                    premises=[DUMMY_LITERAL_NAME_ASSUMPTIONS],
                                                    conclusion=TOAST_SYMBOL_NEGATION + str(statement))
                aspic_rules.append(rule)
                assumption_rule_names.append(rule_name)

    # Encode D-BAS inference rules
    inference_rule_names = []
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        rule_name = create_toast_rule_representation(LITERAL_PREFIX_INFERENCE_RULE, inference.id)
        optional_negation = ('' if inference.is_supportive else TOAST_SYMBOL_NEGATION)
        rule = create_toast_rule_defeasible(rule_name=rule_name,
                                            premises=map(str, list(inference.premises)),
                                            conclusion=optional_negation + str(inference.conclusion))
        aspic_rules.append(rule)
        inference_rule_names.append(rule_name)
    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        rule_name = create_toast_rule_representation(LITERAL_PREFIX_INFERENCE_RULE, undercut.id)
        target_rule_name = create_toast_rule_representation(LITERAL_PREFIX_INFERENCE_RULE, undercut.conclusion)
        rule = create_toast_rule_defeasible(rule_name=rule_name,
                                            premises=map(str, list(undercut.premises)),
                                            conclusion=TOAST_SYMBOL_NEGATION + target_rule_name)
        aspic_rules.append(rule)
        inference_rule_names.append(rule_name)

    # Set rule preferences
    aspic_rule_prefs = []
    if assumptions_type == DABASCO_INPUT_KEYWORD_OPINION_WEAK:
        for assumption_id in assumption_rule_names:
            for inference_id in inference_rule_names:
                preference = create_toast_preference(item_lower=assumption_id, item_higher=inference_id)
                aspic_rule_prefs.append(preference)
    if opinion_type == DABASCO_INPUT_KEYWORD_OPINION_WEAK:
        for opinion_id in opinion_rule_names:
            for inference_id in inference_rule_names:
                preference = create_toast_preference(item_lower=opinion_id, item_higher=inference_id)
                aspic_rule_prefs.append(preference)
    if opinion_type == DABASCO_INPUT_KEYWORD_OPINION_STRONG and assumptions_type == DABASCO_INPUT_KEYWORD_OPINION_WEAK:
        for assumption_id in assumption_rule_names:
            for opinion_id in opinion_rule_names:
                preference = create_toast_preference(item_lower=assumption_id, item_higher=opinion_id)
                aspic_rule_prefs.append(preference)

    result = {TOAST_KEYWORD_ASSUMPTIONS: aspic_assumptions,
              TOAST_KEYWORD_AXIOMS: aspic_axioms,
              TOAST_KEYWORD_RULES: aspic_rules,
              TOAST_KEYWORD_RULEPREFS: aspic_rule_prefs,
              TOAST_KEYWORD_LITERALPREFS: [],
              TOAST_KEYWORD_LINK_PRINCIPLE: TOAST_KEYWORD_LAST_LINK_PRINCIPLE,
              TOAST_KEYWORD_CONTRARINESS: []}

    # Pass through semantics
    if semantics:
        result[TOAST_KEYWORD_SEMANTICS] = str(semantics)

    return result
