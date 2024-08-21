from tools import colors
from parsing.token_parentheses import create_parentheses_nested_lists, check_inutiles_parentheses
from parsing.token_operators import create_implication_operators_nested_lists, create_operators_nested_lists, check_principal_implication_opearator, check_negative_symbole_nested_lists


def create_tokens(line, count, params, comment_part):
    new_list = []
    ref = ["+", "|", "^", '(', ')', '!']
    col = 0
    while col < len(line):
        if (line[col].isalpha() is True and line[col].isupper() is True) or (line[col] in ref) is True:
            new_list.append(line[col])
        elif line[col] == '=':
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
    new_list = check_negative_symbole_nested_lists(new_list)
    new_list = check_inutiles_parentheses(new_list)
    new_list = check_principal_implication_opearator(new_list, count, line)
    if new_list == 1:
        return 1
    
    if params["tester"] == 0:
        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}", end="          ")

    if params["display_comments"] == 1 and len(comment_part) > 0 and params["tester"] == 0:
        print(f"{colors.clr.fg.darkgrey}{comment_part}{colors.clr.reset}", end="          ")

    if params["display_nested_list"] == 1:
        print("")
        print(f"{colors.clr.fg.blue}\u2192 {new_list}{colors.clr.reset}")
    
    if params["tester"] == 0:
        print("")
    
    return new_list