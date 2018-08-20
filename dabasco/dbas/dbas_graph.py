import collections

import logging
logger = logging.getLogger('root')

Inference = collections.namedtuple('Inference', ['id', 'premises', 'conclusion', 'is_supportive'])
Undercut = collections.namedtuple('Undercut', ['id', 'premises', 'conclusion'])


class DBASGraph(object):
    """
    Data structure representing a single graph structure obtained from D-BAS export.

    Attributes:
          discussion_id (int): id of the discussion represented by this graph.
          statements (set): list of statements.
          inferences (dict): dict of inference rules on the statements.
          undercuts (dict): dict of undercut inference rules.
    """

    def __init__(self, discussion_id):
        self.discussion_id = discussion_id
        self.statements = set()
        self.inferences = {}
        self.undercuts = {}

    def is_equivalent_to(self, other):
        """
        Check equivalence of two DBAS graph data structures.

        :param other: DBASGraph to compare this DBASGraph with.
        :type other: DBASGraph
        :return: bool
        """
        if not isinstance(other, self.__class__):
            return False
        if self.discussion_id != other.discussion_id:
            return False
        if self.statements != other.statements:
            return False
        if len(self.inferences) != len(other.inferences):
            return False
        if len(self.undercuts) != len(other.undercuts):
            return False
        for my_inference_id in self.inferences:
            my_inference = self.inferences[my_inference_id]
            found_equal = False
            for other_inference_id in other.inferences:
                other_inference = other.inferences[other_inference_id]
                if (my_inference.id == other_inference.id
                        and my_inference.premises == other_inference.premises
                        and my_inference.conclusion == other_inference.conclusion
                        and my_inference.is_supportive == other_inference.is_supportive):
                    found_equal = True
                    break
            if not found_equal:
                return False
        for my_undercut_id in self.undercuts:
            my_undercut = self.undercuts[my_undercut_id]
            found_equal = False
            for other_undercut_id in other.undercuts:
                other_undercut = other.undercuts[other_undercut_id]
                if (my_undercut.id == other_undercut.id
                        and my_undercut.premises == other_undercut.premises
                        and my_undercut.conclusion == other_undercut.conclusion):
                    found_equal = True
                    break
            if not found_equal:
                return False
        return True

    def add_statement(self, statement):
        """
        Add the given statement to this dbas graph

        :param statement: id of the statement to add
        :type statement: int
        """
        if statement not in self.statements:
            self.statements.add(statement)
        else:
            logging.warning('Attempt to add statement (%s) to DBASGraph: already exists!', str(statement))

    def add_inference(self, inference_id, premises, conclusion, is_supportive):
        """
        Add an inference rule specified by the given components to this dbas graph

        :param inference_id: id of the inference
        :type inference_id: int
        :param premises: list of premise statements
        :type premises: list
        :param conclusion: conclusion of the inference
        :type conclusion: int
        :param is_supportive: indicates whether the rule infers the conclusion or its negation
        :type is_supportive: bool
        """
        if inference_id in self.inferences:
            logging.warning('Adding inference (ID %s) to DBASGraph replaces an already existing inference!',
                            str(inference_id))
        inference = Inference(inference_id, premises, conclusion, is_supportive)
        self.inferences[inference_id] = inference

    def add_undercut(self, inference_id, premises, conclusion):
        """
        Add an undercutting inference rule specified by the given components to this dbas graph

        :param inference_id: id of the inference
        :type inference_id: int
        :param premises: list of premise statements
        :type premises: list
        :param conclusion: id of target inference attacked by this undercut
        """
        if inference_id in self.undercuts:
            logging.warning('Adding inference (ID %s) to DBASGraph replaces an already existing inference!',
                            str(inference_id))
        undercut = Undercut(inference_id, premises, conclusion)
        self.undercuts[inference_id] = undercut
