from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request
import json
from doj.pos import Position
from doj.sm import SM
from doj.doj import DoJ


app = Flask(__name__)
CORS(app)  # Set security headers for Web requests


@app.route('/evaluate/reasons/<int:discussion>')
def evaluate_issue_reasons(discussion):
    """
    Return a json string with all strengths of reason for the given discussion.
    
    :param discussion: discussion ID 
    :return: json string
    """

    url = 'http://localhost:4284/export/doj/{}'.format(discussion)

    response = urllib.request.urlopen(url).read()
    export = response.decode('utf-8')

    while isinstance(export, str):
        export = json.loads(export)

    # Create statement map from data.
    n_nodes = 0
    node_id_for_index = {}
    node_index_for_id = {}
    for n in export['nodes']:
        print(n)
        n_nodes += 1
        node_id_for_index[n_nodes] = n
        node_index_for_id[n] = n_nodes
    print(node_id_for_index)
    print(node_index_for_id)
    sm = SM()
    sm.n = n_nodes

    print()
    print()
    for i in export['inferences']:
        print(i)
        premises = [node_index_for_id[n] for n in i['premises']]
        target = node_index_for_id[i['conclusion']]
        if not i['is_supportive']:
            target = -target
        rid = sm.add_inference(premises, target, i['id'])
        if rid != i['id']:
            print('Added wrong inference id: rid='+str(rid)+', i[id]='+str(i['id']))
        else:
            print('Added successfully!')

    print()
    print()
    for u in export['undercuts']:
        print(u)
        premises = [node_index_for_id[n] for n in u['premises']]
        rid = sm.add_undercut(premises, u['conclusion'], u['id'])
        if rid != u['id']:
            print('Added wrong undercut id: rid='+str(rid)+', u[id]='+str(u['id']))
        else:
            print('Added successfully!')

    print()
    print()
    sm.pretty_print()
    print()
    print()

    # Calculate all Reason relations.
    doj = DoJ()
    n = sm.n
    reasons = {}
    for p in range(1, n+1):
        reasons_p = []
        for q in range(1, n+1):
            r = doj.reason(sm, p, q, DoJ.REASON_RELATION_1, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
            reasons_p.append(r)
        print('Reasons for ', node_id_for_index[p], ': ', reasons_p)
        reasons[node_id_for_index[p]] = reasons_p

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

    # Create statement map from data.
    n_nodes = 0
    node_id_for_index = {}
    node_index_for_id = {}
    for n in export['nodes']:
        print(n)
        n_nodes += 1
        node_id_for_index[n_nodes] = n
        node_index_for_id[n] = n_nodes
    print(node_id_for_index)
    print(node_index_for_id)
    sm = SM()
    sm.n = n_nodes

    print()
    print()
    for i in export['inferences']:
        print(i)
        premises = [node_index_for_id[n] for n in i['premises']]
        target = node_index_for_id[i['conclusion']]
        if not i['is_supportive']:
            target = -target
        rid = sm.add_inference(premises, target, i['id'])
        if rid != i['id']:
            print('Added wrong inference id: rid='+str(rid)+', i[id]='+str(i['id']))
        else:
            print('Added successfully!')

    print()
    print()
    for u in export['undercuts']:
        print(u)
        premises = [node_index_for_id[n] for n in u['premises']]
        rid = sm.add_undercut(premises, u['conclusion'], u['id'])
        if rid != u['id']:
            print('Added wrong undercut id: rid='+str(rid)+', u[id]='+str(u['id']))
        else:
            print('Added successfully!')

    print()
    print()
    sm.pretty_print()
    print()
    print()

    # Calculate the DoJs of all requested statements.
    doj = DoJ()
    dojs = {}
    n = sm.n
    if requested_statements_list:
        requested_statements_list = [i for i in requested_statements_list if i in node_index_for_id]
        query_requested_statements = [node_index_for_id[i] for i in requested_statements_list]
    else:
        # Default: calculate all DoJs ([1,...,n]) if no specific statements were requested.
        query_requested_statements = range(1, n + 1)
    for s in query_requested_statements:
        pos = Position(n)
        pos.set_accepted(s)
        doj_s = doj.doj(sm, pos, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
        dojs[node_id_for_index[s]] = doj_s
        print('DoJ(', node_id_for_index[s], '): ', doj_s)

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

    # Create statement map from data.
    n_nodes = 0
    node_id_for_index = {}
    node_index_for_id = {}
    for n in export['nodes']:
        print(n)
        n_nodes += 1
        node_id_for_index[n_nodes] = n
        node_index_for_id[n] = n_nodes
    print(node_id_for_index)
    print(node_index_for_id)
    sm = SM()
    sm.n = n_nodes

    print()
    print()
    for i in export['inferences']:
        print(i)
        premises = [node_index_for_id[n] for n in i['premises']]
        target = node_index_for_id[i['conclusion']]
        if not i['is_supportive']:
            target = -target
        rid = sm.add_inference(premises, target, i['id'])
        if rid != i['id']:
            print('Added wrong inference id: rid='+str(rid)+', i[id]='+str(i['id']))
        else:
            print('Added successfully!')

    print()
    print()
    for u in export['undercuts']:
        print(u)
        premises = [node_index_for_id[n] for n in u['premises']]
        rid = sm.add_undercut(premises, u['conclusion'], u['id'])
        if rid != u['id']:
            print('Added wrong undercut id: rid='+str(rid)+', u[id]='+str(u['id']))
        else:
            print('Added successfully!')

    print()
    print()
    sm.pretty_print()
    print()
    print()

    # Process input positions
    n = sm.n
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
    result = doj.doj_conditional(sm, pos1, pos2, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)

    return jsonify({'doj': result})


if __name__ == '__main__':
    app.run(threaded=True, port=5101)
