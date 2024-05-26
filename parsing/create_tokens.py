from tools import colors
from parsing.token_parentheses import create_parentheses_nested_lists, check_inutiles_parentheses
from parsing.token_operators import create_implication_operators_nested_lists, create_operators_nested_lists, check_principal_implication_opearator


def create_tokens(line, count):
    new_list = []
    ref = ["+", "|", "^", '(', ')']
    col = 0
    while col < len(line):
        if (line[col].isalpha() is True and line[col].isupper() is True) or (line[col] in ref) is True:
            new_list.append(line[col])
        elif line[col] == '!' or line[col] == '=':
            string = line[col] + line[col + 1]
            new_list.append(string)
            col += 1
        elif line[col] == '<':
            string = line[col] + line[col + 1] + line[col + 2]
            new_list.append(string)
            col += 2
        
        col += 1
    
    new_list = create_parentheses_nested_lists(new_list)
    new_list = create_implication_operators_nested_lists(new_list)
    new_list = create_operators_nested_lists(new_list)
    new_list = check_inutiles_parentheses(new_list)
    new_list = check_principal_implication_opearator(new_list, count, line)
    if new_list == 1:
        return 1
    
    return new_list