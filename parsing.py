from tools import colors


def display_error(col, error_str, count, line):
    str_count = str(count)
    str_col = str(col)
    if col == -1:
        print(line, f"{colors.clr.fg.lightred}\u2717{colors.clr.reset}")
        for elt in line:
            print(f"{colors.clr.fg.red}^{colors.clr.reset}", end="")
        print("")
        print(colors.clr.fg.red, f"Parsing error: [line: {str_count}] {error_str}", colors.clr.reset)
    else:
        ind = 0
        for elt in line:
            if ind == col:
                print(f"{colors.clr.bg.red}{elt}{colors.clr.reset}", end="")
            else:
                print(f"{elt}", end="")
            ind += 1
        print(f" {colors.clr.fg.lightred}\u2717{colors.clr.reset}")
        ind = 0
        for elt in line:
            if ind == col:
                print(f"{colors.clr.fg.red}^{colors.clr.reset}", end="")
            else:
                print(" ", end="")
            ind += 1
        print("")
        print(colors.clr.fg.red, f"Parsing error:[line: {str_count}][col: {str_col}] {error_str}", colors.clr.reset)
    return 1


def define_elt_type(elt):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'i', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    negative = ['!']
    operators = ['<', '=', '>', "+", '|', '^']
    parentheses = ['(', ')']
    if (elt in letters) is True:
        return True, False, False, False, False
    elif (elt in negative) is True:
        return False, True, False, False, False
    elif (elt in operators) is True:
        return False, False, True, False, False
    elif (elt in parentheses) is True:
        return False, False, False, True, False
    else:
        return False, False, False, False, True


def letter_parse(line, line_len, elt, col):
    # prev_is_letter = False
    # prev_is_negative = False
    # prev_is_operator = False
    # prev_is_parenthese = False
    # prev_is_invalid = False

    next_is_letter = False
    next_is_negative = False
    next_is_operator = False
    next_is_parenthese = False
    next_is_invalid = False

    error_str = ""
    error = 0
    # if col > 0 and col < (line_len - 1):
    #     prev_is_letter, prev_is_negative, prev_is_operator, prev_is_parenthese, prev_is_invalid = define_elt_type(elt)
    #     next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(elt)

    if col < (line_len - 1):
        next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(line[col + 1])

        if next_is_letter is True:
            error_str = "a letter cannot be followed by another letter."
            error = 1
            return error, error_str
        
        if next_is_negative is True:
            error_str = "a letter cannot be followed by a negative symbol."
            error = 1
            return error, error_str

        if next_is_parenthese is True:
            if line[col + 1] == '(':
                error_str = "a letter cannot be followed by an opening parenthesis."
                error = 1
                return error, error_str

    
    return error, error_str


def negative_parse(line, line_len, elt, col):

    next_is_letter = False
    next_is_negative = False
    next_is_operator = False
    next_is_parenthese = False
    next_is_invalid = False

    error_str = ""
    error = 0

    if col < (line_len - 1):
        next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(line[col + 1])
        if next_is_negative is True:
            error_str = "a negative symbol can only be followed by a letter."
            error = 1
            return error, error_str
        
        if next_is_operator is True:
            error_str = "a negative symbol can only be followed by a letter."
            error = 1
            return error, error_str
        
        if next_is_parenthese is True:
            error_str = "a negative symbol can only be followed by a letter."
            error = 1
            return error, error_str
    
    if col == (line_len - 1):
        error_str = "a negative symbol cannot be at the end of a rule."
        error = 1
        return error, error_str
    
    return error, error_str


def operator_parse(line, line_len, elt, col):

    next_is_letter = False
    next_is_negative = False
    next_is_operator = False
    next_is_parenthese = False
    next_is_invalid = False

    first_category = ["+", "|", "^"]

    error_str = ""
    error = 0

    if (elt in first_category) is True:
        if col < (line_len - 1):
            next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(line[col + 1])
            if next_is_operator is True:
                error_str = "an operator cannot be followed by another operator."
                error = 1
                return error, error_str
            
            if next_is_parenthese is True:
                if line[col + 1] == ')':
                    error_str = "an operator cannot be followed by a closing parenthesis."
                    error = 1
                    return error, error_str
    
        if col == (line_len - 1):
            error_str = "an operator cannot be at the end of a rule."
            error = 1
            return error, error_str


    if elt == '<':
        if col > (line_len - 3):
            error_str = "invalid operator."
            error = 1
            return error, error_str
        
        elif line[col + 1] != '=' and line[col + 2] != '>':
            error_str = "invalid operator."
            error = 1
            return error, error_str
    
    if elt == '=':
        if col > (line_len - 2):
            error_str = "invalid operator."
            error = 1
            return error, error_str
        
        elif line[col + 1] != '>':
            error_str = "invalid operator."
            error = 1
            return error, error_str
    
    if elt == '>':
        if col < (line_len - 1):
            next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(line[col + 1])
            if next_is_operator is True:
                error_str = "a operator cannot be followed by another operator."
                error = 1
                return error, error_str
            
            if line[col + 1] == ')':
                error_str = "an operator cannot be followed by a closing parenthesis."
                error = 1
                return error, error_str
        
        if col == (line_len - 1):
            error_str = "an operator cannot be at the end of a rule."
            error = 1
            return error, error_str
    
    return error, error_str

        
def parenthese_parse(line, line_len, elt, col):

    next_is_letter = False
    next_is_negative = False
    next_is_operator = False
    next_is_parenthese = False
    next_is_invalid = False

    error_str = ""
    error = 0

    if elt == '(':
        if col < (line_len - 1):
            next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(line[col + 1])
            if next_is_operator is True:
                error_str = "an opening parenthesis cannot be followed by an operator."
                error = 1
                return error, error_str
            
            if line[col + 1] == ')':
                error_str = "an opening parenthesis cannot be followed by a closing parenthesis."
                error = 1
                return error, error_str
    
        if col == (line_len - 1):
            error_str = "an opening parenthesis cannot be at the end of a rule."
            error = 1
            return error, error_str
    
    if elt == ')':
        if col < (line_len - 1):
            next_is_letter, next_is_negative, next_is_operator, next_is_parenthese, next_is_invalid = define_elt_type(line[col + 1])
            if next_is_letter is True:
                error_str = "a closing parenthesis cannot be followed by a letter."
                error = 1
                return error, error_str
            
            if next_is_negative is True:
                error_str = "a closing parenthesis cannot be followed by a negative symbol."
                error = 1
                return error, error_str
            
            if line[col + 1] == '(':
                error_str = "an closing parenthesis cannot be followed by an opening parenthesis."
                error = 1
                return error, error_str
    
    return error, error_str


def check_line(line, count, rules_phase):
    col = 0
    error = 0
    error_str = ""
    line_len = len(line)
    is_letter = False
    is_negative = False
    is_operator = False
    is_parenthese = False
    is_invalid = False

    if rules_phase == False:
        print(f"{colors.clr.fg.darkgrey}########## RULES ##########{colors.clr.reset}")

    if ("=>" in line) is False and ("<=>" in line) is False:
        error = 1
        error_str = "=> or <=> not find in rule."
        return display_error(-1, error_str, count, line)

    for elt in line:

        is_letter, is_negative, is_operator, is_parenthese, is_invalid = define_elt_type(elt)

        if is_invalid:
            error_str = "invalid character found."
            return display_error(col, error_str, count, line)

        if col == 0:
            if is_letter is False and elt != '(':
                error_str = "rules must begin by a letter."
                return display_error(col, error_str, count, line)
        
        if is_letter is True:
            error, error_str = letter_parse(line, line_len, elt, col)
            if error == 1:
                return display_error(col, error_str, count, line)
        
        if is_negative is True:
            error, error_str = negative_parse(line, line_len, elt, col)
            if error == 1:
                return display_error(col, error_str, count, line)
        
        if is_operator is True:
            error, error_str = operator_parse(line, line_len, elt, col)
            if error == 1:
                return display_error(col, error_str, count, line)
        
        if is_parenthese is True:
            error, error_str = parenthese_parse(line, line_len, elt, col)
            if error == 1:
                return display_error(col, error_str, count, line)
        
        col += 1
    
    print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}")
    return 0


def check_initial_facts(line, count):
    print("")
    print(f"{colors.clr.fg.darkgrey}########## INITIAL FACTS ##########{colors.clr.reset}")

    if len(line) == 1 and line[0] == '=':
        error_str = "no initial facts found."
        return display_error(-1, error_str, count, line)

    else:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'i', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        tmp = []
        col = 0
        for elt in line:
            if col == 0 and elt == '=':
                pass
            elif (elt in letters) == True:
                index = letters.remove(elt)
                tmp.append(elt)
            elif (elt in letters) == False:
                if (elt in tmp) == True:
                    error_str = "duplicate detected for this letter in initial facts."
                    return display_error(col, error_str, count, line)
                else:
                    error_str = "invalid character for initial facts."
                    return display_error(col, error_str, count, line)
            col += 1

        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}")
        return 0




def check_queries(line, count):
    print("")
    print(f"{colors.clr.fg.darkgrey}########## QUERIES ##########{colors.clr.reset}")

    if len(line) == 1 and line[0] == '?':
        error_str = "no queries found."
        return display_error(-1, error_str, count, line)

    else:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'i', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        tmp = []
        col = 0
        for elt in line:
            if col == 0 and elt == '?':
                pass
            elif (elt in letters) == True:
                index = letters.remove(elt)
                tmp.append(elt)
            elif (elt in letters) == False:
                if (elt in tmp) == True:
                    error_str = "duplicate detected for this letter in queries."
                    return display_error(col, error_str, count, line)
                else:
                    error_str = "invalid character for queries."
                    return display_error(col, error_str, count, line)
            col += 1
        
        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}")
        return 0


def ex_parsing(params, file_name, datasets_folder_path):
    print(params)
    params["parse_error"] = 0

    print(colors.clr.fg.yellow, f"Parsing {file_name}...", colors.clr.reset)
    print("")

    path = datasets_folder_path + "/" + file_name
    file = open(path, 'r')
    lines = file.readlines()
    tokens = []
    query = []
    facts = []
    rules_phase = False
    fact_phase = False
    query_phase = False
 
    count = 0
    for line in lines:
        count += 1
        line = line.strip()
        line = line.replace(" ", "")
        line = line.replace("\n", "")

        if len(line) > 0 and line[0] == "?":
            if fact_phase == False:
                display_error(-1, "you must initialize initials facts before queries.", count, line)
                print("")
                print(colors.clr.fg.red, f"{file_name} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                return params
            if query_phase == True:
                display_error(-1, "queries have already been initialized.", count, line)
                print("")
                print(colors.clr.fg.red, f"{file_name} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                return params
            else:
                query_phase = True
                ind = 0
                for elt in line:
                    if elt == "#":
                        line = line[:ind]
                        break
                    ind += 1
                result = check_queries(line, count)
                if result == 1:
                    print("")
                    print(colors.clr.fg.red, f"{file_name} parse failed.", colors.clr.reset)
                    print("")
                    params["parse_error"] = 1
                    return params
                else:
                    query = list(line[1:])

        if len(line) > 0 and line[0] == "=":
            if fact_phase == True:
                display_error(-1, "the initial facts have already been initialized.", count, line)
                print("")
                print(colors.clr.fg.red, f"{file_name} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                return params
            else:
                fact_phase = True
                ind = 0
                for elt in line:
                    if elt == "#":
                        line = line[:ind]
                        break
                    ind += 1
                result = check_initial_facts(line, count)
                if result == 1:
                    print("")
                    print(colors.clr.fg.red, f"{file_name} parse failed.", colors.clr.reset)
                    print("")
                    params["parse_error"] = 1
                    return params
                else:
                    facts = list(line[1:])
                

        if query_phase == False and fact_phase == False and len(line) > 0 and line[0] != "#":
            ind = 0
            for elt in line:
                if elt == "#":
                    line = line[:ind]
                    break
                ind += 1
            result = check_line(line, count, rules_phase)
            if result == 1:
                print("")
                print(colors.clr.fg.red, f"{file_name} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                return params
            else:
                new_list = list(line)
                tokens.append(new_list)
                rules_phase = True
    
    params["tokens"] = tokens
    params["initial_facts"] = facts
    params["queries"] = query
    print("")
    print(colors.clr.fg.green, f"{file_name} parse success !", colors.clr.reset)
    print("")
    return params