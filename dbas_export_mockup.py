#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Set security headers for Web requests


@app.route('/export/doj/<int:discussion>')
def export_dummy_discussion(discussion):
    """
    Return a json string with dbas export style data of an example discussion.

    :param discussion: discussion ID
    :return: json string
    """

    nodes = []
    inferences = []
    undercuts = []

    if discussion == 1:
        # Nixon Diamond example discussion
        nodes = [1, 2, 3]
        inferences = [{'id': 1,
                       'premises': [2],
                       'is_supportive': True,
                       'conclusion': 1},
                      {'id': 2,
                       'premises': [3],
                       'is_supportive': False,
                       'conclusion': 1}]

    elif discussion == 2:
        # Extended Nixon Diamond example discussion
        nodes = [1, 2, 3, 4, 5]
        inferences = [{'id': 1,
                       'premises': [2],
                       'is_supportive': True,
                       'conclusion': 1},
                      {'id': 2,
                       'premises': [3],
                       'is_supportive': False,
                       'conclusion': 1},
                      {'id': 3,
                       'premises': [4],
                       'is_supportive': False,
                       'conclusion': 2}]
        undercuts = [{'id': 4,
                      'premises': [5],
                      'conclusion': 2}]

    elif discussion == 3:
        # Town policy debate example discussion
        nodes = [76, 77, 78, 79, 80, 81, 82]
        inferences = [{'id': 65,
                       'premises': [77],
                       'is_supportive': True,
                       'conclusion': 76},
                      {'id': 66,
                       'premises': [78],
                       'is_supportive': False,
                       'conclusion': 76},
                      {'id': 67,
                       'premises': [79],
                       'is_supportive': False,
                       'conclusion': 76},
                      {'id': 68,
                       'premises': [80, 81],
                       'is_supportive': False,
                       'conclusion': 79}]
        undercuts = [{'id': 69,
                      'premises': [82],
                      'conclusion': 65}]

    return jsonify({'nodes': nodes,
                    'inferences': inferences,
                    'undercuts': undercuts})


@app.route('/export/doj_user/<int:user>/<int:discussion>')
def export_dummy_useropinion(user, discussion):
    """
    Return a json string with dbas export style data of an example discussion.

    :param user: user ID
    :param discussion: discussion ID
    :return: json string
    """

    marked_statements = []
    marked_arguments = []
    rejected_arguments = []
    accepted_statements_via_click = []
    rejected_statements_via_click = []

    if discussion == 1:
        # Nixon Diamond example discussion
        if user == 1:
            accepted_statements_via_click = [1]
            rejected_statements_via_click = [3]

    elif discussion == 2:
        # Extended Nixon Diamond example discussion
        if user == 1:
            accepted_statements_via_click = [3, 4]
            rejected_statements_via_click = [5]

    elif discussion == 3:
        # Town policy debate example discussion
        if user == 1:
            accepted_statements_via_click = [76, 77, 80, 81]
            rejected_statements_via_click = [78, 79, 82]

    return jsonify({'marked_statements': marked_statements,
                    'marked_arguments': marked_arguments,
                    'rejected_arguments': rejected_arguments,
                    'accepted_statements_via_click': accepted_statements_via_click,
                    'rejected_statements_via_click': rejected_statements_via_click})

if __name__ == '__main__':
    app.run(threaded=True, port=4284)
