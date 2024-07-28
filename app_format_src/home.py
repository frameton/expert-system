from app_format_src.programs import programs_step
from app_format_src.get_gen_params import get_gen_params
from app_format_src.save_params import save_params
from app_format_src.settings import settings_step
from tools import colors
import inquirer


def home_step_display():
	print(colors.clr.fg.cyan)
	print("")
	print("")
	print("####################################################################################################################")
	print("")
	print("                                              Welcome to Expert System !                                          ")
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