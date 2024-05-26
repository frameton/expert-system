from tools import colors


def check_parenthese(line, count):
    parenthese = 0
    col = 0
    line = line.strip()
    line = line.replace(" ", "")
    line = line.replace("\n", "")
    line = list(line)

    for elt in line:
        if elt == '(':
            parenthese += 1
        if elt == ')':
            if parenthese == 0:
                error_str = "Parenthesis error."
                return display_error(col, error_str, count, line)
            parenthese -= 1
        col += 1
    
    if parenthese != 0:
        error_str = "Parenthesis error."
        return display_error(-2, error_str, count, line)


    _match = []
    open_match = []
    parenthese_index = 0
    parenthese_close = [False]
    col = 0

    for elt in line:
        if elt == '(':
            parenthese_index += 1
            parenthese_close.append(False)
            if line[col + 1] == '(':
                tmp = []
                tmp.append(parenthese_index)
                tmp.append(parenthese_index + 1)
                open_match.append(tmp)

        if elt == ')':
            selection = len(parenthese_close) - 1
            while selection > 0:
                if parenthese_close[selection] == False:
                    parenthese_close[selection] = True
                    break
                selection -= 1
            
            if col < (len(line) - 2) and line[col + 1] == ')':
                selection2 = len(parenthese_close) - 1
                while selection2 > 0:
                    if parenthese_close[selection2] == False:
                        break
                    selection2 -= 1
                for elt2 in open_match:
                    if elt2[0] == selection2 and elt2[1] == selection:
                        if (selection in _match) is False:
                            _match.append(selection)
                

        col += 1

    parenthese_index = 0
    parenthese_close = [False]
    col = 0

    for elt in line:
        if elt == '(':
            parenthese_index += 1
            parenthese_close.append(False)
            if (parenthese_index in _match) is True:
                line[col] = " "

        if elt == ')':
            selection = len(parenthese_close) - 1
            while selection > 0:
                if parenthese_close[selection] == False:
                    parenthese_close[selection] = True
                    break
                selection -= 1
            if (selection in _match) is True:
                line[col] = " "
        
        col += 1

    line = ''.join(line)
    line = line.strip()
    line = line.replace(" ", "")
    line = list(line)

    col = 0
    for elt in line:
        if elt == '(' and col < len(line) - 2 and (line[col + 1].isalpha()) is True and (line[col + 1].isupper()) is True and line[col + 2] == ')':
            line[col] = " "
            line[col + 2] = " "

    line = ''.join(line)
    line = line.strip()
    line = line.replace(" ", "")

    return line


def search_recursice_parenthese_list(base_list):
    count = 0
    new_list = []
    total_delete = 0

    for elt in base_list:
        if elt == '(':
            new_elt, len_delete = search_recursice_parenthese_list(base_list[count + 1:])
            new_list.append(new_elt)
            base_list[count] = new_elt
            total_delete = total_delete + len_delete
            while len_delete > 0:
                base_list.pop(count + 1)
                len_delete -= 1

        elif elt == ')':
            total_delete = total_delete + (len(new_list) + 1)
            return new_list, total_delete

        else:
            new_list.append(elt)
        
        count += 1
    
    print(colors.clr.fg.red, "An unexpected error has occurred.", colors.clr.reset)
    exit(1)




def create_parentheses_nested_lists(new_list):
    count = 0

    for elt in new_list:
        if elt == '(':
            new_elt, len_delete = search_recursice_parenthese_list(new_list[count + 1:])
            new_list[count] = new_elt
            count2 = 1
            while len_delete > 0:
                new_list.pop(count + 1)
                len_delete -= 1

        count += 1

    return new_list


def check_inutiles_parentheses(new_list):

    if len(new_list) == 1:
        new_list = new_list[0]

    count = 0
    for elt in new_list:
        if type(elt) is list:
            new_list[count] = check_inutiles_parentheses(elt)
        
        count += 1

    return new_list