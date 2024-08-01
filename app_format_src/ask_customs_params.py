import inquirer
from tools import colors


def ask_customs_params(params):
    print(colors.clr.fg.cyan)
    print("")
    print("")
    print("####################################################################################################################")
    print("")
    if params["interactive_facts"] == 1 and params['interactive_queries'] == 1:
        print("                             Do you want to reload the program with custom facts and queries?                                         ")
    if params["interactive_facts"] == 1 and params['interactive_queries'] == 0:
        print("                                  Do you want to reload the program with custom facts ?                                         ")
    if params["interactive_facts"] == 0 and params['interactive_queries'] == 1:
        print("                                 Do you want to reload the program with custom queries ?                                         ")
    print("")
    print("")
    print("")


    questions = [
    inquirer.List(
        "customs_params_answer",
        message="",
        choices=["Yes", "No"],
    ),
    ]
    return inquirer.prompt(questions)