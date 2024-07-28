from tools import colors
from parsing.create_tokens import create_tokens
from parsing.display_error import display_error
from parsing.token_parentheses import check_parenthese
from parsing.duplicate_negative_symbol import sort_negative_symbol, search_end_negative_series


def define_elt_type(elt):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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
            error_str = "a negative symbol can only be followed by a letter or open parenthesis."
            error = 1
            return error, error_str
        
        if next_is_operator is True:
            error_str = "a negative symbol can only be followed by a letter or open parenthesis."
            error = 1
            return error, error_str
        
        if line[col + 1] == ')':
            error_str = "a negative symbol can only be followed by a letter or open parenthesis."
            error = 1
            return error, error_str

        # if next_is_parenthese is True:
        #     error_str = "a negative symbol can only be followed by a letter or open parenthesis."
        #     error = 1
        #     return error, error_str
    
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

        if col > 0 and line_len > 1:
            if line[col - 1] != '=':
                error_str = "invalid operator."
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
            
            # if line[col + 1] == ')':
            #     error_str = "an opening parenthesis cannot be followed by a closing parenthesis."
            #     error = 1
            #     return error, error_str
    
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
    implication_operator_count = 0

    if rules_phase == False:
        print("")
        print("")
        print(f"{colors.clr.fg.purple}********** RULES **********{colors.clr.reset}")
        print("")

    for elt in line:

        is_letter, is_negative, is_operator, is_parenthese, is_invalid = define_elt_type(elt)

        if is_invalid:
            error_str = "invalid character found."
            return display_error(col, error_str, count, line)

        if col == 0:
            if is_letter is False and elt != '(' and elt != '!':
                error_str = "rules must begin by a letter, negative symbole or opening parenthesis."
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
            # if elt == '=':
            #     implication_operator_count += 1
            # if implication_operator_count >= 2:
            #     return display_error(col, "duplicate detected for implication operator.", count, line)
            error, error_str = operator_parse(line, line_len, elt, col)
            if error == 1:
                return display_error(col, error_str, count, line)
        
        if is_parenthese is True:
            error, error_str = parenthese_parse(line, line_len, elt, col)
            if error == 1:
                return display_error(col, error_str, count, line)
        
        col += 1
    
    if ("=>" in line) is False and ("<=>" in line) is False:
        error = 1
        error_str = "=> or <=> not find in rule."
        return display_error(-1, error_str, count, line)

    line = check_parenthese(line, count)
    if line == 1:
        return 1

    return 0


def check_initial_facts(line, count, comment_part, params):
    print("")
    print("")
    print("")
    print(f"{colors.clr.fg.purple}********** INITIAL FACTS **********{colors.clr.reset}")
    print("")

    if len(line) == 1 and line[0] == '=':
        error_str = "no initial facts found."
        return display_error(-1, error_str, count, line)

    else:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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
                    pass
                else:
                    error_str = "invalid character for initial facts."
                    return display_error(col, error_str, count, line)
            col += 1

    if params["display_comments"] == 1 and len(comment_part) > 0:
        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}", end="          ")
        print(f"{colors.clr.fg.darkgrey}{comment_part}{colors.clr.reset}")
    
    else:
        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}")

    return 0




def check_queries(line, count, comment_part, params):
    print("")
    print("")
    print("")
    print(f"{colors.clr.fg.purple}********** QUERIES **********{colors.clr.reset}")
    print("")

    if len(line) == 1 and line[0] == '?':
        error_str = "no queries found."
        return display_error(-1, error_str, count, line)

    else:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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
                    pass
                else:
                    error_str = "invalid character for queries."
                    return display_error(col, error_str, count, line)
            col += 1
        
    if params["display_comments"] == 1 and len(comment_part) > 0:
        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}", end="          ")
        print(f"{colors.clr.fg.darkgrey}{comment_part}{colors.clr.reset}")
    
    else:
        print(f"{line} {colors.clr.fg.green}\u2713{colors.clr.reset}")
    
    return 0


def ex_parsing(params, path):
    params["tokens"] = []
    params["initial_facts"] = []
    params["queries"] = []
    params["parse_error"] = 0

    print(colors.clr.fg.yellow, f"Parsing {path}...", colors.clr.reset)
    print("")

    file = open(path, 'r')
    tokens = []
    query = []
    facts = []
    rules_phase = False
    fact_phase = False
    query_phase = False
    comment_part = ""
 
    count = 0
    while True:
        line = file.readline()

        if not line:
            break

        count += 1
        ind = 0
        line = sort_negative_symbol(line)
        for elt in line:
            if elt == "#":
                comment_part = line[ind:]
                line = line[:ind]
                comment_part = comment_part.strip()
                comment_part = comment_part.replace("\n", "")
                break
            ind += 1
        line = line.strip()
        line = line.replace(" ", "")
        line = line.replace("\n", "")

        if len(line) > 0 and line[0] == "?":
            if fact_phase == False:
                print("")
                print("")
                print("")
                print(f"{colors.clr.fg.purple}********** QUERIES **********{colors.clr.reset}")
                print("")
                display_error(-1, "you must initialize initials facts before queries.", count, line)
                print("")
                print(colors.clr.fg.red, f"{path} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                file.close()
                return params
            if query_phase == True:
                display_error(-1, "queries have already been initialized.", count, line)
                print("")
                print(colors.clr.fg.red, f"{path} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                file.close()
                return params
            else:
                query_phase = True
                result = check_queries(line, count, comment_part, params)
                if result == 1:
                    print("")
                    print(colors.clr.fg.red, f"{path} parse failed.", colors.clr.reset)
                    print("")
                    params["parse_error"] = 1
                    file.close()
                    return params
                else:
                    query = list(line[1:])

        elif len(line) > 0 and line[0] == "=":
            if fact_phase == True:
                display_error(-1, "the initial facts have already been initialized.", count, line)
                print("")
                print(colors.clr.fg.red, f"{path} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                file.close()
                return params
            else:
                fact_phase = True
                result = check_initial_facts(line, count, comment_part, params)
                if result == 1:
                    print("")
                    print(colors.clr.fg.red, f"{path} parse failed.", colors.clr.reset)
                    print("")
                    params["parse_error"] = 1
                    file.close()
                    return params
                else:
                    facts = list(line[1:])
                

        elif query_phase == False and fact_phase == False and len(line) > 0 and line[0] != "#":
            result = check_line(line, count, rules_phase)
            if result == 1:
                print("")
                print(colors.clr.fg.red, f"{path} parse failed.", colors.clr.reset)
                print("")
                params["parse_error"] = 1
                file.close()
                return params
            else:
                new_list = create_tokens(line, count, params, comment_part)
                if new_list == 1:
                    params["parse_error"] = 1
                    file.close()
                    return params

                tokens.append(new_list)
                rules_phase = True
        
        if params["display_comments"] == 1 and len(line) == 0 and len(comment_part) > 0:
            print("")
            print(f"{colors.clr.fg.darkgrey}{comment_part}{colors.clr.reset}")
            print("")

    
    params["tokens"] = tokens
    params["initial_facts"] = facts
    params["queries"] = query
    print("")
    print("")
    print("")
    print(colors.clr.fg.green, f"{path} parse success !", colors.clr.reset)
    print("")
    file.close()
    return params