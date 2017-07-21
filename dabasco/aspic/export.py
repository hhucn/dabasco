import logging
logger = logging.getLogger('root')


def export_toast(dbas_graph, dbas_user):
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

    result = {'assumptions': ';'.join(assumptions),
              'rules': ';'.join(rules),
              'contrariness': ''}
    return result
