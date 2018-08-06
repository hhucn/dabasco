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

    def is_equivalent_to(self, other):
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
        return None

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
