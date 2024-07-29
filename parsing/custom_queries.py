from tools import colors


def check_initial_queries(line):
    if len(line) == 1 and line[0] == '=':
        return False
    
    if len(line) == 0:
        return False

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
                    print("")
                    print(colors.clr.fg.red, "invalid character for initial queries.")
                    print("")
                    return False
            col += 1

    return True


def get_user_queries(params):
    validation = False
    letters_list = params["dataset_letters"]
    while validation == False:
        print("")
        print(colors.clr.fg.yellow, "------------------------- Choose your own queries ! (ex: AEG) -------------------------")
        print(colors.clr.fg.yellow, f"Letter(s) found in dataset: {letters_list}")
        print("")
        queries = input("Queries: ")
        queries = queries.strip()
        queries = queries.replace(" ", "")
        queries = queries.replace("\n", "")
        validation = check_initial_queries(queries)

    print(colors.clr.reset)
    print(f"{colors.clr.fg.purple}QUERIES is set ! \u2192 {queries}{colors.clr.reset}")
    print("")
    print("")

    return list(queries)