import itertools

from dabasco.config import *
from .af_graph import AF

import logging
logger = logging.getLogger('root')


def import_af_wyner(dbas_graph, opinion, opinion_strict):
    """
    Create an AF representation of the given discussion.

    The AF representation contains an argument per inference/undercut in the D-BAS graph
    and two arguments for each statement in the D-BAS graph (negated and not-negated).

    :param dbas_graph: DBASGraph to be used for AF generation
    :type dbas_graph: DBASGraph
    :param opinion: DBASUser to be used for ADF generation
    :type opinion: DBASUser
    :param opinion_strict: indicate whether user opinion shall be implemented as strict or defeasible rules
    :type opinion_strict: bool
    :return: AF
    """
    logging.debug('Create Argumentation Framework from D-BAS graph and user opinion...')
    current_argument = -1
    element_id_for_argument = {}
    argument_for_statement_id = {}
    argument_for_inference_id = {}

    # Get accepted/rejected statements from opinion
    user_rejected_statements = set()
    user_accepted_statements = set()
    if opinion:
        user_rejected_statements = opinion.get_rejected_statements().intersection(dbas_graph.statements)
        user_accepted_statements = opinion.get_accepted_statements().intersection(dbas_graph.statements)

    # Add two arguments for each statement
    for statement in dbas_graph.statements:
        logging.debug('Statement: %s', statement)
        current_argument += 1
        statement_argument_name = LITERAL_PREFIX_STATEMENT + str(statement)
        element_id_for_argument[current_argument] = statement_argument_name
        argument_for_statement_id[statement] = current_argument
        current_argument += 1
        statement_argument_name_negated = LITERAL_PREFIX_NOT + LITERAL_PREFIX_STATEMENT + str(statement)
        element_id_for_argument[current_argument] = statement_argument_name_negated

    # Add one argument for each inference
    for inference_id in itertools.chain(dbas_graph.inferences, dbas_graph.undercuts):
        logging.debug('Inference: %s', inference_id)
        current_argument += 1
        inference_argument_name = LITERAL_PREFIX_INFERENCE_RULE + str(inference_id)
        element_id_for_argument[current_argument] = inference_argument_name
        argument_for_inference_id[inference_id] = current_argument

    # When using strict user opinion, create a dummy arg that attacks all statements that oppose the user opinion
    opinion_arg_id_for_name = {}
    if opinion:
        # When using strict user opinion, create a single dummy arg
        if opinion_strict:
            current_argument += 1
            element_id_for_argument[current_argument] = DUMMY_LITERAL_NAME_OPINION
            opinion_arg_id_for_name[DUMMY_LITERAL_NAME_OPINION] = current_argument
        # When using non-strict user opinion, create a dummy arg for each commitment to a statement in the opinion
        else:
            for statement in user_accepted_statements:
                current_argument += 1
                arg_name = DUMMY_LITERAL_NAME_OPINION + '_' + str(statement)
                element_id_for_argument[current_argument] = arg_name
                opinion_arg_id_for_name[arg_name] = current_argument
            for statement in user_rejected_statements:
                current_argument += 1
                arg_name = DUMMY_LITERAL_NAME_OPINION + '_' + LITERAL_PREFIX_NOT + str(statement)
                element_id_for_argument[current_argument] = arg_name
                opinion_arg_id_for_name[arg_name] = current_argument

    # Create AF for the determined number of AF arguments
    n_nodes = current_argument + 1
    af = AF(n_nodes)
    for arg in element_id_for_argument:
        af.set_argument_name(arg, element_id_for_argument[arg])

    # When using strict user opinion, the single dummy arg attacks all statements that oppose the user opinion
    if opinion and opinion_strict:
        for statement in user_accepted_statements:
            statement_argument = argument_for_statement_id[statement] + 1  # attack the negated statement arg
            af.set_attack(opinion_arg_id_for_name[DUMMY_LITERAL_NAME_OPINION], statement_argument, AF.DEFINITE_ATTACK)
        for statement in user_rejected_statements:
            statement_argument = argument_for_statement_id[statement]  # attack the non-negated statement arg
            af.set_attack(opinion_arg_id_for_name[DUMMY_LITERAL_NAME_OPINION], statement_argument, AF.DEFINITE_ATTACK)

    # For non-strict user opinion, add attacks between each dummy arg and the statement opposing that user opinion
    if opinion and not opinion_strict:
        for statement in user_accepted_statements:
            statement_argument = argument_for_statement_id[statement] + 1  # attack the negated statement arg
            arg_name = DUMMY_LITERAL_NAME_OPINION + '_' + str(statement)
            af.set_attack(opinion_arg_id_for_name[arg_name], statement_argument, AF.DEFINITE_ATTACK)
            af.set_attack(statement_argument, opinion_arg_id_for_name[arg_name], AF.DEFINITE_ATTACK)
        for statement in user_rejected_statements:
            statement_argument = argument_for_statement_id[statement]  # attack the non-negated statement arg
            arg_name = DUMMY_LITERAL_NAME_OPINION + '_' + LITERAL_PREFIX_NOT + str(statement)
            af.set_attack(opinion_arg_id_for_name[arg_name], statement_argument, AF.DEFINITE_ATTACK)
            af.set_attack(statement_argument, opinion_arg_id_for_name[arg_name], AF.DEFINITE_ATTACK)

    # Create attacks between statement arguments
    for statement in dbas_graph.statements:
        statement_argument = argument_for_statement_id[statement]
        negated_statement_argument = statement_argument + 1
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
        af.set_attack(target_argument, inference_argument, AF.DEFINITE_ATTACK)

    # Create rebutting attacks between rule arguments and literal arguments
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        conclusion = inference.conclusion

        # Attack against the statement argument that contradicts the conclusion
        eliminated_statement_argument = argument_for_statement_id[conclusion]
        if inference.is_supportive:
            eliminated_statement_argument += 1  # In case of a supportive inference, attack the negated statement
        af.set_attack(inference_argument, eliminated_statement_argument, AF.DEFINITE_ATTACK)
        af.set_attack(eliminated_statement_argument, inference_argument, AF.DEFINITE_ATTACK)

    # Create rebutting attacks between conflicting rule arguments
    for inference_id in dbas_graph.inferences:
        inference = dbas_graph.inferences[inference_id]
        inference_argument = argument_for_inference_id[inference_id]
        conclusion = inference.conclusion

        # Conflicting D-BAS arguments
        for inference2_id in dbas_graph.inferences:
            inference2 = dbas_graph.inferences[inference2_id]
            conclusion2 = inference2.conclusion
            if conclusion2 == conclusion:
                if inference.is_supportive != inference2.is_supportive:
                    inference2_argument = argument_for_inference_id[inference2_id]
                    af.set_attack(inference_argument, inference2_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference2_argument, inference_argument, AF.DEFINITE_ATTACK)

        if opinion:
            # Conflict between D-BAS argument and a user opinion commitment
            if inference.is_supportive and (conclusion in user_rejected_statements):
                if opinion_strict:
                    arg_name = DUMMY_LITERAL_NAME_OPINION
                    af.set_attack(opinion_arg_id_for_name[arg_name], inference_argument, AF.DEFINITE_ATTACK)
                else:
                    arg_name = DUMMY_LITERAL_NAME_OPINION + '_' + LITERAL_PREFIX_NOT + str(conclusion)
                    af.set_attack(opinion_arg_id_for_name[arg_name], inference_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference_argument, opinion_arg_id_for_name[arg_name], AF.DEFINITE_ATTACK)
            elif (not inference.is_supportive) and (conclusion in user_accepted_statements):
                if opinion_strict:
                    arg_name = DUMMY_LITERAL_NAME_OPINION
                    af.set_attack(opinion_arg_id_for_name[arg_name], inference_argument, AF.DEFINITE_ATTACK)
                else:
                    arg_name = DUMMY_LITERAL_NAME_OPINION + '_' + str(conclusion)
                    af.set_attack(opinion_arg_id_for_name[arg_name], inference_argument, AF.DEFINITE_ATTACK)
                    af.set_attack(inference_argument, opinion_arg_id_for_name[arg_name], AF.DEFINITE_ATTACK)

    return af
