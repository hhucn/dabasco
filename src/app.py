from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request
import json
import math
from pos import Position
from sm import SM
from doj import DoJ

app = Flask(__name__)
CORS(app) # Set security headers for Web Requests

@app.route('/evaluate/all', methods=['GET'])
def evaluate_issue_all():
    '''Return a json file with all DoJs and all strengths of reason.'''
    
    issue = request.args.get('issue')
    url = "http://localhost:4284/export/doj/"+str(issue)
    print(url)
    response = urllib.request.urlopen(url).read()
    export = json.loads(response.decode("utf-8"))

    # Create statement map from data.
    nNodes = 0
    nodeIDForIndex = {}
    nodeIndexForID = {}
    for n in export["nodes"]:
        print(n)
        nNodes += 1
        nodeIDForIndex[nNodes] = n
        nodeIndexForID[n] = nNodes
    print(nodeIDForIndex)
    print(nodeIndexForID)
    sm = SM()
    sm.n = nNodes

    print()
    print()
    for i in export["inferences"]:
        print(i)
        premises = [nodeIndexForID[n] for n in i['premises']]
        target = nodeIndexForID[i['conclusion']]
        if i['is_supportive'] == False:
            target = -target
        rid = sm.addInference(premises, target, i['id'])
        if (rid != i['id']):
            print('Falsche id: rid='+str(rid)+', i[id]='+str(i['id']))
        else:
            print('added successfully!')

    print()
    print()
    for u in export["undercuts"]:
        print(u)
        premises = [nodeIndexForID[n] for n in u['premises']]
        rid = sm.addUndercut(premises, u['conclusion'], u['id'])
        if (rid != u['id']):
            print('Falsche id: rid='+str(rid)+', u[id]='+str(u['id']))
        else:
            print('added successfully!')

    print()
    print()
    sm.prettyPrint()
    print()
    print()

    # Calculate all DoJs.
    doj = DoJ()
    dojs = {}
    n = sm.n
    for s in range(1,n+1):
        pos = Position(n)
        pos.setAccepted(s)
        doj_s = doj.doj(sm,pos,DoJ.DOJ_RECALL,SM.COHERENCE_DEDUCTIVE_INFERENCES)
        dojs[nodeIDForIndex[s]] = doj_s
        print('DoJ(',nodeIDForIndex[s],'): ',doj_s)

    # Calculate all Reason relations.
    n = sm.n
    reasons = {}
    for p in range(1,n+1):
        reasons_p = []
        for q in range(1,n+1):
            r = doj.reason(sm,p,q,DoJ.REASON_RELATION_1,DoJ.DOJ_RECALL,SM.COHERENCE_DEDUCTIVE_INFERENCES)
            reasons_p.append(r)
        print('Reasons for ',nodeIDForIndex[p],': ',reasons_p)
        reasons[nodeIDForIndex[p]] = reasons_p
    
    return jsonify({'dojs': dojs,
                    'reasons': reasons})


if __name__ == '__main__':
    app.run(threaded=True,port=5101)

