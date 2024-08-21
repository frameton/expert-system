from app_format_src.get_gen_params import get_gen_params
from app_format_src.save_params import save_params
from expert_system_program import expert_system_program
from os import walk
from tools import colors

def set_params_for_tester(params):
    params["tokens"] = None
    params["initial_facts"] = None
    params["queries"] = None
    params["parse_error"] = 0
    params["display_comments"] = 0
    params["display_nested_list"] = 0
    params["interactive_facts"] = 0
    params["interactive_queries"] = 0
    params["tester"] = 1
    params["facts_results"] = None
    return params

def tester_mode():

    params = {}

    basics = []
    path = "./tester_src/basics"
    for (path, dirnames, filenames) in walk(path):
        for elt in filenames:
            basics.append(elt)
        break
    
    errors = []
    path = "./tester_src/errors"
    for (path, dirnames, filenames) in walk(path):
        for elt in filenames:
            errors.append(elt)
        break

    hards = []
    path = "./tester_src/hards"
    for (path, dirnames, filenames) in walk(path):
        for elt in filenames:
            hards.append(elt)
        break

    print(colors.clr.fg.cyan, "######################## Expert-System Tester ###########################", colors.clr.reset)
    print("")
    print("")

    print(colors.clr.fg.cyan, "******************** Basics test ********************", colors.clr.reset)
    print("")
    for basic in basics:
        params = set_params_for_tester(params)
        params["path"] = "./tester_src/basics/" + basic
        params = expert_system_program(params)

        facts_results = []
        total_facts_results = []
        if params["facts_results"] != None:
            for fact in params["facts_results"]:
                tab2 = []
                tab2.append(fact.name)
                if fact.value == False:
                    tab2.append(False)
                elif fact.value == True:
                    tab2.append(True)
                else:
                    tab2.append(fact.value)
                total_facts_results.append(tab2)
                if fact.name in params["queries"]:
                    facts_results.append(tab2)

        expected_output = sorted(params["tester_reference"])
        facts_results = sorted(facts_results)

        error = 0
        if len(expected_output) != len(facts_results):
            error = 1

        if error == 0:
            index = 0
            for elt in expected_output:
                if len(expected_output[index]) != len(facts_results[index]):
                    error = 1
                    break
                if expected_output[index][1] != facts_results[index][1]:
                    error = 1
                    break
                index += 1

        if error == 0:
            print(f"{colors.clr.fg.green}|{colors.clr.reset} ./tester_src/basics/{basic} {colors.clr.fg.green}\u2713{colors.clr.reset}")
            print(f"{colors.clr.fg.green}|{colors.clr.reset}     Expected output:   {expected_output}")
            print(f"{colors.clr.fg.green}|{colors.clr.reset}     Program output:    {facts_results}      total_input->  {total_facts_results}   ")
            print("")
        
        if error == 1:
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset} ./tester_src/basics/{basic} {colors.clr.fg.lightred}\u2717{colors.clr.reset}")
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset}     Expected output:   {expected_output}")
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset}     Program output:    {facts_results}      total_input->  {total_facts_results}   ")
            print("")
        
        # if params["tester_infos"] == 1:
        #     print(f"Expected output:   {expected_output}")
        #     print(f"Program output:    {facts_results}")
        #     print("")

    print("")
    print("")
    print(colors.clr.fg.cyan, "******************** Hards test ********************", colors.clr.reset)
    print("")
    for hard in hards:
        params = set_params_for_tester(params)
        params["path"] = "./tester_src/hards/" + hard
        params = expert_system_program(params)

        facts_results = []
        total_facts_results = []
        if params["facts_results"] != None:
            for fact in params["facts_results"]:
                tab2 = []
                tab2.append(fact.name)
                if fact.value == False:
                    tab2.append(False)
                elif fact.value == True:
                    tab2.append(True)
                else:
                    tab2.append(fact.value)
                total_facts_results.append(tab2)
                if fact.name in params["queries"]:
                    facts_results.append(tab2)

        expected_output = sorted(params["tester_reference"])
        facts_results = sorted(facts_results)

        error = 0
        if len(expected_output) != len(facts_results):
            error = 1

        if error == 0:
            index = 0
            for elt in expected_output:
                if len(expected_output[index]) != len(facts_results[index]):
                    error = 1
                    break
                if expected_output[index][1] != facts_results[index][1]:
                    error = 1
                    break
                index += 1
        if error == 0:
            print(f"{colors.clr.fg.green}|{colors.clr.reset} ./tester_src/hards/{hard} {colors.clr.fg.green}\u2713{colors.clr.reset}")
            print(f"{colors.clr.fg.green}|{colors.clr.reset}     Expected output:   {expected_output}")
            print(f"{colors.clr.fg.green}|{colors.clr.reset}     Program output:    {facts_results}      total_input->  {total_facts_results}   ")
            print("")
        
        if error == 1:
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset} ./tester_src/hards/{hard} {colors.clr.fg.lightred}\u2717{colors.clr.reset}")
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset}     Expected output:   {expected_output}")
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset}     Program output:    {facts_results}      total_input->  {total_facts_results}   ")
            print("")


    
    print("")
    print("")
    print(colors.clr.fg.cyan, "******************** Errors test ********************", colors.clr.reset)
    print("")
    for error in errors:
        params = set_params_for_tester(params)
        params["path"] = "./tester_src/errors/" + error
        params = expert_system_program(params)

        if params["parse_error"] == 1:
            print(f"{colors.clr.fg.green}|{colors.clr.reset} ./tester_src/errors/{error} {colors.clr.fg.green}\u2713{colors.clr.reset}")
            print(f"{colors.clr.fg.green}|{colors.clr.reset}     An error is expected and the program return an error.")
            print("")
        
        if params["parse_error"] == 0:
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset} ./tester_src/errors/{error} {colors.clr.fg.lightred}\u2717{colors.clr.reset}")
            print(f"{colors.clr.fg.lightred}|{colors.clr.reset}     An error is expected and the program don't return an error.")
            print("")