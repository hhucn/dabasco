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
    aspic_axioms = ['assumptions_dummy', 'opinion_dummy']
    aspic_rules = []

    # Encode user opinion
    opinion_rule_ids = []
    if opinion_type == 'strict':
        for statement in opinion.accepted_statements_explicit:
            aspic_axioms.append(str(statement))
        for statement in opinion.accepted_statements_implicit:
            aspic_axioms.append(str(statement))
        for statement in opinion.rejected_statements_implicit:
            aspic_axioms.append('~' + str(statement))
    elif opinion_type == 'strong':
        for statement in opinion.accepted_statements_explicit:
            aspic_rules.append('[o' + str(statement) + '] opinion_dummy=>' + str(statement))
            opinion_rule_ids.append('[o' + str(statement) + ']')
        for statement in opinion.accepted_statements_implicit:
            aspic_rules.append('[o' + str(statement) + '] opinion_dummy=>' + str(statement))
            opinion_rule_ids.append('[o' + str(statement) + ']')
        for statement in opinion.rejected_statements_implicit:
            aspic_rules.append('[o' + str(statement) + '] opinion_dummy=>~' + str(statement))
            opinion_rule_ids.append('[o' + str(statement) + ']')
    elif opinion_type == 'weak':
        for statement in opinion.accepted_statements_explicit:
            aspic_rules.append('[o' + str(statement) + '] opinion_dummy=>' + str(statement))
            opinion_rule_ids.append('[o' + str(statement) + ']')
        for statement in opinion.accepted_statements_implicit:
            aspic_rules.append('[o' + str(statement) + '] opinion_dummy=>' + str(statement))
            opinion_rule_ids.append('[o' + str(statement) + ']')
        for statement in opinion.rejected_statements_implicit:
            aspic_rules.append('[o' + str(statement) + '] opinion_dummy=>~' + str(statement))
            opinion_rule_ids.append('[o' + str(statement) + ']')

    # Encode assumptions
    assumption_rule_ids = []
    if assumptions_type:
        for statement in dbas_graph.statements:
            if assumptions_bias != 'negative':
                aspic_rules.append('[a' + str(statement) + '] assumptions_dummy=>' + str(statement))
                assumption_rule_ids.append('[a' + str(statement) + ']')
            if assumptions_bias != 'positive':
                aspic_rules.append('[an' + str(statement) + '] assumptions_dummy=>~' + str(statement))
                assumption_rule_ids.append('[an' + str(statement) + ']')

    # Encode D-BAS inference rules
    inference_rule_ids = []
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        aspic_rules.append('[r' + str(inference.id) + '] '
                           + (','.join(map(str, list(inference.premises))))
                           + '=>' + ('' if inference.is_supportive else '~')
                           + str(inference.conclusion))
        inference_rule_ids.append('[r' + str(inference.id) + ']')
    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        aspic_rules.append('[r' + str(undercut.id) + '] '
                           + (','.join(map(str, list(undercut.premises))))
                           + '=>~'
                           + '[r' + str(undercut.conclusion) + ']')
        inference_rule_ids.append('[r' + str(undercut.id) + ']')

    # Set rule preferences
    aspic_rule_prefs = []
    if assumptions_type == "weak":
        for assumption_id in assumption_rule_ids:
            for inference_id in inference_rule_ids:
                aspic_rule_prefs.append(assumption_id + ' < ' + inference_id)
    if opinion_type == "weak":
        for opinion_id in opinion_rule_ids:
            for inference_id in inference_rule_ids:
                aspic_rule_prefs.append(opinion_id + ' < ' + inference_id)
    if opinion_type == "strong" and assumptions_type == "weak":
        for assumption_id in assumption_rule_ids:
            for opinion_id in opinion_rule_ids:
                aspic_rule_prefs.append(assumption_id + ' < ' + opinion_id)

    result = {'assumptions': aspic_assumptions,
              'axioms': aspic_axioms,
              'rules': aspic_rules,
              'rulePrefs': aspic_rule_prefs,
              'kbPrefs': [],
              'link': 'last',
              'contrariness': []}

    # Pass through semantics
    if semantics:
        result['semantics'] = str(semantics)

    return result
