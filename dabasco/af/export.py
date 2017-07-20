from .af import AF


def export_aspartix(af):
    """
    Create an ASPARTIX formatted string representation of the given af.

    :param af: argumentation framework
    :return: ASPARTIX formatted string representation of the given af
    """
    str_list = []
    for arg in range(af.n):
        if af.A[arg] == AF.DEFINITE_ARGUMENT:
            str_list.append('arg(')
            str_list.append(str(af.get_name_for_argument(arg)))
            str_list.append(').\n')
    for attacker in range(af.n):
        for target in range(af.n):
            if af.R[attacker][target] == AF.DEFINITE_ATTACK:
                str_list.append('att(')
                str_list.append(str(af.get_name_for_argument(attacker)))
                str_list.append(',')
                str_list.append(str(af.get_name_for_argument(target)))
                str_list.append(').\n')
    str_output = ''.join(str_list)
    return str_output
