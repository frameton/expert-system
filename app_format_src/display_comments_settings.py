import inquirer
from tools import colors


def display_comments_setting_step_display(status):
    print(colors.clr.fg.cyan)
    print("")
    print("")
    print("####################################################################################################################")
    print("")
    print("                                              Display comments setting                                               ")
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
        "display_comments_setting_step_answer",
        message="Enable or disable display comments mode for parsing",
        choices=["On", "Off", "Back"],
    ),
    ]
    return inquirer.prompt(questions)


def display_comments_settings(params):
    while True:
        answer = display_comments_setting_step_display(params["display_comments"])
        if answer["display_comments_setting_step_answer"] == "On":
            params["display_comments"] = 1
        if answer["display_comments_setting_step_answer"] == "Off":
            params["display_comments"] = 0
        if answer["display_comments_setting_step_answer"] == "Back":
            break
    return params