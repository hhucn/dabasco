def export_toast(dbas_graph, dbas_user, assumptions_strict):
    """
    Create an ASPIC representation formatted for TOAST from the given D-BAS data.

    :param dbas_graph: DBASGraph to be used for ADF generation
    :type dbas_graph: DBASGraph
    :param dbas_user: DBASUser to be used for ADF generation
    :type dbas_user: DBASUser
    :param assumptions_strict: indicate whether assumptions shall be implemented as strict or defeasible
    :type assumptions_strict: bool
    :return: dict
    """
    assumptions = []
    for statement in dbas_user.accepted_statements_explicit:
        assumptions.append(str(statement))
    for statement in dbas_user.accepted_statements_implicit:
        assumptions.append(str(statement))
    for statement in dbas_user.rejected_statements_implicit:
        assumptions.append('~' + str(statement))

    rules = []
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        rules.append('[r' + str(inference.id) + '] '
                     + (','.join(map(str, list(inference.premises))))
                     + '=>' + ('' if inference.is_supportive else '~')
                     + str(inference.conclusion))
    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        rules.append('[r' + str(undercut.id) + '] '
                     + (','.join(map(str, list(undercut.premises))))
                     + '=>~'
                     + '[r' + str(undercut.conclusion) + ']')

    premises_key = 'axioms' if assumptions_strict else 'assumptions'
    result = {premises_key: ';'.join(assumptions),
              'rules': ';'.join(rules),
              'contrariness': ''}
    return result


def export_toast_rulebased(dbas_graph, dbas_user):
    """
    Create an ASPIC representation formatted for TOAST from the given D-BAS data.

    :param dbas_graph: DBASGraph to be used for ADF generation
    :type dbas_graph: DBASGraph
    :param dbas_user: DBASUser to be used for ADF generation
    :type dbas_user: DBASUser
    :return: dict
    """
    assumptions = []
    for statement in dbas_user.accepted_statements_explicit:
        assumptions.append('dummy' + str(statement))
    for statement in dbas_user.accepted_statements_implicit:
        assumptions.append('dummy' + str(statement))
    for statement in dbas_user.rejected_statements_implicit:
        assumptions.append('~dummy' + str(statement))

    rules = []
    assumption_rule_ids = []
    for statement in dbas_user.accepted_statements_explicit:
        rules.append('[a' + str(statement) + '] dummy' + str(statement) + '=>' + str(statement))
        assumption_rule_ids.append('[a' + str(statement) + ']')
    for statement in dbas_user.accepted_statements_implicit:
        rules.append('[a' + str(statement) + '] dummy' + str(statement) + '=>' + str(statement))
        assumption_rule_ids.append('[a' + str(statement) + ']')
    for statement in dbas_user.rejected_statements_implicit:
        rules.append('[a' + str(statement) + '] dummy' + str(statement) + '=>~' + str(statement))
        assumption_rule_ids.append('[a' + str(statement) + ']')

    inference_rule_ids = []
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        rules.append('[r' + str(inference.id) + '] '
                     + (','.join(map(str, list(inference.premises))))
                     + '=>' + ('' if inference.is_supportive else '~')
                     + str(inference.conclusion))
        inference_rule_ids.append('[r' + str(inference.id) + ']')
    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        rules.append('[r' + str(undercut.id) + '] '
                     + (','.join(map(str, list(undercut.premises))))
                     + '=>~'
                     + '[r' + str(undercut.conclusion) + ']')
        inference_rule_ids.append('[r' + str(undercut.id) + ']')

    rule_prefs = ''
    for assumption_id in assumption_rule_ids:
        for inference_id in inference_rule_ids:
            rule_prefs += assumption_id + ' < ' + inference_id + ';'

    result = {'assumptions': ';'.join(assumptions),
              'rules': ';'.join(rules),
              'rulePrefs': rule_prefs,
              'contrariness': ''}
    return result


def export_toast_rulebased_objective(dbas_graph, positive_bias):
    """
    Create an ASPIC representation formatted for TOAST from the given D-BAS data.

    :param dbas_graph: DBASGraph to be used for ADF generation
    :type dbas_graph: DBASGraph
    :param positive_bias: indicate whether default assumptions shall be created for all or only for positive literals
    :type positive_bias: bool
    :return: dict
    """
    rules = []
    assumption_rule_ids = []
    assumptions = []
    for statement in dbas_graph.statements:
        assumptions.append('dummy' + str(statement))
        rules.append('[a' + str(statement) + '] dummy' + str(statement) + '=>' + str(statement))
        assumption_rule_ids.append('[a' + str(statement) + ']')
        if not positive_bias:
            assumptions.append('dummy_not' + str(statement))
            rules.append('[an' + str(statement) + '] dummy_not' + str(statement) + '=>~' + str(statement))
            assumption_rule_ids.append('[an' + str(statement) + ']')

    inference_rule_ids = []
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        rules.append('[r' + str(inference.id) + '] '
                     + (','.join(map(str, list(inference.premises))))
                     + '=>' + ('' if inference.is_supportive else '~')
                     + str(inference.conclusion))
        inference_rule_ids.append('[r' + str(inference.id) + ']')
    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        rules.append('[r' + str(undercut.id) + '] '
                     + (','.join(map(str, list(undercut.premises))))
                     + '=>~'
                     + '[r' + str(undercut.conclusion) + ']')
        inference_rule_ids.append('[r' + str(undercut.id) + ']')

    rule_prefs = ''
    for assumption_id in assumption_rule_ids:
        for inference_id in inference_rule_ids:
            rule_prefs += assumption_id + ' < ' + inference_id + ';'

    result = {'assumptions': ';'.join(assumptions),
              'rules': ';'.join(rules),
              'rulePrefs': rule_prefs,
              'contrariness': ''}
    return result
