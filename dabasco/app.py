#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request
import json
import itertools

from doj.pos import Position
from doj.sm import SM
from doj.doj import DoJ

from af.af import AF

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
@app.route('/evaluate/doj/<int:dis>/pos1/rej/<string:rej1>/pos2/acc/<string:acc2>/rej/<string:rej2>',
           defaults={'acc1': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/pos2/acc/<string:acc2>/rej/<string:rej2>',
           defaults={'rej1': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/rej/<string:rej2>',
           defaults={'acc2': ''})
@app.route('/evaluate/doj/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/acc/<string:acc2>',
           defaults={'rej2': ''})
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


@app.route('/evaluate/dungify_extended/<int:discussion>')
def dungify_extended(discussion):
    """
    Create a Dung-style argumentation graph representation for the given discussion.

    :param discussion: discussion ID
    :return: json string
    """

    # Get D-BAS graph and user data
    graph_url = 'http://localhost:4284/export/doj/{}'.format(discussion)

    graph_response = urllib.request.urlopen(graph_url).read()
    graph_export = graph_response.decode('utf-8')
    while isinstance(graph_export, str):
        graph_export = json.loads(graph_export)

    # Create AF
    af, argument_for_statement_id, argument_for_inference_id, element_id_for_argument, = \
        dbas_graph_to_argumentation_framework_extended(graph_export)

    # Create output text format
    str_list = []
    for arg in range(af.n):
        if af.A[arg] == AF.DEFINITE_ARGUMENT:
            str_list.append('arg(')
            str_list.append(str(element_id_for_argument[arg]))
            str_list.append(').\n')
    for attacker in range(af.n):
        for target in range(af.n):
            if af.R[attacker][target] == AF.DEFINITE_ATTACK:
                str_list.append('att(')
                str_list.append(str(element_id_for_argument[attacker]))
                str_list.append(',')
                str_list.append(str(element_id_for_argument[target]))
                str_list.append(').\n')

    str_output = ''.join(str_list)

    json_result = jsonify({'discussion_' + str(discussion): str_output})
    return json_result


@app.route('/evaluate/dungify/<int:discussion>')
def dungify(discussion):
    """
    Create a Dung-style argumentation graph representation for the given discussion.

    :param discussion: discussion ID
    :return: json string
    """

    # Get D-BAS graph and user data
    graph_url = 'http://localhost:4284/export/doj/{}'.format(discussion)

    graph_response = urllib.request.urlopen(graph_url).read()
    graph_export = graph_response.decode('utf-8')
    while isinstance(graph_export, str):
        graph_export = json.loads(graph_export)

    # Create AF
    af, argument_for_inference_id, element_id_for_argument, = \
        dbas_graph_to_argumentation_framework(graph_export)

    # Create output text format
    str_list = []
    for arg in range(af.n):
        if af.A[arg] == AF.DEFINITE_ARGUMENT:
            str_list.append('arg(')
            str_list.append(str(element_id_for_argument[arg]))
            str_list.append(').\n')
    for attacker in range(af.n):
        for target in range(af.n):
            if af.R[attacker][target] == AF.DEFINITE_ATTACK:
                str_list.append('att(')
                str_list.append(str(element_id_for_argument[attacker]))
                str_list.append(',')
                str_list.append(str(element_id_for_argument[target]))
                str_list.append(').\n')

    str_output = ''.join(str_list)

    json_result = jsonify({'discussion_' + str(discussion): str_output})
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


def dbas_graph_to_argumentation_framework(dbas_graph):
    """
    Convert the given D-BAS graph export to an argumentation framework.

    The AF representation contains an argument per inference/undercut in the D-BAS graph.

    :param dbas_graph: string as provided by D-BAS graph export
    :return: AF, argument_for_inference_id, element_id_for_argument

    Along with the AF object, also provides the corresponding mappings
    between D-BAS inference IDs and AF argument IDs.
    """
    logging.debug('Create Argumentation Framework from D-BAS graph...')
    current_argument = -1
    element_id_for_argument = {}
    argument_for_inference_id = {}

    # Add one argument for each inference
    for inference in itertools.chain(dbas_graph['inferences'], dbas_graph['undercuts']):
        logging.debug('Inference: %s', inference['id'])
        current_argument += 1
        element_id_for_argument[current_argument] = inference['id']  # inference argument
        argument_for_inference_id[inference['id']] = current_argument

    logging.debug('element_id_for_argument: %s', element_id_for_argument)
    logging.debug('argument_for_inference_id: %s', argument_for_inference_id)
    n_nodes = current_argument+1
    af = AF(n_nodes)

    # Create undercut attacks
    for inference in dbas_graph['undercuts']:
        inference_argument = argument_for_inference_id[inference['id']]
        target_argument = argument_for_inference_id[inference['conclusion']]
        af.set_attack(inference_argument, target_argument, AF.DEFINITE_ATTACK)

    # Create rebutting and undermining attacks
    for inference in dbas_graph['inferences']:
        inference_argument = argument_for_inference_id[inference['id']]
        conclusion = inference['conclusion']

        # Create rebutting attacks
        for inference2 in dbas_graph['inferences']:
            inference2_argument = argument_for_inference_id[inference2['id']]
            conclusion2 = inference2['conclusion']
            if conclusion == conclusion2:
                if inference['is_supportive'] != inference2['is_supportive']:
                    af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference2_argument, inference_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks
        for inference2 in itertools.chain(dbas_graph['inferences'], dbas_graph['undercuts']):
            inference2_argument = argument_for_inference_id[inference2['id']]
            if not inference['is_supportive']:  # TODO: can a premise be a negated statement? If yes, cover that case!!
                for premise2 in inference2['premises']:
                    if conclusion == premise2:
                        af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)

    return af, argument_for_inference_id, element_id_for_argument


def dbas_graph_to_argumentation_framework_extended(dbas_graph):
    """
    Convert the given D-BAS graph export to an argumentation framework.

    The AF representation contains an argument per inference/undercut in the D-BAS graph
    and two arguments for each statement in the D-BAS graph (negated and not-negated).

    :param dbas_graph: string as provided by D-BAS graph export
    :return: AF, argument_for_statement_id, argument_for_inference_id, element_id_for_argument

    Along with the AF object, also provides the corresponding mappings
    between D-BAS statement/inference IDs and AF argument IDs.
    """
    logging.debug('Create Argumentation Framework from D-BAS graph...')
    current_argument = -1
    element_id_for_argument = {}
    argument_for_statement_id = {}
    argument_for_inference_id = {}

    # Add two arguments for each statement
    for statement in dbas_graph['nodes']:
        logging.debug('Statement: %s', statement)
        current_argument += 1
        element_id_for_argument[current_argument] = statement  # statement argument
        argument_for_statement_id[statement] = current_argument
        current_argument += 1
        element_id_for_argument[current_argument] = -statement  # negated statement argument

    # Add one argument for each inference
    for inference in itertools.chain(dbas_graph['inferences'], dbas_graph['undercuts']):
        logging.debug('Inference: %s', inference['id'])
        current_argument += 1
        element_id_for_argument[current_argument] = 'r' + str(inference['id'])  # inference argument
        argument_for_inference_id[inference['id']] = current_argument

    logging.debug('element_id_for_argument: %s', element_id_for_argument)
    logging.debug('argument_for_statement_id: %s', argument_for_statement_id)
    logging.debug('argument_for_inference_id: %s', argument_for_inference_id)
    n_nodes = current_argument+1
    af = AF(n_nodes)

    # Create attacks between statement arguments
    for statement in dbas_graph['nodes']:
        statement_argument = argument_for_statement_id[statement]
        negated_statement_argument = statement_argument+1
        af.set_attack(statement_argument, negated_statement_argument, AF.DEFINITE_ATTACK)
        af.set_attack(negated_statement_argument, statement_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks from statement arguments against inference premises
        for inference2 in itertools.chain(dbas_graph['inferences'], dbas_graph['undercuts']):
            inference2_argument = argument_for_inference_id[inference2['id']]
            for premise2 in inference2['premises']:
                # TODO: can a premise be a negated statement? If yes, cover that case, too!!
                if statement == premise2:
                    af.set_attack(negated_statement_argument, inference2_argument, AF.DEFINITE_ATTACK)

    # Create undercut attacks
    for inference in dbas_graph['undercuts']:
        inference_argument = argument_for_inference_id[inference['id']]
        target_argument = argument_for_inference_id[inference['conclusion']]
        af.set_attack(inference_argument, target_argument, AF.DEFINITE_ATTACK)

    # Create rebutting and undermining attacks
    for inference in dbas_graph['inferences']:
        inference_argument = argument_for_inference_id[inference['id']]
        conclusion = inference['conclusion']

        # Attack the statement argument that contradicts the conclusion
        eliminated_statement_argument = argument_for_statement_id[conclusion]
        if inference['is_supportive']:
            eliminated_statement_argument += 1  # In case of a supportive inference, attack the negated statement
        af.set_attack(inference_argument, eliminated_statement_argument, AF.DEFINITE_ATTACK)

        # Create rebutting attacks
        for inference2 in dbas_graph['inferences']:
            inference2_argument = argument_for_inference_id[inference2['id']]
            conclusion2 = inference2['conclusion']
            if conclusion == conclusion2:
                if inference['is_supportive'] != inference2['is_supportive']:
                    af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference2_argument, inference_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks
        for inference2 in itertools.chain(dbas_graph['inferences'], dbas_graph['undercuts']):
            inference2_argument = argument_for_inference_id[inference2['id']]
            if not inference['is_supportive']:  # TODO: can a premise be a negated statement? If yes, cover that case!!
                for premise2 in inference2['premises']:
                    if conclusion == premise2:
                        af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)

    return af, argument_for_statement_id, argument_for_inference_id, element_id_for_argument


if __name__ == '__main__':
    app.run(threaded=True, port=5101)
