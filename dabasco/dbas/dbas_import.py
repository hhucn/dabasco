from dabasco.config import *
from dabasco.dbas.dbas_user import DBASUser
from dabasco.dbas.dbas_graph import DBASGraph

import logging
logger = logging.getLogger('root')


def import_dbas_graph_v2(discussion_id, statements_json, arguments_json):
    """
    Convert the given D-BAS API v2 graph export to a DBASGraph data structure.

    :param discussion_id: id of the discussion
    :type discussion_id: int
    :param statements_json: json dict as provided by D-BAS graph export
    :type statements_json: dict
    :param arguments_json: json dict as provided by D-BAS graph export
    :type arguments_json: dict
    :return: DBASGraph
    """
    logging.debug('Reading D-BAS graph data...')
    graph = DBASGraph(discussion_id)

    if statements_json[DBAS_API2_KEYWORD_ISSUE]:
        all_statements = set()
        for statement_json in statements_json[DBAS_API2_KEYWORD_ISSUE][DBAS_API2_KEYWORD_STATEMENTS]:
            statement = int(statement_json[DBAS_API2_KEYWORD_UID])
            logging.debug('Statement: %s', statement)
            all_statements.add(statement)

        used_statements = set()
        for argument_json in arguments_json[DBAS_API2_KEYWORD_ISSUE][DBAS_API2_KEYWORD_ARGUMENTS]:
            logging.debug('Inference: %s', argument_json)
            inference_id = int(argument_json[DBAS_API2_KEYWORD_UID])
            premises = [int(s[DBAS_API2_KEYWORD_STATEMENT_UID])
                        for s in argument_json[DBAS_API2_KEYWORD_PREMISEGROUP][DBAS_API2_KEYWORD_PREMISES]]
            for premise in premises:
                used_statements.add(premise)

            conclusion = argument_json[DBAS_API2_KEYWORD_CONCLUSION_UID]
            undercut_target = argument_json[DBAS_API2_KEYWORD_ARGUMENT_UID]

            if conclusion:
                # Normal argument
                conclusion = int(conclusion)
                used_statements.add(conclusion)
                is_supportive = bool(argument_json[DBAS_API2_KEYWORD_IS_SUPPORTIVE])
                graph.add_inference(inference_id, premises, conclusion, is_supportive)
            elif undercut_target:
                # Undercutting argument
                undercut_target = int(undercut_target)
                graph.add_undercut(inference_id, premises, undercut_target)
            else:
                logging.warning('D-BAS argument %s has neither statement conclusion nor undercut target!', inference_id)

        for statement in all_statements:
            if statement not in used_statements:
                logging.debug('Statement %s not used in arguments: omit!', statement)
            else:
                graph.add_statement(statement)

    return graph


def import_dbas_user_v2(discussion_id, user_id, user_json):
    """
    Convert the given D-BAS API v2 user export to a DBASUser data structure.

    :param discussion_id: id of the context discussion
    :type discussion_id: int
    :param user_id: id of the user
    :type user_id: int
    :param user_json: json dict as provided by D-BAS user opinion export
    :type user_json: dict
    :return: DBASUser
    """
    logging.debug('Reading D-BAS user opinion data...')
    user_opinion = DBASUser(discussion_id, user_id)

    if user_json[DBAS_API2_KEYWORD_USER] and user_json[DBAS_API2_KEYWORD_USER][DBAS_API2_KEYWORD_CLICKED_STATEMENTS]:
        statements_json = user_json[DBAS_API2_KEYWORD_USER][DBAS_API2_KEYWORD_CLICKED_STATEMENTS]
        for statement_json in statements_json:
            statement_id = int(statement_json[DBAS_API2_KEYWORD_STATEMENT_UID])
            is_upvote = bool(statement_json[DBAS_API2_KEYWORD_IS_UPVOTE])
            if is_upvote:
                user_opinion.accepted_statements_explicit.add(statement_id)
            else:
                user_opinion.rejected_statements_explicit.add(statement_id)

    return user_opinion


def import_dbas_graph(discussion_id, graph_export):
    """
    Convert the given D-BAS graph export to a DBASGraph data structure.

    :param discussion_id: id of the discussion
    :type discussion_id: int
    :param graph_export: json dict as provided by D-BAS graph export
    :type graph_export: dict
    :return: DBASGraph
    """
    logging.debug('Reading D-BAS graph data...')
    graph = DBASGraph(discussion_id)

    all_statements = set()
    for statement in graph_export[DBAS_KEYWORD_STATEMENTS]:
        logging.debug('Statement: %s', statement)
        # graph.add_statement(statement)
        all_statements.add(statement)

    used_statements = set()
    for argument in graph_export[DBAS_KEYWORD_INFERENCE_RULES]:
        logging.debug('Inference: %s', argument)
        inference_id = argument[DBAS_KEYWORD_INFERENCE_RULE_ID]
        premises = argument[DBAS_KEYWORD_INFERENCE_RULE_PREMISES]
        conclusion = argument[DBAS_KEYWORD_INFERENCE_RULE_CONCLUSION]
        for premise in premises:
            used_statements.add(premise)
        used_statements.add(conclusion)
        is_supportive = argument[DBAS_KEYWORD_INFERENCE_RULE_SUPPORTIVE]
        graph.add_inference(inference_id, premises, conclusion, is_supportive)

    for undercut in graph_export[DBAS_KEYWORD_UNDERCUTS]:
        logging.debug('Undercut: %s', undercut)
        inference_id = undercut[DBAS_KEYWORD_UNDERCUT_ID]
        premises = undercut[DBAS_KEYWORD_UNDERCUT_PREMISES]
        conclusion = undercut[DBAS_KEYWORD_UNDERCUT_CONCLUSION]
        for premise in premises:
            used_statements.add(premise)
        graph.add_undercut(inference_id, premises, conclusion)

    for statement in all_statements:
        if statement not in used_statements:
            logging.debug('Statement %s not used in arguments: omit!', statement)
        else:
            graph.add_statement(statement)

    return graph


def import_dbas_user(discussion_id, user_id, user_export):
    """
    Convert the given D-BAS user export to a DBASUser data structure.

    :param discussion_id: id of the context discussion
    :type discussion_id: int
    :param user_id: id of the user
    :type user_id: int
    :param user_export: json dict as provided by D-BAS user opinion export
    :type user_export: dict
    :return: DBASUser
    """
    logging.debug('Reading D-BAS user opinion data...')
    user_opinion = DBASUser(discussion_id, user_id)

    user_opinion.accepted_statements_explicit = set(user_export[DBAS_KEYWORD_ACCEPTED_STATEMENTS_EXPLICIT])
    user_opinion.accepted_statements_implicit = set(user_export[DBAS_KEYWORD_ACCEPTED_STATEMENTS_IMPLICIT])
    user_opinion.rejected_statements_implicit = set(user_export[DBAS_KEYWORD_REJECTED_STATEMENTS_IMPLICIT])
    user_opinion.accepted_arguments_explicit = set(user_export[DBAS_KEYWORD_ACCEPTED_ARGUMENTS_EXPLICIT])
    user_opinion.rejected_arguments_explicit = set(user_export[DBAS_KEYWORD_REJECTED_ARGUMENTS_EXPLICIT])

    return user_opinion
