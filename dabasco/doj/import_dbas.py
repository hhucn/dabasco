from .sm import SM

import logging
logger = logging.getLogger('root')


def import_statement_map(dbas_graph):
    """
    Convert the given D-BAS graph to a SM data structure.

    :param dbas_graph: dbas graph to be converted
    :type dbas_graph: DBASGraph
    :return: SM
    """
    logging.debug('Create Statement Map from D-BAS graph...')
    n_nodes = 0
    node_id_for_index = {}
    node_index_for_id = {}
    for n in dbas_graph.statements:
        logging.debug('Node: %s', n)
        n_nodes += 1
        node_id_for_index[n_nodes] = n
        node_index_for_id[n] = n_nodes
    logging.debug('node_id_for_index: %s', node_id_for_index)
    logging.debug('node_index_for_id: %s', node_index_for_id)
    statement_map = SM()
    statement_map.n = n_nodes
    statement_map.node_id_for_index = node_id_for_index
    statement_map.node_index_for_id = node_index_for_id

    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        logging.debug('Inference: %s', inference)
        premises = [node_index_for_id[n] for n in inference.premises]
        conclusion = node_index_for_id[inference.conclusion]
        if not inference.is_supportive:
            conclusion = -conclusion
        rid = statement_map.add_inference(premises, conclusion, inference_id)
        if rid != inference_id:
            logging.warning('Added wrong inference id: rid=%s, i.id=%s', str(rid), str(inference_id))
        else:
            logging.debug('Added inference successfully (rid=%s)!', str(rid))

    for undercut_id in dbas_graph.undercuts:
        undercut = dbas_graph.undercuts[undercut_id]
        logging.debug('Undercut: %s', undercut)
        premises = [node_index_for_id[n] for n in undercut.premises]
        rid = statement_map.add_undercut(premises, undercut.conclusion, undercut_id)
        if rid != undercut_id:
            logging.warning('Added wrong undercut id: rid=' + str(rid) + ', u.id=' + str(undercut_id))
        else:
            logging.debug('Added undercut successfully (rid=%s)!', str(rid))

    return statement_map
