import itertools

from .af_graph import AF
from dbas_graph import DBASGraph

import logging
logger = logging.getLogger('root')


def import_af_wyner(dbas_graph, strict_inferences):
    """
    Create an AF representation of the given discussion.

    The AF representation contains an argument per inference/undercut in the D-BAS graph
    and two arguments for each statement in the D-BAS graph (negated and not-negated).

    :param dbas_graph: DBASGraph to be used for AF generation
    :type dbas_graph: DBASGraph
    :return: AF
    """
    logging.debug('Create Argumentation Framework from D-BAS graph...')
    current_argument = -1
    element_id_for_argument = {}
    argument_for_statement_id = {}
    argument_for_inference_id = {}

    # Add two arguments for each statement
    for statement in dbas_graph.statements:
        logging.debug('Statement: %s', statement)
        current_argument += 1
        element_id_for_argument[current_argument] = statement  # statement argument
        argument_for_statement_id[statement] = current_argument
        current_argument += 1
        element_id_for_argument[current_argument] = -statement  # negated statement argument

    # Add one argument for each inference
    for inference_id in itertools.chain(dbas_graph.inferences, dbas_graph.undercuts):
        logging.debug('Inference: %s', inference_id)
        current_argument += 1
        element_id_for_argument[current_argument] = 'r' + str(inference_id)  # inference argument
        argument_for_inference_id[inference_id] = current_argument

    n_nodes = current_argument+1
    af = AF(n_nodes)
    for arg in element_id_for_argument:
        af.set_argument_name(arg, element_id_for_argument[arg])

    # Create attacks between statement arguments
    for statement in dbas_graph.statements:
        statement_argument = argument_for_statement_id[statement]
        negated_statement_argument = statement_argument+1
        af.set_attack(statement_argument, negated_statement_argument, AF.DEFINITE_ATTACK)
        af.set_attack(negated_statement_argument, statement_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks from statement arguments against inference premises
        for inference2_id, inference2 in itertools.chain(dbas_graph.inferences.items(), dbas_graph.undercuts.items()):
            inference2_argument = argument_for_inference_id[inference2_id]
            for premise2 in inference2.premises:
                if statement == premise2:
                    af.set_attack(negated_statement_argument, inference2_argument, AF.DEFINITE_ATTACK)

    # Create undercut attacks
    for inference_id in dbas_graph.undercuts:
        inference = dbas_graph.undercuts[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        target_argument = argument_for_inference_id[inference.conclusion]
        af.set_attack(inference_argument, target_argument, AF.DEFINITE_ATTACK)

    # Create rebutting attacks
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        conclusion = inference.conclusion

        # Attack against the statement argument that contradicts the conclusion
        eliminated_statement_argument = argument_for_statement_id[conclusion]
        if inference.is_supportive:
            eliminated_statement_argument += 1  # In case of a supportive inference, attack the negated statement
        af.set_attack(inference_argument, eliminated_statement_argument, AF.DEFINITE_ATTACK)
        if not strict_inferences:
            # Statement arguments can only rebut defeasible inferences, not strict inferences
            af.set_attack(eliminated_statement_argument, inference_argument, AF.DEFINITE_ATTACK)

    return af


def import_af_small(dbas_graph):
    """
    Create an AF representation of the given discussion.

    The AF representation contains an argument per inference/undercut in the D-BAS graph.

    :param dbas_graph: DBASGraph to be used for AF generation
    :type dbas_graph: DBASGraph
    :return: AF
    """
    logging.debug('Create Argumentation Framework from D-BAS graph...')
    current_argument = -1
    element_id_for_argument = {}
    argument_for_inference_id = {}

    # Add one argument for each inference
    for inference_id in itertools.chain(dbas_graph.inferences, dbas_graph.undercuts):
        logging.debug('Inference: %s', inference_id)
        current_argument += 1
        element_id_for_argument[current_argument] = 'r' + str(inference_id)  # inference argument
        argument_for_inference_id[inference_id] = current_argument

    logging.debug('element_id_for_argument: %s', element_id_for_argument)
    logging.debug('argument_for_inference_id: %s', argument_for_inference_id)
    n_nodes = current_argument+1
    af = AF(n_nodes)
    for arg in element_id_for_argument:
        af.set_argument_name(arg, element_id_for_argument[arg])

    # Create undercut attacks
    for inference_id in dbas_graph.undercuts:
        inference = dbas_graph.undercuts[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        target_argument = argument_for_inference_id[inference.conclusion]
        af.set_attack(inference_argument, target_argument, AF.DEFINITE_ATTACK)

    # Create rebutting and undermining attacks
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        conclusion = inference.conclusion

        # Create rebutting attacks
        for inference2_id, inference2 in dbas_graph.inferences.items():
            inference2_argument = argument_for_inference_id[inference2_id]
            conclusion2 = inference2.conclusion
            if conclusion == conclusion2:
                if inference.is_supportive != inference2.is_supportive:
                    af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference2_argument, inference_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks
        for inference2_id, inference2 in itertools.chain(dbas_graph.inferences.items(), dbas_graph.undercuts.items()):
            inference2_argument = argument_for_inference_id[inference2_id]
            if not inference.is_supportive:
                # If a a premise can be a negated statement in future versions of D-BAS, cover that case!
                for premise2 in inference2.premises:
                    if conclusion == premise2:
                        af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)

    return af


def import_af_extended(dbas_graph):
    """
    Create an AF representation of the given discussion.

    The AF representation contains an argument per inference/undercut in the D-BAS graph
    and two arguments for each statement in the D-BAS graph (negated and not-negated).

    :param dbas_graph: DBASGraph to be used for AF generation
    :type dbas_graph: DBASGraph
    :return: AF
    """
    logging.debug('Create Argumentation Framework from D-BAS graph...')
    current_argument = -1
    element_id_for_argument = {}
    argument_for_statement_id = {}
    argument_for_inference_id = {}

    # Add two arguments for each statement
    for statement in dbas_graph.statements:
        logging.debug('Statement: %s', statement)
        current_argument += 1
        element_id_for_argument[current_argument] = statement  # statement argument
        argument_for_statement_id[statement] = current_argument
        current_argument += 1
        element_id_for_argument[current_argument] = -statement  # negated statement argument

    # Add one argument for each inference
    for inference_id in itertools.chain(dbas_graph.inferences, dbas_graph.undercuts):
        logging.debug('Inference: %s', inference_id)
        current_argument += 1
        element_id_for_argument[current_argument] = 'r' + str(inference_id)  # inference argument
        argument_for_inference_id[inference_id] = current_argument

    n_nodes = current_argument+1
    af = AF(n_nodes)
    for arg in element_id_for_argument:
        af.set_argument_name(arg, element_id_for_argument[arg])

    # Create attacks between statement arguments
    for statement in dbas_graph.statements:
        statement_argument = argument_for_statement_id[statement]
        negated_statement_argument = statement_argument+1
        af.set_attack(statement_argument, negated_statement_argument, AF.DEFINITE_ATTACK)
        af.set_attack(negated_statement_argument, statement_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks from statement arguments against inference premises
        for inference2_id, inference2 in itertools.chain(dbas_graph.inferences.items(), dbas_graph.undercuts.items()):
            inference2_argument = argument_for_inference_id[inference2_id]
            for premise2 in inference2.premises:
                # If a a premise can be a negated statement in future versions of D-BAS, cover that case!
                if statement == premise2:
                    af.set_attack(negated_statement_argument, inference2_argument, AF.DEFINITE_ATTACK)

    # Create undercut attacks
    for inference_id in dbas_graph.undercuts:
        inference = dbas_graph.undercuts[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        target_argument = argument_for_inference_id[inference.conclusion]
        af.set_attack(inference_argument, target_argument, AF.DEFINITE_ATTACK)

    # Create rebutting and undermining attacks
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        conclusion = inference.conclusion

        # Attack the statement argument that contradicts the conclusion
        eliminated_statement_argument = argument_for_statement_id[conclusion]
        if inference.is_supportive:
            eliminated_statement_argument += 1  # In case of a supportive inference, attack the negated statement
        af.set_attack(inference_argument, eliminated_statement_argument, AF.DEFINITE_ATTACK)

        # Create rebutting attacks
        for inference2_id in dbas_graph.inferences:
            inference = dbas_graph.inferences[inference2_id]
            inference2_argument = argument_for_inference_id[inference2_id]
            conclusion2 = inference2.conclusion
            if conclusion == conclusion2:
                if inference.is_supportive != inference2.is_supportive:
                    af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference2_argument, inference_argument, AF.DEFINITE_ATTACK)

        # Create undermining attacks
        for inference2_id, inference2 in itertools.chain(dbas_graph.inferences.items(), dbas_graph.undercuts.items()):
            inference2_argument = argument_for_inference_id[inference2_id]
            if not inference.is_supportive:
                # If a a premise can be a negated statement in future versions of D-BAS, cover that case!
                for premise2 in inference2.premises:
                    if conclusion == premise2:
                        af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)

    return af
