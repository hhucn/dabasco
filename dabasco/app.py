#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request
import json

from config import *

from dbas import dbas_import
from invalid_request_error import InvalidRequestError

from doj.pos import Position
from doj.sm import SM
from doj.doj import DoJ
import doj.import_dbas as sm_import

import adf.import_strass as adf_import_strass
import adf.export_diamond as adf_export_diamond

import af.import_wyner as af_import_wyner
import af.export_aspartix as af_export_aspartix

import aspic.export_toast as aspic_export_toast

from os import path
import logging
import logging.config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('root')

app = Flask(__name__)
CORS(app)  # Set security headers for Web requests


def load_dbas_graph_data(discussion_id):
    """
    Get graph data for the given discussion from the D-BAS export interface.

    :param discussion_id: discussion ID
    :type discussion_id: int
    :return: json string representation of the graph
    """
    graph_url = DBAS_BASE_URL + '/' + DBAS_PATH_GRAPH_DATA + '/{}'.format(discussion_id)
    graph_response = urllib.request.urlopen(graph_url).read()
    graph_export = graph_response.decode('utf-8')
    while isinstance(graph_export, str):
        graph_export = json.loads(graph_export)
    dbas_graph = dbas_import.import_dbas_graph(discussion_id, graph_export)
    return dbas_graph


def load_dbas_user_data(discussion_id, user_id):
    """
    Get user opinion data for the given user in the given discussion from the D-BAS export interface.

    :param discussion_id: discussion ID
    :type discussion_id: int
    :param user_id: user ID
    :type user_id: int
    :return: json string representation of the user opinion
    """
    user_url = DBAS_BASE_URL + '/' + DBAS_PATH_USER_DATA + '/{}/{}'.format(user_id, discussion_id)
    user_response = urllib.request.urlopen(user_url).read()
    user_export = user_response.decode('utf-8')
    while isinstance(user_export, str):
        user_export = json.loads(user_export)
    dbas_user = dbas_import.import_dbas_user(discussion_id, user_id, user_export)
    return dbas_user


@app.route('/evaluate/reasons/dis/<int:discussion>/for/<int:s1>/by/<int:s2>')
@app.route('/evaluate/reasons/dis/<int:discussion>/by/<int:s2>/for/<int:s1>')
@app.route('/evaluate/reasons/dis/<int:discussion>/for/<int:s1>',
           defaults={'s2': None})
@app.route('/evaluate/reasons/dis/<int:discussion>/by/<int:s2>',
           defaults={'s1': None})
@app.route('/evaluate/reasons/dis/<int:discussion>',
           defaults={'s1': None, 's2': None})
def evaluate_issue_reasons(discussion, s1, s2):
    """
    Return a json string with strengths of reason for the given discussion and the specified statements.

    IDs of statements that do not exist in the given discussion are ignored.
    If no statements are given, strengths of reason for all statements in the discussion are calculated.

    :param discussion: discussion ID
    :type discussion: int
    :param s1: statement ID, calculate reasons for/against this
    :type s1: int
    :param s2: statement ID, calculate reasons by/from this
    :type s2: int
    :return: json string
    """

    # Get D-BAS graph
    dbas_graph = load_dbas_graph_data(discussion)

    # Create statement map from data
    statement_map = sm_import.import_statement_map(dbas_graph)

    # Calculate all Reason relations
    doj = DoJ()
    n = statement_map.n
    reasons = {}

    # Use the specified statement for s1 resp. s2, or all statements if none is specified
    s1_range = [statement_map.node_index_for_id[s1]] \
        if (s1 and s1 in statement_map.node_index_for_id) \
        else range(1, n + 1)
    s2_range = [statement_map.node_index_for_id[s2]] \
        if (s2 and s2 in statement_map.node_index_for_id) \
        else range(1, n + 1)

    for s1 in s1_range:
        reasons_s1 = {}
        for s2 in s2_range:
            r = doj.reason(statement_map, s1, s2, DoJ.REASON_RELATION_1, DoJ.DOJ_RECALL,
                           SM.COHERENCE_DEDUCTIVE_INFERENCES)
            reasons_s1[statement_map.node_id_for_index[s2]] = r
        reasons['for ' + str(statement_map.node_id_for_index[s1])] = reasons_s1

    json_result = jsonify({DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
                           DABASCO_OUTPUT_KEYWORD_REASONS: reasons})
    return json_result


@app.route('/evaluate/dojs/dis/<int:discussion>/stats/<string:statements>')
@app.route('/evaluate/dojs/dis/<int:discussion>',
           defaults={'statements': ''})
def evaluate_issue_dojs(discussion, statements):
    """
    Return a json string with DoJs for the specified statements.

    IDs of statements that do not exist in the given discussion are ignored.
    If no statements are given, DoJs for all statements in the discussion are calculated.

    :param discussion: discussion ID
    :type discussion: int
    :param statements: comma separated string of statements for which the DoJs are calculated.
    :type statements: str
    :return: json string
    """

    # Get D-BAS graph
    dbas_graph = load_dbas_graph_data(discussion)

    # Create statement map from data
    statement_map = sm_import.import_statement_map(dbas_graph)

    requested_statements_list = None
    if statements:
        requested_statements_list = [int(s) for s in statements.split(',')]

    # Calculate the DoJs of all requested statements
    doj = DoJ()
    dojs = {}
    n = statement_map.n
    if requested_statements_list:
        requested_statements_list = [i for i in requested_statements_list if i in statement_map.node_index_for_id]
        query_requested_statements = [statement_map.node_index_for_id[i] for i in requested_statements_list]
    else:
        # Default: calculate all DoJs ([1,...,n]) if no specific statements were requested.
        query_requested_statements = range(1, n + 1)
    for s in query_requested_statements:
        pos = Position(n)
        pos.set_accepted(s)
        doj_s = doj.doj(statement_map, pos, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)
        dojs[statement_map.node_id_for_index[s]] = doj_s
        logging.debug('DoJ(%s): %s', statement_map.node_id_for_index[s], doj_s)

    json_result = jsonify({DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
                           DABASCO_OUTPUT_KEYWORD_DEGREES_OF_JUSTIFICATION: dojs})
    return json_result


@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/acc/<string:acc2>/'
           'rej/<string:rej2>')
@app.route('/evaluate/doj/dis/<int:dis>/pos1/rej/<string:rej1>/pos2/acc/<string:acc2>/rej/<string:rej2>',
           defaults={'acc1': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/pos2/acc/<string:acc2>/rej/<string:rej2>',
           defaults={'rej1': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/rej/<string:rej2>',
           defaults={'acc2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2/acc/<string:acc2>',
           defaults={'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/pos2/acc/<string:acc2>/rej/<string:rej2>',
           defaults={'acc1': '', 'rej1': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/rej/<string:rej1>/pos2/rej/<string:rej2>',
           defaults={'acc1': '', 'acc2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/rej/<string:rej1>/pos2/acc/<string:acc2>',
           defaults={'acc1': '', 'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/pos2/rej/<string:rej2>',
           defaults={'rej1': '', 'acc2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/pos2/acc/<string:acc2>',
           defaults={'rej1': '', 'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/rej/<string:rej1>/pos2',
           defaults={'acc2': '', 'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/pos2/rej/<string:rej2>',
           defaults={'acc1': '', 'rej1': '', 'acc2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/pos2/acc/<string:acc2>',
           defaults={'acc1': '', 'rej1': '', 'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/rej/<string:rej1>/pos2',
           defaults={'acc1': '', 'acc2': '', 'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/acc/<string:acc1>/pos2',
           defaults={'rej1': '', 'acc2': '', 'rej2': ''})
@app.route('/evaluate/doj/dis/<int:dis>/pos1/pos2',
           defaults={'acc1': '', 'rej1': '', 'acc2': '', 'rej2': ''})
def evaluate_issue_conditional_doj(dis, acc1, rej1, acc2, rej2):
    """
    Return a json string with the DoJ of position pos1 given position pos2.

    IDs of statements that do not exist in the given discussion are ignored.

    :param dis: discussion ID
    :type dis: int
    :param acc1: (optional) comma separated string of statement IDs which are accepted in position pos1.
    :type acc1: str
    :param rej1: (optional) comma separated string of statement IDs which are rejected in position pos1.
    :type rej1: str
    :param acc2: (optional) comma separated string of statement IDs which are accepted in conditional position pos2.
    :type acc2: str
    :param rej2: (optional) comma separated string of statement IDs which are rejected in conditional position pos2.
    :type rej2: str
    :return: json string
    """

    # Get D-BAS graph
    dbas_graph = load_dbas_graph_data(dis)

    # Create statement map from data
    statement_map = sm_import.import_statement_map(dbas_graph)

    # Process input positions
    n = statement_map.n
    pos1 = Position(n)
    if acc1:
        for s in acc1.split(','):
            if int(s) in statement_map.node_index_for_id:
                pos1.set_accepted(statement_map.node_index_for_id[int(s)])
    if rej1:
        for s in rej1.split(','):
            if int(s) in statement_map.node_index_for_id:
                pos1.set_rejected(statement_map.node_index_for_id[int(s)])

    pos2 = Position(n)
    if acc2:
        for s in acc2.split(','):
            if int(s) in statement_map.node_index_for_id:
                pos2.set_accepted(statement_map.node_index_for_id[int(s)])
    if rej2:
        for s in rej2.split(','):
            if int(s) in statement_map.node_index_for_id:
                pos2.set_rejected(statement_map.node_index_for_id[int(s)])

    # Calculate the conditional DoJ of position 1 given position 2.
    doj = DoJ()
    result = doj.doj_conditional(statement_map, pos1, pos2, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)

    json_result = jsonify({DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: dis,
                           DABASCO_OUTPUT_KEYWORD_DEGREE_OF_JUSTIFICATION: result})
    return json_result


@app.route('/evaluate/doj/dis/<int:discussion>/user/<int:user>')
def evaluate_issue_doj_user_position(discussion, user):
    """
    Return a json string with the DoJ of the opinion of the given user.

    :param discussion: discussion ID
    :type discussion: int
    :param user: user ID
    :type user: int
    :return: json string
    """

    # Get D-BAS graph and user data
    dbas_graph = load_dbas_graph_data(discussion)
    dbas_user = load_dbas_user_data(discussion, user)

    # Create statement map from data
    statement_map = sm_import.import_statement_map(dbas_graph)

    # Process input position
    n = statement_map.n
    pos1 = Position(n)
    for statement in dbas_user.accepted_statements_explicit:
        pos1.set_accepted(statement_map.node_index_for_id[int(statement)])
    for statement in dbas_user.accepted_statements_implicit:
        pos1.set_accepted(statement_map.node_index_for_id[int(statement)])
    for statement in dbas_user.rejected_statements_implicit:
        pos1.set_rejected(statement_map.node_index_for_id[int(statement)])

    # Calculate the conditional DoJ of position 1 given position 2.
    doj = DoJ()
    result = doj.doj(statement_map, pos1, DoJ.DOJ_RECALL, SM.COHERENCE_DEDUCTIVE_INFERENCES)

    json_result = jsonify({DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
                           DABASCO_OUTPUT_KEYWORD_USER_ID: user,
                           DABASCO_OUTPUT_KEYWORD_DEGREE_OF_JUSTIFICATION: result})
    return json_result


@app.route('/evaluate/toastify', methods=['GET'])
def toastify():
    """
    Create a TOAST-formatted graph representation for given user's opinion.

    TOAST documentation: http://toast.arg-tech.org/help/web

    :return: json string
    """
    logging.debug('Create TOAST representation from D-BAS graph...')

    json_params = request.get_json()

    # Respond with error if no parameters in body
    if not json_params:
        raise InvalidRequestError('Missing request parameters', status_code=400)

    # The 'discussion' field is mandatory, respond with error if missing.
    if DABASCO_INPUT_KEYWORD_DISCUSSION_ID not in json_params:
        raise InvalidRequestError('Field "discussion" is required', status_code=400)

    discussion = int(json_params[DABASCO_INPUT_KEYWORD_DISCUSSION_ID])
    dbas_graph = load_dbas_graph_data(discussion)

    opinion_type = None
    opinion = None
    if DABASCO_INPUT_KEYWORD_OPINION in json_params:
        opinion_params = json_params[DABASCO_INPUT_KEYWORD_OPINION]
        if isinstance(opinion_params, dict):
            if (DABASCO_INPUT_KEYWORD_TYPE in opinion_params and
                opinion_params[DABASCO_INPUT_KEYWORD_TYPE] in [DABASCO_INPUT_KEYWORD_OPINION_WEAK,
                                                               DABASCO_INPUT_KEYWORD_OPINION_STRONG,
                                                               DABASCO_INPUT_KEYWORD_OPINION_STRICT]):
                opinion_type = opinion_params[DABASCO_INPUT_KEYWORD_TYPE]
            if opinion_type:
                if DABASCO_INPUT_KEYWORD_USER in opinion_params:
                    user_id = int(opinion_params[DABASCO_INPUT_KEYWORD_USER])
                    opinion = load_dbas_user_data(discussion, user_id)

    assumptions_type = None
    assumptions_bias = None
    if DABASCO_INPUT_KEYWORD_ASSUMPTIONS in json_params:
        assumptions = json_params[DABASCO_INPUT_KEYWORD_ASSUMPTIONS]
        if isinstance(assumptions, dict):
            if (DABASCO_INPUT_KEYWORD_TYPE in assumptions and
                    assumptions[DABASCO_INPUT_KEYWORD_TYPE] in [DABASCO_INPUT_KEYWORD_OPINION_WEAK,
                                                                DABASCO_INPUT_KEYWORD_OPINION_STRONG]):
                assumptions_type = assumptions[DABASCO_INPUT_KEYWORD_TYPE]
            if (DABASCO_INPUT_KEYWORD_BIAS in assumptions and
                    assumptions[DABASCO_INPUT_KEYWORD_BIAS] in [DABASCO_INPUT_KEYWORD_POSITIVE_BIAS,
                                                                DABASCO_INPUT_KEYWORD_NEGATIVE_BIAS]):
                assumptions_bias = assumptions[DABASCO_INPUT_KEYWORD_BIAS]

    # Pass through given semantics, or set a default semantics
    semantics = TOAST_KEYWORD_SEMANTICS_PREFERRED  # Default semantics
    if DABASCO_INPUT_KEYWORD_SEMANTICS in json_params:
        semantics = str(json_params[DABASCO_INPUT_KEYWORD_SEMANTICS])

    # Get assumptions and inference rules from D-BAS data
    result = aspic_export_toast.export_toast(dbas_graph,
                                             opinion_type,
                                             opinion,
                                             assumptions_type,
                                             assumptions_bias,
                                             semantics)

    return jsonify(result)


@app.route('/evaluate/adfify/dis/<int:discussion>/user/<int:user>',
           defaults={'assumptions_strict': 0})
@app.route('/evaluate/adfify/dis/<int:discussion>/user/<int:user>/assumptions_strict',
           defaults={'assumptions_strict': 1})
def adfify(discussion, user, assumptions_strict):
    """
    Create a YADF/QADF/DIAMOND-formatted ADF representation for given user's opinion.

    YADF documentation: https://www.dbai.tuwien.ac.at/proj/adf/yadf/

    :param discussion: discussion ID
    :type discussion: int
    :param user: user ID
    :type user: int
    :param assumptions_strict: indicate whether assumptions shall be implemented as strict or defeasible
    :type assumptions_strict: int
    :return: json string
    """
    logging.debug('Create ADF from D-BAS graph...')

    # Get D-BAS graph and user data
    dbas_graph = load_dbas_graph_data(discussion)
    dbas_user = load_dbas_user_data(discussion, user)

    # Create ADF
    adf = adf_import_strass.import_adf(dbas_graph, dbas_user, bool(assumptions_strict))

    # Convert to DIAMOND/YADF formatted string
    output_string = adf_export_diamond.export_diamond(adf)
    json_result = jsonify({DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
                           DABASCO_OUTPUT_KEYWORD_USER_ID: user,
                           DABASCO_OUTPUT_KEYWORD_ADF: output_string})
    return json_result


@app.route('/evaluate/dungify/dis/<int:discussion>',
           defaults={'user': None, 'assumptions_strict': 0})
@app.route('/evaluate/dungify/dis/<int:discussion>/user/<int:user>',
           defaults={'assumptions_strict': 0})
@app.route('/evaluate/dungify/dis/<int:discussion>/user/<int:user>/assumptions_strict',
           defaults={'assumptions_strict': 1})
def dungify(discussion, user, assumptions_strict):
    """
    Create a Dung-style argumentation graph representation for the given discussion.

    :param discussion: discussion ID
    :type discussion: int
    :param user: user ID
    :type user: int
    :param assumptions_strict: indicate whether user opinion shall be implemented as strict or defeasible rules
    :type assumptions_strict: int
    :return: json string
    """
    logging.debug('Create AF from D-BAS graph...')

    # Get D-BAS graph data
    dbas_graph = load_dbas_graph_data(discussion)

    # Create AF
    dbas_user = load_dbas_user_data(discussion, user) if user else None
    af = af_import_wyner.import_af_wyner(dbas_graph, dbas_user, assumptions_strict=bool(assumptions_strict))

    logging.debug(str(af.name_for_argument))
    logging.debug(str(af.argument_for_name))

    # Create output text format
    str_output = af_export_aspartix.export_aspartix(af)
    result = {DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
              DABASCO_OUTPUT_KEYWORD_AF: str_output}
    if user:
        result[DABASCO_OUTPUT_KEYWORD_USER_ID] = user
    json_result = jsonify(result)
    return json_result


@app.errorhandler(InvalidRequestError)
def handle_invalid_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(threaded=True, port=5101)
