from random import randrange
import copy


class AF(object):
    """
    Argumentation Framework.
    """

    NO_ATTACK = 0
    """constant that represents attack state 'no attack' between two arguments."""
    DEFINITE_ATTACK = 1
    """constant that represents attack state 'definite attack' between two arguments."""

    NO_ARGUMENT = 0
    """constant that represents argument state 'no argument' of an argument."""
    DEFINITE_ARGUMENT = 1
    """constant that represents argument state 'definite argument' of an argument."""

    def __init__(self, n):
        self.n = n
        """(int) number of arguments. The set of arguments is [0,...,n-1] implicitly."""
        self.A = [AF.DEFINITE_ARGUMENT for _ in range(n)]
        """(list) argument statuses for each argument"""
        self.R = [[AF.NO_ATTACK for _ in range(n)] for _ in range(n)]
        """(list) attack statuses for each pair of arguments"""

        self.name_for_argument = {}
        self.argument_for_name = {}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.n != other.n:
                return False
            for arg in range(self.n):
                if self.A[arg] != other.A[arg]:
                    return False
            for attacker in range(self.n):
                for target in range(self.n):
                    if self.R[attacker][target] != other.R[attacker][target]:
                        return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def set_argument_name(self, arg, name):
        """
        Remember the given name for the given argument.

        :param arg: ID of an argument in this AF
        :type arg: int
        :param name: name for the argument
        :type name: str
        """
        self.name_for_argument[arg] = name
        self.argument_for_name[name] = arg

    def get_name_for_argument(self, arg):
        """
        Return the name of the given argument.

        :param arg: argument ID in [0,...,self.n-1]
        :type arg: int
        :return: name of the given argument
        """
        if arg in self.name_for_argument:
            return self.name_for_argument[arg]
        return arg

    def get_argument_for_name(self, name):
        """
        Return the argument that represents the given name in this AF.

        :param name: argument name
        :type name: str
        :return: argument ID of the given statement
        """
        if name in self.argument_for_name:
            return self.argument_for_name[name]
        return name

    def merge_with_af(self, other):
        """
        Merge self with the other given AF into a new argumentation framework.

        The new AF has the union of the arguments and attacks from self and other.

        :param other: the af to merge with
        :type other: AF
        :return: a new AF that represents the union of self and other
        """
        n = self.n + other.n
        new = self.__class__(n)
        for attacker in range(self.n):
            for target in range(self.n):
                new.set_attack(attacker, target, self.R[attacker][target])
        for attacker in range(other.n):
            for target in range(other.n):
                new.set_attack(attacker + self.n, target + self.n, other.R[attacker][target])
        return new

    def restricted_extension(self, s):
        """
        Create a copy of the given set of arguments without those arguments that
        do not have status DEFINITE_ARGUMENT in this AF.

        :param s: set of arguments
        :type s: set
        :return: set of arguments
        """
        s2 = set()
        for a in range(self.n):
            if (a in s) and (self.A[a] == AF.DEFINITE_ARGUMENT):
                s2.add(a)
        return s2

    def randomize_attacks(self):
        """
        Set all attack relations in self randomly to NO_ATTACK or DEFINITE_ATTACK.
        """
        for attacker in range(self.n):
            for target in range(self.n):
                self.R[attacker][target] = randrange(AF.NO_ATTACK, AF.DEFINITE_ATTACK + 1)

    def set_attack(self, attacker, target, value):
        """
        Set the attack state from the given attacking argument to the given target argument.

        :param attacker: attacking argument
        :type attacker: int
        :param target: target argument
        :type target: int
        :param value: attack state to be set
        :type value: int
        """
        self.R[attacker][target] = value

    def set_argument(self, argument, value):
        """
        Set the argument state of the given argument.

        :param argument: argument
        :type argument: int
        :param value: argument state to be set
        :type value: int
        """
        self.A[argument] = value

    def pretty_print(self):
        """
        Print a human readable representation of this AF to stdout.
        """
        for attacker in range(self.n):
            print(str(self.R[attacker]))

    def attacks(self, attacker, target):
        """
        Indicates whether whether there is a definite attack from attacker to target in this AF.

        Both attacker and target may be a single argument (int) or a set of multiple arguments.

        :param attacker: single attacking argument or set of attacking arguments
        :type attacker: int or set
        :param target: single target argument or set of target arguments
        :type target: int or set
        :return: true if at least one attacker attacks at least one target, False otherwise
        """
        if type(attacker) is int:
            if self.A[attacker] != AF.DEFINITE_ARGUMENT:
                return False
            if type(target) is int:
                if self.A[target] != AF.DEFINITE_ARGUMENT:
                    return False
                return self.R[attacker][target] == AF.DEFINITE_ATTACK
            else:
                for b in target:
                    if (self.A[b] == AF.DEFINITE_ARGUMENT)\
                            and (self.R[attacker][b] == AF.DEFINITE_ATTACK):
                        return True
                return False
        else:
            if type(target) is int:
                for a in attacker:
                    if (self.A[a] == AF.DEFINITE_ARGUMENT)\
                            and (self.R[a][target] == AF.DEFINITE_ATTACK):
                        return True
                return False
            else:
                for a in attacker:
                    for b in target:
                        if (self.A[a] == AF.DEFINITE_ARGUMENT)\
                                and (self.A[b] == AF.DEFINITE_ARGUMENT)\
                                and (self.R[a][b] == AF.DEFINITE_ATTACK):
                            return True
                return False

    def grounded_extension(self):
        """
        Determine the grounded extension of this AF.

        :return: set of arguments representing the grounded extension
        """
        s = set()
        s_next = set()
        for a in range(self.n):
            if self.A[a] == AF.DEFINITE_ARGUMENT:
                if self.is_acceptable(a, s):
                    s_next.add(a)
        while s != s_next:
            s = s_next
            s_next = set()
            for a in range(self.n):
                if self.A[a] == AF.DEFINITE_ARGUMENT:
                    if self.is_acceptable(a, s):
                        s_next.add(a)
        return s

    def is_conflict_free(self, s):
        """
        Indicates whether the given set of arguments is conflict-free in this AF.

        :param s: set of arguments
        :type s: set
        :return: True if s is conflict-free, False otherwise
        """
        s = self.restricted_extension(s)
        for attacker in s:
            for target in s:
                if self.R[attacker][target] == AF.DEFINITE_ATTACK:
                    return False
        return True

    def is_acceptable(self, a, s):
        """
        Indicates whether the given argument is acceptable with respect to the given set of arguments in this AF.

        Always returns True if the argument does not have status DEFINITE_ARGUMENT in self.

        :param a: the argument to be checked for acceptability
        :type a: int
        :param s: set of arguments
        :type s: set
        :return: True if a is acceptable with respect to s in self, False otherwise
        """
        s = self.restricted_extension(s)
        if self.A[a] == AF.DEFINITE_ARGUMENT:
            for attacker in range(self.n):
                if (self.A[attacker] == AF.DEFINITE_ARGUMENT) and (self.R[attacker][a] == AF.DEFINITE_ATTACK):
                    if not self.attacks(s, attacker):
                        return False
        return True

    def is_admissible(self, s):
        """
        Indicates whether the given set of arguments is admissible in this AF.

        :param s: set of arguments
        :type s: set
        :return: True if s is admissible, False otherwise
        """
        s = self.restricted_extension(s)
        if not self.is_conflict_free(s):
            return False
        for a in s:
            if not self.is_acceptable(a, s):
                return False
        return True

    def is_stable(self, s):
        """
        Indicates whether the given set of arguments is stable in this AF.

        :param s: set of arguments
        :type s: set
        :return: True if s is stable, False otherwise
        """
        s = self.restricted_extension(s)
        if not self.is_conflict_free(s):
            return False
        for target in range(self.n):
            if target not in s:
                if not self.attacks(s, target):
                    return False
        return True

    def is_grounded(self, s):
        """
        Indicates whether the given set of arguments is grounded in this AF.

        :param s: set of arguments
        :type s: set
        :return: True if s is grounded, False otherwise
        """
        s = self.restricted_extension(s)
        return self.grounded_extension() == s

    def is_complete(self, s):
        """
        Indicates whether the given set of arguments is complete in this AF.

        :param s: set of arguments
        :type s: set
        :return: True if s is complete, False otherwise
        """
        s = self.restricted_extension(s)
        if not self.is_admissible(s):
            return False
        for a in range(self.n):
            if (self.A[a] == AF.DEFINITE_ARGUMENT) and (a not in s) and (self.is_acceptable(a, s)):
                return False
        return True

    def is_preferred(self, s):
        """
        Indicates whether the given set of arguments is preferred in this AF.

        :param s: set of arguments
        :type s: set
        :return: True if s is preferred, False otherwise
        """
        s = self.restricted_extension(s)
        if not self.is_admissible(s):
            return False
        t = copy.deepcopy(s)
        possible_args = []
        for argument in range(self.n):
            if self.A[argument] == AF.DEFINITE_ARGUMENT \
                    and argument not in s \
                    and not self.attacks(argument, s) \
                    and not self.attacks(s, argument):
                possible_args.append(argument)
        return not self.is_dominated(s, t, possible_args, len(possible_args))

    def is_dominated(self, s, t, possible_args, k):
        """
        Indicates whether the first set of arguments is dominated by the second set of arguments in this AF.

        An argument s is dominated by an argument t if t is a strict admissible superset of s.
        Intended for internal use in is_preferred!

        :param s: first argument
        :type s: set
        :param t: second argument
        :type t: set
        :param possible_args: candidates to be added to t
        :type possible_args: list
        :param k: length of possible_args
        :type k: int
        :return: True if the first set is dominated by the second set in self, False otherwise
        """
        if k == 0:
            if s == t:
                return False
            return self.is_admissible(t)
        k -= 1
        possible_arg = possible_args[k]
        if self.is_dominated(s, t, possible_args, k):
            return True
        t.add(possible_arg)
        if self.is_dominated(s, t, possible_args, k):
            return True
        t.remove(possible_arg)
        return False
