#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request
import json

from doj.pos import Position
from doj.sm import SM
from doj.doj import DoJ

from os import path
import logging
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('root')

app = Flask(__name__)
CORS(app)  # Set security headers for Web requests


@app.route('/evaluate/reasons/<int:discussion>')
def evaluate_issue_reasons(discussion):
    """
    Return a json string with all strengths of reason for the given discussion.
    
    :param discussion: discussion ID 
    :return: json string
    """

    # Get D-BAS graph
    url = 'http://localhost:4284/export/doj/{}'.format(discussion)

    response = urllib.request.urlopen(url).read()
    export = response.decode('utf-8')

    while isinstance(export, str):
        export = json.loads(export)

    # Create statement map from data
    statement_map, node_index_for_id, node_id_for_index = dbas_graph_to_statement_map(export)

    # Calculate all Reason relations
    doj = DoJ()
    n = statement_map.n
    reasons = {}
    for s1 in range(1, n + 1):
        reasons_s1 = {}
        for s2 in range(1, n + 1):
            r = doj.reason(statement_map, s1, s2, DoJ.REASON_RELATION_1, DoJ.DOJ_RECALL,
                           SM.COHERENCE_DEDUCTIVE_INFERENCES)
            reasons_s1[node_id_for_index[s2]] = r
        reasons[node_id_for_index[s1]] = reasons_s1

    return jsonify({'reasons': reasons})


@app.route('/evaluate/dojs/<int:discussion>/<string:statements>')
@app.route('/evaluate/dojs/<int:discussion>/', defaults={'statements': ''})
@app.route('/evaluate/dojs/<int:discussion>', defaults={'statements': ''})
def evaluate_issue_dojs(discussion, statements):
    """
    Return a json string with DoJs for the specified statements.

    :param discussion: discussion ID
    :param statements: comma separated string of statements for which the DoJs are calculated. 
    :return: json string
    
    IDs of statements that do not exist in the given discussion are ignored.
    If no statements are given, DoJs for all statements in the discussion are calculated.
    """

    url = 'http://localhost:4284/export/doj/{}'.format(discussion)

    requested_statements_list = None
    if statements:
        requested_statements_list = [int(s) for s in statements.split(',')]

    response = urllib.request.urlopen(url).read()
    export = response.decode('utf-8')

    while isinstance(export, str):
        export = json.loads(export)

    # Create statement map from data
    statement_map, node_index_for_id, node_id_for_index = dbas_graph_to_statement_map(export)

    # Calculate the DoJs of all requested statements
    doj = DoJ()
    dojs = {}
    n = statement_map.n
    if requested_statements_list:
        requested_statements_list = [i for i in requested_statements_list if i in node_index_for_id]
        query_requested_statements = [node_index_for_id[i] for i in requested_statements_list]
    else:
        # Default: calculate all DoJs ([1,...,n]) if no specific statements were requested.
        query_requested_statements = range(1, n + 1)
    for s in query_requested_statements:
        pos = Position(n)
        pos.set_accepted(s)
        doj_s = doj.doj(statement_map, pos, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
        dojs[node_id_for_index[s]] = doj_s
        logging.debug('DoJ(%s): %s', node_id_for_index[s], doj_s)

    return jsonify({'dojs': dojs})


@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/acc/<string:acc2>/rej/<string:rej2>')
@app.route('/evaluate/doj/<int:dis>/pos1/rej/<string:rej1>/pos2/acc/<string:acc2>/rej/<string:rej2>', defaults={'acc1': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/pos2/acc/<string:acc2>/rej/<string:rej2>', defaults={'rej1': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/rej/<string:rej2>', defaults={'acc2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/acc/<string:acc2>', defaults={'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/pos2/acc/<string:acc2>/rej/<string:rej2>', defaults={'acc1': '', 'rej1': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/rej/<string:rej1>/pos2/rej/<string:rej2>', defaults={'acc1': '', 'acc2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/rej/<string:rej1>/pos2/acc/<string:acc2>', defaults={'acc1': '', 'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/pos2/rej/<string:rej2>', defaults={'rej1': '', 'acc2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/pos2/acc/<string:acc2>', defaults={'rej1': '', 'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2', defaults={'acc2': '', 'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/pos2/rej/<string:rej2>', defaults={'acc1': '', 'rej1': '', 'acc2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/pos2/acc/<string:acc2>', defaults={'acc1': '', 'rej1': '', 'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/rej/<string:rej1>/pos2', defaults={'acc1': '', 'acc2': '', 'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/pos2', defaults={'rej1': '', 'acc2': '', 'rej2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/pos2', defaults={'acc1': '', 'rej1': '', 'acc2': '', 'rej2': ''})
def evaluate_issue_conditional_doj(dis, acc1, rej1, acc2, rej2):
    """
    Return a json string with the DoJ of position pos1 given position pos2.
    
    :param dis: discussion ID
    :param acc1: (optional) comma separated string of statement IDs which are accepted in position pos1.
    :param rej1: (optional) comma separated string of statement IDs which are rejected in position pos1.
    :param acc2: (optional) comma separated string of statement IDs which are accepted in conditional position pos2.
    :param rej2: (optional) comma separated string of statement IDs which are rejected in conditional position pos2. 
    :return: json string
    
    IDs of statements that do not exist in the given discussion are ignored.
    """

    # Get discussion graph
    url = 'http://localhost:4284/export/doj/{}'.format(dis)

    response = urllib.request.urlopen(url).read()
    export = response.decode('utf-8')

    while isinstance(export, str):
        export = json.loads(export)

    # Create statement map from data
    statement_map, node_index_for_id, node_id_for_index = dbas_graph_to_statement_map(export)

    # Process input positions
    n = statement_map.n
    pos1 = Position(n)
    if acc1:
        for s in acc1.split(','):
            if int(s) in node_index_for_id:
                pos1.set_accepted(node_index_for_id[int(s)])
    if rej1:
        for s in rej1.split(','):
            if int(s) in node_index_for_id:
                pos1.set_rejected(node_index_for_id[int(s)])

    pos2 = Position(n)
    if acc2:
        for s in acc2.split(','):
            if int(s) in node_index_for_id:
                pos2.set_accepted(node_index_for_id[int(s)])
    if rej2:
        for s in rej2.split(','):
            if int(s) in node_index_for_id:
                pos2.set_rejected(node_index_for_id[int(s)])

    # Calculate the conditional DoJ of position 1 given position 2.
    doj = DoJ()
    result = doj.doj_conditional(statement_map, pos1, pos2, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)

    return jsonify({'doj': result})


@app.route('/evaluate/doj/<int:dis>/user/<int:user>')
def evaluate_issue_doj_user_position(dis, user):
    """
    Return a json string with the DoJ of the opinion of the given user.

    :param dis: discussion ID
    :param user: user ID 
    :return: json string
    """

    # Get D-BAS graph and user data
    graph_url = 'http://localhost:4284/export/doj/{}'.format(dis)
    user_url = 'http://localhost:4284/export/doj_user/{}/{}'.format(user, dis)

    user_response = urllib.request.urlopen(user_url).read()
    user_export = user_response.decode('utf-8')
    while isinstance(user_export, str):
        user_export = json.loads(user_export)

    graph_response = urllib.request.urlopen(graph_url).read()
    graph_export = graph_response.decode('utf-8')
    while isinstance(graph_export, str):
        graph_export = json.loads(graph_export)

    # Create statement map from data
    statement_map, node_index_for_id, node_id_for_index = dbas_graph_to_statement_map(graph_export)

    # Process input position
    n = statement_map.n
    pos1 = Position(n)
    for statement in user_export['marked_statements']:
        if statement in graph_export['nodes']:
            pos1.set_accepted(node_index_for_id[int(statement)])
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(dis))
    for statement in user_export['accepted_statements_via_click']:
        if statement in graph_export['nodes']:
            pos1.set_accepted(node_index_for_id[int(statement)])
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(dis))
    for statement in user_export['rejected_statements_via_click']:
        if statement in graph_export['nodes']:
            pos1.set_rejected(node_index_for_id[int(statement)])
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(dis))

    # Calculate the conditional DoJ of position 1 given position 2.
    doj = DoJ()
    result = doj.doj(statement_map, pos1, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)

    return jsonify({'doj': result})


@app.route('/evaluate/toastify/<int:discussion>/<int:user>')
def toastify(discussion, user):
    """
    Create a TOAST-formatted graph representation for given user's opinion.

    :param discussion: discussion ID
    :param user: user ID
    :return: json string
    
    TOAST documentation: http://www.arg.dundee.ac.uk/toast/help/web
    """

    # Get D-BAS graph and user data
    graph_url = 'http://localhost:4284/export/doj/{}'.format(discussion)
    user_url = 'http://localhost:4284/export/doj_user/{}/{}'.format(user, discussion)

    user_response = urllib.request.urlopen(user_url).read()
    user_export = user_response.decode('utf-8')
    while isinstance(user_export, str):
        user_export = json.loads(user_export)

    graph_response = urllib.request.urlopen(graph_url).read()
    graph_export = graph_response.decode('utf-8')
    while isinstance(graph_export, str):
        graph_export = json.loads(graph_export)

    # Get assumptions and inference rules from D-BAS data
    assumptions = ''
    for statement in user_export['marked_statements']:
        if statement in graph_export['nodes']:
            assumptions += str(statement) + ';'
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(discussion))
    for statement in user_export['accepted_statements_via_click']:
        if statement in graph_export['nodes']:
            assumptions += str(statement) + ';'
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(discussion))
    for statement in user_export['rejected_statements_via_click']:
        if statement in graph_export['nodes']:
            assumptions += '~' + str(statement) + ';'
        else:
            logging.warning('Found non-matching statement ID (%s) in user opinion - No such statement exists for '
                            'issue %s!', str(statement), str(discussion))

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

    json_result = jsonify({'assumptions': assumptions,
                           'kbPrefs': statement_prefs,
                           'rules': rules,
                           'rulePrefs': rule_prefs,
                           'contrariness': '',
                           'link': link_principle,
                           # 'query': query,
                           'semantics': semantics})
    return json_result


def dbas_graph_to_statement_map(dbas_graph):
    """
    Convert the given D-BAS graph export to a SM data structure.

    :param dbas_graph: string as provided by D-BAS graph export 
    :return: SM, node_index_for_id, node_id_for_index

    Along with the SM object, also provides the corresponding mappings
    between D-BAS statement IDs and SM statement indices. 
    """
    logging.debug('Create Statement Map from D-BAS graph...')
    n_nodes = 0
    node_id_for_index = {}
    node_index_for_id = {}
    for n in dbas_graph['nodes']:
        logging.debug('Node: %s', n)
        n_nodes += 1
        node_id_for_index[n_nodes] = n
        node_index_for_id[n] = n_nodes
    logging.debug('node_id_for_index: %s', node_id_for_index)
    logging.debug('node_index_for_id: %s', node_index_for_id)
    statement_map = SM()
    statement_map.n = n_nodes

    for i in dbas_graph['inferences']:
        logging.debug('Inference: %s', i)
        premises = [node_index_for_id[n] for n in i['premises']]
        target = node_index_for_id[i['conclusion']]
        if not i['is_supportive']:
            target = -target
        rid = statement_map.add_inference(premises, target, i['id'])
        if rid != i['id']:
            logging.warning('Added wrong inference id: rid=%s, i[id]=%s', str(rid), str(i['id']))
        else:
            logging.debug('Added inference successfully (rid=%s)!', str(rid))

    for u in dbas_graph['undercuts']:
        logging.debug('Undercut: %s', u)
        premises = [node_index_for_id[n] for n in u['premises']]
        rid = statement_map.add_undercut(premises, u['conclusion'], u['id'])
        if rid != u['id']:
            logging.warning('Added wrong undercut id: rid=' + str(rid) + ', u[id]=' + str(u['id']))
        else:
            logging.debug('Added undercut successfully (rid=%s)!', str(rid))

    return statement_map, node_index_for_id, node_id_for_index


if __name__ == '__main__':
    app.run(threaded=True, port=5101)
