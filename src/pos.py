import sys


class Position(object):
    """Map elements in a set [1, ..n] to {REJECTED, UNDECIDED, ACCEPTED}."""

    REJECTED = -1
    UNDECIDED = 0
    ACCEPTED = 1

    def __init__(self, n):
        self.n = n
        self.nUndecided = n  # Cache the number of undecided elements to improve performance.
        self.A = [Position.UNDECIDED]*(n+1)

    def set_acceptance(self, i, a):
        change = abs(self.A[i]) - abs(a)
        self.nUndecided += change
        self.A[i] = a

    def set_accepted(self, i):
        change = abs(self.A[i]) - 1
        self.nUndecided += change
        self.A[i] = Position.ACCEPTED

    def set_rejected(self, i):
        change = abs(self.A[i]) - 1
        self.nUndecided += change
        self.A[i] = Position.REJECTED

    def set_undecided(self, i):
        change = abs(self.A[i])
        self.nUndecided += change
        self.A[i] = Position.UNDECIDED

    def is_accepted(self, i):
        if i < 0:
            return self.A[-i] == Position.REJECTED
        return self.A[i] == Position.ACCEPTED

    def is_rejected(self, i):
        if i < 0:
            return self.A[-i] == Position.ACCEPTED
        return self.A[i] == Position.REJECTED

    def is_undecided(self, i):
        return self.A[abs(i)] == Position.UNDECIDED

    def get_acceptance(self, i):
        return self.A[abs(i)]

    def accepted_elements(self):
        s = set()
        for element in range(1, self.n+1):
            if self.A[element] == Position.ACCEPTED:
                s.add(element)
        return s

    def get_free_elements(self):
        free_elements = set()
        for element in range(1, self.n+1):
            my_choice = self.A[element]
            if my_choice == Position.UNDECIDED:
                free_elements.add(element)
        return free_elements

    def is_complete(self):
        return self.nUndecided == 0

    def union_with(self, other_pos):
        """Create a new position from self and otherPos.

        Creates a new position of same size as self. For each
        undecided element in self, use the acceptance value from
        otherPos, else use acceptance from self.
        Return None if the two positions are conflicting."""

        new_pos = Position(self.n)
        for element in range(1, self.n+1):
            my_choice = self.A[element]
            their_choice = other_pos.A[element]
            if my_choice == Position.UNDECIDED:
                new_pos.set_acceptance(element, their_choice)
            elif their_choice == Position.UNDECIDED:
                new_pos.set_acceptance(element, my_choice)
            elif my_choice != their_choice:
                return None
            else:
                new_pos.set_acceptance(element, their_choice)
        return new_pos

    def get_number_of_completions(self):
        return 2**self.nUndecided

    def pretty_print(self, prefix, suffix):
        if prefix:
            sys.stdout.write(prefix)
        sys.stdout.write('[')
        for arg in range(1, self.n+1):
            if self.A[arg] == Position.ACCEPTED:
                sys.stdout.write('+')
            elif self.A[arg] == Position.REJECTED:
                sys.stdout.write('-')
            else:
                sys.stdout.write('?')
        sys.stdout.write(']')
        if suffix:
            sys.stdout.write(suffix)
        sys.stdout.write('\n')
