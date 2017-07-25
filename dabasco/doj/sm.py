import copy
import collections

Inference = collections.namedtuple('Inference', ['id', 'origin', 'target'])


class SM(object):
    """
    A statement map data structure.

    Consists of:
    n -- Number of statements (set of statements is [1, .., n] implicitly)
    inferences -- Set of arguments
    undercuts -- Set of undercuts
    """

    COHERENCE_DEDUCTIVE_INFERENCES = 0

    # -----------------------------------------------------------
    # CONSTRUCTION
    def __init__(self):
        self.n = 0
        self.inferences = {}
        self.undercuts = {}
        self.node_index_for_id = {}
        self.node_id_for_index = {}

    def add_inference(self, origin, target, rid):
        """Add an inference rule with a statement target."""

        # Update statements.
        self.n = max(self.n, abs(target))
        for p in origin:
            self.n = max(self.n, abs(p))

        # check (or generate) inference id.
        if rid is None or (rid in self.inferences):
            i = 1
            while i in self.inferences:
                i += 1
            rid = i

        # Add rule.
        self.inferences[rid] = Inference(rid, origin, target)
        return rid

    def add_undercut(self, origin, target, rid):
        """Add an inference rule with a rule target."""

        # Update statements.
        for p in origin:
            self.n = max(self.n, abs(p))

        # check (or generate) inference id.
        if rid is None or (rid in self.undercuts):
            i = 1
            while i in self.undercuts:
                i += 1
            rid = i

        # Add rule.
        self.undercuts[rid] = Inference(rid, origin, target)
        return rid

    # -----------------------------------------------------------
    # I/O
    def pretty_print(self):
        """
        Print a human readable representation of this statement map to stdout.
        """
        if self.n < 5:
            print('Statements: ', range(1, self.n+1))
        else:
            print('Statements: [ 1, ..., ', self.n, ']')
        for rid in self.inferences:
            self.print_inference(rid)
        for rid in self.undercuts:
            self.print_undercut(rid)

    def print_inference(self, rid):
        rule = self.inferences[rid]
        print(rule.id, ': (', rule.origin, ', ', rule.target, ')')

    def print_undercut(self, rid):
        rule = self.undercuts[rid]
        print(rule.id, ': (', rule.origin, ', rule', rule.target, ')')

    # -----------------------------------------------------------
    # EVALUATION
    def inference_is_violated(self, pos, r):
        for p in r.origin:
            if not pos.is_accepted(p):
                return False
        return pos.is_rejected(r.target)

    def get_active_inferences(self, pos):
        """Return all active and non-undercut inferences.

        An inference is active if it has a satisfied premise.
        An inference is undercut if there is an undercut with
        satisfied premise against it.
        """

        # Fetch inferences with satisfied premises.
        active_inferences = []
        for rid in self.inferences:
            r = self.inferences[rid]
            active = True
            for p in r.origin:
                if not pos.is_accepted(p):
                    active = False
                    break
            if active:
                active_inferences.append(r)

        # Fetch undercuts with satisfied premises.
        active_undercuts = []
        for rid in self.undercuts:
            r = self.undercuts[rid]
            active = True
            for p in r.origin:
                if not pos.is_accepted(p):
                    active = False
                    break
            if active:
                active_undercuts.append(r)

        # Remove rules that are undercut by active undercuts.
        definite_undercuts = []
        changed = True
        while changed:
            changed = False

            # Find unattacked undercutting rules and remember them as definitely active.
            for r in active_undercuts:
                if r not in definite_undercuts:
                    is_undercut = False
                    for r2 in active_undercuts:
                        if r.id == abs(r2.target):
                            is_undercut = True
                            break
                    if not is_undercut:
                        definite_undercuts.append(r)

            # Remove all rules from active_undercuts that are undercut by some rule in definite_undercuts.
            for r in definite_undercuts:
                target_id = abs(r.target)
                n_old = len(active_undercuts)
                active_undercuts[:] = [r2 for r2 in active_undercuts if r2.id != target_id]
                active_inferences[:] = [r2 for r2 in active_inferences if r2.id != target_id]
                n_new = len(active_undercuts)
                if n_new < n_old:
                    changed = True

        return active_inferences

    def get_violated_rules(self, pos):
        """Return a list of Inference tuples, which are the rules in self that are violated by the given position."""
        ar = self.get_active_inferences(pos)
        vr = []
        for r in ar:
            if self.inference_is_violated(pos, r):
                vr.append(r)
        return vr

    def is_deductively_valid(self, pos):
        return len(self.get_violated_rules(pos)) == 0

    # -----------------------------------------------------------
    # COHERENCE
    def get_number_of_coherent_completions(self, pos, coherence):
        if coherence == SM.COHERENCE_DEDUCTIVE_INFERENCES:
            return self.get_number_of_deductively_valid_completions(pos)
        return 0

    def get_number_of_deductively_valid_completions(self, pos):
        possible_statements = list(pos.get_free_elements())
        pos2 = copy.deepcopy(pos)
        return self.get_number_of_deductively_valid_completions_rec(pos2, possible_statements, len(possible_statements))

    def get_number_of_deductively_valid_completions_rec(self, pos, possible_statements, k):
        if k == 0:
            if self.is_deductively_valid(pos):
                return 1
            else:
                return 0
        k -= 1
        possible_statement = possible_statements[k]
        pos.set_accepted(possible_statement)
        n1 = self.get_number_of_deductively_valid_completions_rec(pos, possible_statements, k)
        pos.set_rejected(possible_statement)
        n2 = self.get_number_of_deductively_valid_completions_rec(pos, possible_statements, k)
        pos.set_undecided(possible_statement)
        return n1+n2
