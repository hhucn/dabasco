#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request
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
    dbas_user = load_dbas_user_data(discussion, user)

    # Create ADF
    adf = adf_import_strass.import_adf(dbas_graph, dbas_user, opinion_strict=bool(opinion_strict))

    # Convert to DIAMOND/YADF formatted string
    output_string = adf_export_diamond.export_diamond(adf)
    json_result = jsonify({DABASCO_OUTPUT_KEYWORD_DISCUSSION_ID: discussion,
                           DABASCO_OUTPUT_KEYWORD_USER_ID: user,
                           DABASCO_OUTPUT_KEYWORD_ADF: output_string})
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
