#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request
import urllib.parse
import json

from config import *

from dbas import dbas_import
from invalid_request_error import InvalidRequestError

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


def load_dbas_graph_data_v2(discussion_id):
    """
    Get graph data for the given discussion from the D-BAS API v2 export interface.

    :param discussion_id: discussion ID
    :type discussion_id: int
    :return: json string representation of the graph
    """
    base_url = DBAS_BASE_URL + DBAS_API2_BASE_PATH

    # Fetch statements
    params_statements = {DBAS_API2_QUERY_KEY: DBAS_API2_QUERY_STATEMENTS.substitute(discussion_id=discussion_id)}
    query_string_statements = urllib.parse.urlencode(params_statements)
    url_statements = base_url + '?' + query_string_statements
    logging.debug('API_v2 statements URL: %s' % url_statements)

    # Fetch arguments
    params_arguments = {DBAS_API2_QUERY_KEY: DBAS_API2_QUERY_ARGUMENTS.substitute(discussion_id=discussion_id)}
    query_string_arguments = urllib.parse.urlencode(params_arguments)
    url_arguments = base_url + '?' + query_string_arguments
    logging.debug('API_v2 arguments URL: %s' % url_arguments)

    statements_response = urllib.request.urlopen(url_statements).read()
    statements_json = statements_response.decode('utf-8')
    while isinstance(statements_json, str):
        statements_json = json.loads(statements_json)

    arguments_response = urllib.request.urlopen(url_arguments).read()
    arguments_json = arguments_response.decode('utf-8')
    while isinstance(arguments_json, str):
        arguments_json = json.loads(arguments_json)

    dbas_graph = dbas_import.import_dbas_graph_v2(discussion_id, statements_json, arguments_json)
    return dbas_graph


def load_dbas_graph_data_v1(discussion_id):
    """
    Get graph data for the given discussion from the D-BAS API v1 export interface.

    :param discussion_id: discussion ID
    :type discussion_id: int
    :return: json string representation of the graph
    """
    graph_url = DBAS_BASE_URL + DBAS_API1_BASE_PATH + '/' + DBAS_API1_PATH_GRAPH_DATA + '/{}'.format(discussion_id)
    graph_response = urllib.request.urlopen(graph_url).read()
    graph_export = graph_response.decode('utf-8')
    while isinstance(graph_export, str):
        graph_export = json.loads(graph_export)
    dbas_graph = dbas_import.import_dbas_graph(discussion_id, graph_export)
    return dbas_graph


def load_dbas_graph_data(discussion_id):
    if str(DBAS_API_VERSION) == '1':
        return load_dbas_graph_data_v1(discussion_id)
    elif str(DBAS_API_VERSION) == '2':
        return load_dbas_graph_data_v2(discussion_id)
    else:
        logging.warning('invalid DBAS_API_VERSION `%s` (expected `1` or `2`)', str(DBAS_API_VERSION))
        return None


def load_dbas_user_data_v2(discussion_id, user_id):
    """
    Get user opinion data for the given user in the given discussion from the D-BAS API v2 export interface.

    :param discussion_id: discussion ID
    :type discussion_id: int
    :param user_id: user ID
    :type user_id: int
    :return: json string representation of the user opinion
    """
    base_url = DBAS_BASE_URL + DBAS_API2_BASE_PATH

    # Fetch user opinions
    params_user = {DBAS_API2_QUERY_KEY: DBAS_API2_QUERY_OPINION.substitute(user_id=user_id)}
    query_string_user = urllib.parse.urlencode(params_user)
    url_user = base_url + '?' + query_string_user

    user_response = urllib.request.urlopen(url_user).read()
    user_json = user_response.decode('utf-8')
    while isinstance(user_json, str):
        user_json = json.loads(user_json)

    dbas_user = dbas_import.import_dbas_user_v2(discussion_id, user_id, user_json)
    return dbas_user


def load_dbas_user_data_v1(discussion_id, user_id):
    """
    Get user opinion data for the given user in the given discussion from the D-BAS API v1 export interface.

    :param discussion_id: discussion ID
    :type discussion_id: int
    :param user_id: user ID
    :type user_id: int
    :return: json string representation of the user opinion
    """
    user_url = '{}{}/{}/{}/{}'.format(DBAS_BASE_URL, DBAS_API1_BASE_PATH,
                                      DBAS_API1_PATH_USER_DATA, user_id, discussion_id)
    user_response = urllib.request.urlopen(user_url).read()
    user_export = user_response.decode('utf-8')
    while isinstance(user_export, str):
        user_export = json.loads(user_export)
    dbas_user = dbas_import.import_dbas_user(discussion_id, user_id, user_export)
    return dbas_user


def load_dbas_user_data(discussion_id, user_id):
    if str(DBAS_API_VERSION) == '1':
        return load_dbas_user_data_v1(discussion_id, user_id)
    elif str(DBAS_API_VERSION) == '2':
        return load_dbas_user_data_v2(discussion_id, user_id)
    else:
        logging.warning('invalid DBAS_API_VERSION `%s` (expected `1` or `2`)', str(DBAS_API_VERSION))
        return None


@app.route('/evaluate/toastify/dis/<int:discussion>/user/<int:user>',
           defaults={'opinion_strict': 0})
@app.route('/evaluate/toastify/dis/<int:discussion>/user/<int:user>/opinion_strict',
           defaults={'opinion_strict': 1})
@app.route('/evaluate/toastify/dis/<int:discussion>/user/<int:user>/opinion_weak',
           defaults={'opinion_strict': -1})
def toastify(discussion, user, opinion_strict):
    """
    Create a TOAST-formatted graph representation for given user's opinion.

    TOAST documentation: http://toast.arg-tech.org/help/web

    :param discussion: discussion ID
    :type discussion: int
    :param user: user ID
    :type user: int
    :param opinion_strict: indicate whether assumptions shall be implemented as strict (1), defeasible (0), or weak (-1)
    :type opinion_strict: int
    :return: json string
    """
    logging.debug('Create TOAST representation from D-BAS graph...')

    # Get D-BAS graph and user data
    dbas_graph = load_dbas_graph_data(discussion)
    dbas_user = load_dbas_user_data(discussion, user)

    assumptions_type = None
    assumptions_bias = None

    # Pass through opinion strength
    opinion_type = DABASCO_INPUT_KEYWORD_OPINION_STRONG
    if opinion_strict == 1:
        opinion_type = DABASCO_INPUT_KEYWORD_OPINION_STRICT
    elif opinion_strict == -1:
        opinion_type = DABASCO_INPUT_KEYWORD_OPINION_WEAK

    # Set a default semantics
    semantics = TOAST_KEYWORD_SEMANTICS_PREFERRED  # Default semantics

    # Get assumptions and inference rules from D-BAS data
    result = aspic_export_toast.export_toast(dbas_graph,
                                             opinion_type,
                                             dbas_user,
                                             assumptions_type,
                                             assumptions_bias,
                                             semantics)

    return jsonify(result)


@app.route('/evaluate/adfify/dis/<int:discussion>',
           defaults={'user': None, 'opinion_strict': 0})
@app.route('/evaluate/adfify/dis/<int:discussion>/user/<int:user>',
           defaults={'opinion_strict': 0})
@app.route('/evaluate/adfify/dis/<int:discussion>/user/<int:user>/opinion_strict',
           defaults={'opinion_strict': 1})
def adfify(discussion, user, opinion_strict):
    """
    Create a YADF/QADF/DIAMOND-formatted ADF representation for given user's opinion.

    YADF documentation: https://www.dbai.tuwien.ac.at/proj/adf/yadf/

    :param discussion: discussion ID
    :type discussion: int
    :param user: user ID
    :type user: int
    :param opinion_strict: indicate whether assumptions shall be implemented as strict or defeasible
    :type opinion_strict: int
    :return: json string
    """
    logging.debug('Create ADF from D-BAS graph...')

    # Get D-BAS graph and user data
    dbas_graph = load_dbas_graph_data(discussion)
    dbas_user = load_dbas_user_data(discussion, user) if user else None

    # Create ADF
    adf = adf_import_strass.import_adf(dbas_graph, dbas_user, opinion_strict=bool(opinion_strict))

    # Convert to DIAMOND/YADF formatted string
    str_output = adf_export_diamond.export_diamond(adf)
    result = {DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
              DABASCO_OUTPUT_KEYWORD_ADF: str_output}
    if user:
        result[DABASCO_OUTPUT_KEYWORD_USER_ID] = user
    json_result = jsonify(result)
    return json_result


@app.route('/evaluate/dungify/dis/<int:discussion>',
           defaults={'user': None, 'opinion_strict': 0})
@app.route('/evaluate/dungify/dis/<int:discussion>/user/<int:user>',
           defaults={'opinion_strict': 0})
@app.route('/evaluate/dungify/dis/<int:discussion>/user/<int:user>/opinion_strict',
           defaults={'opinion_strict': 1})
def dungify(discussion, user, opinion_strict):
    """
    Create a Dung-style argumentation graph representation for the given discussion.

    :param discussion: discussion ID
    :type discussion: int
    :param user: user ID
    :type user: int
    :param opinion_strict: indicate whether user opinion shall be implemented as strict or defeasible rules
    :type opinion_strict: int
    :return: json string
    """
    logging.debug('Create AF from D-BAS graph...')

    # Get D-BAS graph data
    dbas_graph = load_dbas_graph_data(discussion)

    # Create AF
    dbas_user = load_dbas_user_data(discussion, user) if user else None
    af = af_import_wyner.import_af_wyner(dbas_graph, dbas_user, opinion_strict=bool(opinion_strict))

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
