import logging
logger = logging.getLogger('root')


def export_toast(graph_export, user_export, discussion_id, user_id):
    """
    Create an ASPIC representation formatted for TOAST from the given D-BAS data.

    :param graph_export:
    :param user_export:
    :param discussion_id:
    :param user_id:
    :return: dict
    """
    # TODO: do not use graph_export/user_export strings as input, but the dbas defeasible KB class (to be implemented)
    assumptions = ''
    for statement in user_export['marked_statements']:
        if statement in graph_export['nodes']:
            assumptions += str(statement) + ';'
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(discussion_id))
    for statement in user_export['accepted_statements_via_click']:
        if statement in graph_export['nodes']:
            assumptions += str(statement) + ';'
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(discussion_id))
    for statement in user_export['rejected_statements_via_click']:
        if statement in graph_export['nodes']:
            assumptions += '~' + str(statement) + ';'
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(discussion_id))

    rules = ''
    for rule in graph_export['inferences']:
        rules += '[r' + str(rule['id']) + '] ' \
                 + (','.join(map(str, list(rule['premises'])))) \
                 + '=>' + ('' if rule['is_supportive'] else '~') \
                 + str(rule['conclusion']) + ';'
    for undercut in graph_export['undercuts']:
        rules += '[r' + str(undercut['id']) + '] ' \
                 + (','.join(map(str, list(undercut['premises'])))) \
                 + '=>~' \
                 + '[r' + str(undercut['conclusion']) + '];'

    # Auxiliary TOAST input fields (not used, or defaults used)
    statement_prefs = ''
    rule_prefs = ''
    link_principle = 'weakest'  # options: 'weakest', 'last'.
    # query = ''
    semantics = 'preferred'  # options: 'stable', 'preferred', 'grounded'.

    result = {'assumptions': assumptions,
              'kbPrefs': statement_prefs,
              'rules': rules,
              'rulePrefs': rule_prefs,
              'contrariness': '',
              'link': link_principle,
              # 'query': query,
              'semantics': semantics}
    return result