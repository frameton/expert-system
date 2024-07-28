import inquirer
from tools import colors


def interactive_facts_setting_step_display(status):
    print(colors.clr.fg.cyan)
    print("")
    print("")
    print("####################################################################################################################")
    print("")
    print("                                              Interactive facts setting                                               ")
    print("")
    if status == 0:
        print(colors.clr.fg.red)
        print("                                                     Satut: Off                                                  ")
        print(colors.clr.reset)
    if status == 1:
        print(colors.clr.fg.green)
        print("                                                      Satut: On                                                  ")
        print(colors.clr.reset)
    print("")
    print("")
    print("")

    questions = [
    inquirer.List(
        "interactive_facts_setting_step_answer",
        message="Enable or disable interactive facts mode",
        choices=["On", "Off", "Back"],
    ),
    ]
    return inquirer.prompt(questions)


def interactive_facts_settings(params):
    while True:
        answer = interactive_facts_setting_step_display(params["interactive_facts"])
        if answer["interactive_facts_setting_step_answer"] == "On":
            params["interactive_facts"] = 1
        if answer["interactive_facts_setting_step_answer"] == "Off":
            params["interactive_facts"] = 0
        if answer["interactive_facts_setting_step_answer"] == "Back":
            break
    return params