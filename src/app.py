from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request
import json
from pos import Position
from sm import SM
from doj import DoJ


app = Flask(__name__)
CORS(app)  # Set security headers for Web requests


@app.route('/evaluate/all', methods=['GET'])
def evaluate_issue_all():
    """Return a json file with all DoJs and all strengths of reason."""

    issue = request.args.get('issue')
    url = 'http://localhost:4284/export/doj/{}'.format(issue)

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

    # Calculate all DoJs.
    doj = DoJ()
    dojs = {}
    n = sm.n
    for s in range(1, n+1):
        pos = Position(n)
        pos.set_accepted(s)
        doj_s = doj.doj(sm, pos, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
        dojs[node_id_for_index[s]] = doj_s
        print('DoJ(', node_id_for_index[s], '): ', doj_s)

    # Calculate all Reason relations.
    n = sm.n
    reasons = {}
    for p in range(1, n+1):
        reasons_p = []
        for q in range(1, n+1):
            r = doj.reason(sm, p, q, DoJ.REASON_RELATION_1, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
            reasons_p.append(r)
        print('Reasons for ', node_id_for_index[p], ': ', reasons_p)
        reasons[node_id_for_index[p]] = reasons_p

    return jsonify({'dojs': dojs,
                    'reasons': reasons})


@app.route('/evaluate/dojs', methods=['GET'])
def evaluate_issue_dojs():
    """Return a json file with DoJs for the specified statements.

    GET parameter 'issue':
     Is expected to specify the issue for which statement DoJs are calculated.
    GET parameter 'statements':
     May specify a list of statement IDs (separated by comma) for which the DoJs are calculated.
     IDs of statements not existing in the given issue are ignored.
     If not given, DoJs for all statements are calculated."""

    issue = request.args.get('issue')
    url = 'http://localhost:4284/export/doj/{}'.format(issue)

    requested_statements = request.args.get('statements')
    requested_statements_list = None
    if requested_statements:
        requested_statements_list = [int(s) for s in requested_statements.split(',')]

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


if __name__ == '__main__':
    app.run(threaded=True, port=5101)
