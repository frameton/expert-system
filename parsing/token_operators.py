from tools import colors
from parsing.display_error import display_error


def check_negative_symbole_nested_lists(new_list):
    col = 0

    for elt in new_list:
        if type(elt) is list:
            elt = check_negative_symbole_nested_lists(elt)
        else:
            if elt == '!':
                new_list[col] = []
                new_list[col].append('!')
                new_list[col].append(new_list[col + 1])
                new_list.pop(col + 1)

        col += 1

    return new_list



def create_operators_nested_lists(new_list):
    count = 0

    for elt in new_list:
        if type(elt) is list:
            new_list[count] = create_operators_nested_lists(elt)
        
        else:
            if elt == "^" or elt == "|":
                left_part = []
                right_part = []
                count2 = 0

                while count2 < count:
                    left_part.append(new_list[count2])
                    count2 += 1
                count2 += 1
                while count2 < len(new_list):
                     right_part.append(new_list[count2])
                     count2 += 1
                right_part = create_operators_nested_lists(right_part)

                new_list = []
                new_list.append(left_part)
                new_list.append(elt)
                new_list.append(right_part)

                break

        count += 1

    return new_list


def create_implication_operators_nested_lists(new_list):
    count = 0

    for elt in new_list:
        if type(elt) is list:
            new_list[count] = create_implication_operators_nested_lists(elt)
        
        else:
            if elt == "=>" or elt == "<=>":
                left_part = []
                right_part = []
                count2 = 0

                while count2 < count:
                    left_part.append(new_list[count2])
                    count2 += 1
                count2 += 1
                while count2 < len(new_list):
                     right_part.append(new_list[count2])
                     count2 += 1
                right_part = create_implication_operators_nested_lists(right_part)

                new_list = []
                new_list.append(left_part)
                new_list.append(elt)
                new_list.append(right_part)

                break

        count += 1

    return new_list


def check_principal_implication_opearator(new_list, count, line):
    for elt in new_list:
        if type(elt) is str and (elt == "=>" or elt == "<=>"):
            return new_list
        
    return display_error(-1, "Principal implication operator not found in rule.", count, line)
