from app_format_src.choose_file import choose_file
from app_format_src.ask_customs_params import ask_customs_params
from tools import colors
from parsing.parsing import ex_parsing
from parsing.custom_facts import get_user_facts
from parsing.custom_queries import get_user_queries
import os
from inference_engine.engine import InferenceEngine


def display_results(facts):
    false_facts = []
    true_facts = []
    none_facts = []

    for fact in facts:
        if fact.value == False:
            false_facts.append(fact.name)
        elif fact.value == True:
            true_facts.append(fact.name)
        else:
            none_facts.append(fact.name)
    
    print("")
    print("")
    print(colors.clr.fg.green, "--------------------------------------------------------------------------")
    print(f"  True facts ({len(true_facts)}) \u2192 ", " ".join(true_facts))
    print(colors.clr.fg.green, "--------------------------------------------------------------------------")
    print(colors.clr.fg.red, "--------------------------------------------------------------------------")
    print(f"  False facts ({len(false_facts)}) \u2192 " , " ".join(false_facts))
    print(colors.clr.fg.red, "--------------------------------------------------------------------------")
    print(colors.clr.fg.lightgrey, "--------------------------------------------------------------------------")
    print(f"  Unknown facts ({len(none_facts)}) \u2192 ", " ".join(none_facts))
    print(colors.clr.fg.lightgrey, "--------------------------------------------------------------------------", colors.clr.reset)
    print("")
    print("")

def expert_system_program(params):
    if params["path"] == None:
        path = "./datasets"
        answer = choose_file(path)

        if answer is None:
            if (params["tester"] == 0):
                print(colors.clr.fg.yellow, "WARNING: no valid file found, check your datasets folder.", colors.clr.reset)
            return params
        path = "./datasets/" + answer["datasets_file"]
    
    else:
        path = params["path"]
        if not os.path.exists(path):
            if (params["tester"] == 0):
                print(colors.clr.fg.yellow, "WARNING: file not found, check your datasets folder.", colors.clr.reset)
            return params

    params = ex_parsing(params, path)

    if params["parse_error"] == 0:
        engine = InferenceEngine(params["tokens"], params["initial_facts"], params["queries"])
        engine.infer_goals()
        facts_results = engine.print_facts()

        if params["tester"] == 0:
            display_results(facts_results)
        params["facts_results"] = false_facts

        if params['interactive_facts'] or params['interactive_queries']:
            answer_customs_params = ask_customs_params(params)
            while answer_customs_params["customs_params_answer"] == "Yes":
                if (params['interactive_facts']):
                    params["initial_facts"] = get_user_facts(params)
                if (params['interactive_queries']):
                    params["queries"] = get_user_queries(params)
                
                engine = InferenceEngine(params["tokens"], params["initial_facts"], params["queries"])
                engine.infer_goals()
                facts_results = engine.print_facts()
                display_results(facts_results)

                answer_customs_params = ask_customs_params(params)
                

    return params