from app_format_src.choose_file import choose_file
from tools import colors
from parsing.parsing import ex_parsing
import os
from inference_engine.engine import InferenceEngine


def expert_system_program(params):
    if params["path"] == None:
        path = "./datasets"
        answer = choose_file(path)

        if answer is None:
            print(colors.clr.fg.yellow, "WARNING: no valid file found, check your datasets folder.", colors.clr.reset)
            return params
        path = "./datasets/" + answer["datasets_file"]
    
    else:
        path = params["path"]
        if not os.path.exists(path):
            print(colors.clr.fg.yellow, "WARNING: file not found, check your datasets folder.", colors.clr.reset)
            return params

    params = ex_parsing(params, path)

# execute seulement si le parsing est un reussit
    if params["parse_error"] == 0:
        engine = InferenceEngine(params["tokens"], params["initial_facts"], params["queries"])
        engine.infer_goals()
        engine.print_facts()

    return params
###############################################""