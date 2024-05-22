import inquirer
import os
from tools import colors
from expert_system_program import expert_system_program
from app_format_src.datasets_test_program import datasets_test_program

def programs_step_display():
	print(colors.clr.fg.cyan)
	print("")
	print("")
	print("####################################################################################################################")
	print("")
	print("                                                 Choose program                                                     ")
	print("")
	print("")
	print("")

	questions = [
    inquirer.List(
        "program",
        message="This program is composed of 1 sub-programs, choose the one that interests you",
        choices=["Datasets test", "Expert-system", "Back"],
    ),
	]
	return inquirer.prompt(questions)


def programs_step(params):
	while True:
		answer = programs_step_display()
		if answer["program"] == "Datasets test":
			params = datasets_test_program(params)
		if answer["program"] == "Expert-system":
			params = expert_system_program(params)
		if answer["program"] == "Back":
			break