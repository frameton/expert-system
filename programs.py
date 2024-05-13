import inquirer
import os
from tools import colors
from expert_system_program import *

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
        choices=["Expert-system", "Back"],
    ),
	]
	return inquirer.prompt(questions)


def programs_step(params):
  while True:
    answer = programs_step_display()
    if answer["program"] == "Expert-system":
      params = expert_system_program(params)
    if answer["program"] == "Back":
      break