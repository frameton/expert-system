from choose_file import *
from tools import colors
from parsing import *

############################## ton code ############################
def your_function(params):
    # params["tokens"] -> tableau de tableaux avec tous les tokens ex: [['C', '=', '>', 'E'], ['A', '+', 'B', '+', 'C', '=', '>', 'D']]
    # params["initial_facts"] -> tableau des faits initiaux ex: ['A', 'G', 'P']
    # params[queries] -> tableau des queries ex: ['K', 'M', 'S']
    print(params)







######################################################################







def expert_system_program(params):
    path = "./datasets"
    answer = choose_file(path)

    if answer is None:
        print(colors.clr.fg.yellow, "WARNING: no valid file found, check your datasets folder.", colors.clr.reset)
        return params

    params = ex_parsing(params, answer["datasets_file"], path)

# execute seulement si le parsing est un reussit
    if params["parse_error"] == 0:
        your_function(params)
###############################################""