from programs import *
from settings import *
from get_gen_params import *
from save_params import *
import inquirer


def home_step_display():
	print(colors.clr.fg.cyan)
	print("")
	print("")
	print("####################################################################################################################")
	print("")
	print("                                         Welcome to Total Expert System !                                          ")
	print("")
	print("")
	print("")

	questions = [
    inquirer.List(
        "home_step_answer",
        message="",
        choices=["Programs", "Settings", "Exit"],
    ),
	]
	return inquirer.prompt(questions)


def home_step():
    params = get_gen_params()
    params["path"] = None

    while True:
        answer = home_step_display()
        if answer["home_step_answer"] == "Programs":
            programs_step(params)
        if answer["home_step_answer"] == "Settings":
            params = settings_step(params)
        if answer["home_step_answer"] == "Exit":
            save_params(params)
            break