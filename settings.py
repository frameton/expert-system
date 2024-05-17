import inquirer
from tools import colors
from display_comments_settings import *


def settings_step_display():
	print(colors.clr.fg.cyan)
	print("")
	print("")
	print("####################################################################################################################")
	print("")
	print("                                                     Settings                                                       ")
	print("")
	print("")
	print("")

	questions = [
    inquirer.List(
        "settings_step_answer",
        message="Dslr settings",
        choices=["Display comments", "Back"],
    ),
	]
	return inquirer.prompt(questions)


def settings_step(params):
    while True:
        answer = settings_step_display()
        if answer["settings_step_answer"] == "Display comments":
            params = display_comments_settings(params)
        if answer["settings_step_answer"] == "Back":
            break
    return params