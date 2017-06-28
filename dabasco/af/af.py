from random import randrange
import copy


class AF(object):
    """
    Argumentation Framework.
    """

    NO_ATTACK = 0
    DEFINITE_ATTACK = 1

    NO_ARGUMENT = 0
    DEFINITE_ARGUMENT = 1

    def __init__(self, n):
        self.n = n
        self.A = [AF.DEFINITE_ARGUMENT for _ in range(n)]
        self.R = [[AF.NO_ATTACK for _ in range(n)] for _ in range(n)]

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

    def merge_with_af(self, other):
        """
        Create a new argumentation framework from self and other.
        It has the added sets of arguments from self and other and
        the respective sets of attacks.
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
        Create a copy of s in which all arguments are removed that
        do not have status DEFINITE_ARGUMENT in self.
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
        self.R[attacker][target] = value

    def set_argument(self, argument, value):
        self.A[argument] = value

    def pretty_print(self):
        for attacker in range(self.n):
            print(str(self.R[attacker]))

    def attacks(self, attacker, target):
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
        s = self.restricted_extension(s)
        for attacker in s:
            for target in s:
                if self.R[attacker][target] == AF.DEFINITE_ATTACK:
                    return False
        return True

    def is_acceptable(self, a, s):
        """
        Return True if a is acceptable with respect to s in self, False otherwise.
        Note: Always return True if a does not have status DEFINITE_ARGUMENT in self.
        """
        s = self.restricted_extension(s)
        if self.A[a] == AF.DEFINITE_ARGUMENT:
            for attacker in range(self.n):
                if (self.A[attacker] == AF.DEFINITE_ARGUMENT) and (self.R[attacker][a] == AF.DEFINITE_ATTACK):
                    if not self.attacks(s, attacker):
                        return False
        return True

    def is_admissible(self, s):
        s = self.restricted_extension(s)
        if not self.is_conflict_free(s):
            return False
        for a in s:
            if not self.is_acceptable(a, s):
                return False
        return True

    def is_stable(self, s):
        s = self.restricted_extension(s)
        if not self.is_conflict_free(s):
            return False
        for target in range(self.n):
            if target not in s:
                if not self.attacks(s, target):
                    return False
        return True

    def is_grounded(self, s):
        s = self.restricted_extension(s)
        return self.grounded_extension() == s

    def is_complete(self, s):
        s = self.restricted_extension(s)
        if not self.is_admissible(s):
            return False
        for a in range(self.n):
            if (self.A[a] == AF.DEFINITE_ARGUMENT) and (a not in s) and (self.is_acceptable(a, s)):
                return False
        return True

    def is_preferred(self, s):
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
        Return True if s is dominated by t in self, False otherwise.
        s is dominated by t if t is a strict admissible superset of s.
        Note: Only for internal use in is_preferred(self,s)!
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
