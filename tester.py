from app_format_src.get_gen_params import get_gen_params
from app_format_src.save_params import save_params
from expert_system_program import expert_system_program
from os import walk

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

if __name__ == "__main__":

    params = {}
    params = set_params_for_tester(params)

    basics = []
    path = "./tests_subject/basics"
    for (path, dirnames, filenames) in walk(path):
        for elt in filenames:
            basics.append(elt)
        break
    
    errors = []
    path = "./tests_subject/errors"
    for (path, dirnames, filenames) in walk(path):
        for elt in filenames:
            errors.append(elt)
        break

    hards = []
    path = "./tests_subject/hards"
    for (path, dirnames, filenames) in walk(path):
        for elt in filenames:
            hards.append(elt)
        break

    # for basic in basics:
    #     print(basic)

    # print()
    # print()

    # for error in errors:
    #     print(error)

    # print()
    # print()

    # for hard in hards:
    #     print(hard)


    params["path"] = "./tests_subject/basics/basic_and2"
    params = expert_system_program(params)

    tab = []
    for fact in params["facts_results"]:
        tab2 = []
        tab2.append(fact.name)
        if fact.value == False:
            tab2.append(False)
        elif fact.value == True:
            tab2.append(True)
        # else:
        #     none_facts.append(fact.name)
        tab.append(tab2)
    
    sort1 = sorted(params["tester_reference"])
    sort2 = sorted(tab)

    print(sort1)
    print(sort2)

    exit()