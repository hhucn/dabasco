from dabasco.config import *
from dabasco.dbas.dbas_user import DBASUser
from dabasco.dbas.dbas_graph import DBASGraph

import logging
logger = logging.getLogger('root')


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

    n_statements = 0
    for statement in graph_export[DBAS_KEYWORD_STATEMENTS]:
        logging.debug('Statement: %s', statement)
        graph.add_statement(statement)
        n_statements += 1

    for i in graph_export[DBAS_KEYWORD_INFERENCE_RULES]:
        logging.debug('Inference: %s', i)
        inference_id = i[DBAS_KEYWORD_INFERENCE_RULE_ID]
        premises = i[DBAS_KEYWORD_INFERENCE_RULE_PREMISES]
        conclusion = i[DBAS_KEYWORD_INFERENCE_RULE_CONCLUSION]
        is_supportive = i[DBAS_KEYWORD_INFERENCE_RULE_SUPPORTIVE]
        graph.add_inference(inference_id, premises, conclusion, is_supportive)

    for u in graph_export[DBAS_KEYWORD_UNDERCUTS]:
        logging.debug('Undercut: %s', u)
        inference_id = u[DBAS_KEYWORD_UNDERCUT_ID]
        premises = u[DBAS_KEYWORD_UNDERCUT_PREMISES]
        conclusion = u[DBAS_KEYWORD_UNDERCUT_CONCLUSION]
        graph.add_undercut(inference_id, premises, conclusion)

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

    user_opinion.accepted_statements_explicit = user_export[DBAS_KEYWORD_ACCEPTED_STATEMENTS_EXPLICIT]
    user_opinion.accepted_statements_implicit = user_export[DBAS_KEYWORD_ACCEPTED_STATEMENTS_IMPLICIT]
    user_opinion.rejected_statements_implicit = user_export[DBAS_KEYWORD_REJECTED_STATEMENTS_IMPLICIT]
    user_opinion.accepted_arguments_explicit = user_export[DBAS_KEYWORD_ACCEPTED_ARGUMENTS_EXPLICIT]
    user_opinion.rejected_arguments_explicit = user_export[DBAS_KEYWORD_REJECTED_ARGUMENTS_EXPLICIT]

    return user_opinion
