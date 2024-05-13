import inquirer
from tools import colors


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
        choices=["Settings1", "Back"],
    ),
	]
	return inquirer.prompt(questions)


def settings_step(params):
    while True:
        answer = settings_step_display()
        if answer["settings_step_answer"] == "Settings1":
            print("Settings1")
        if answer["settings_step_answer"] == "Back":
            break
    return params