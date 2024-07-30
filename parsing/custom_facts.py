from tools import colors


def check_initial_facts(line):
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
                    print(colors.clr.fg.red, "invalid character for initial facts.")
                    print("")
                    return False
            col += 1

    return True


def get_user_facts(params):
    validation = False
    letters_list = params["dataset_letters"]
    while validation == False:
        print("")
        print(colors.clr.fg.yellow, "------------------------- Choose your own facts ! (ex: AEG) -------------------------")
        print(colors.clr.fg.yellow, f"Letter(s) found in dataset: {' '.join(letters_list)}")
        print("")
        facts = input("Facts: ")
        facts = facts.strip()
        facts = facts.replace(" ", "")
        facts = facts.replace("\n", "")
        validation = check_initial_facts(facts)

    print(colors.clr.reset)
    print(f"{colors.clr.fg.purple}FACTS is set ! \u2192 {facts}{colors.clr.reset}")

    return list(facts)