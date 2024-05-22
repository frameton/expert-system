from os import walk
import inquirer
from tools import colors


def choose_file(path):
	print(colors.clr.fg.cyan)
	print("")
	print("")
	print("####################################################################################################################")
	print("")
	print("                                              Choose dataset file                                                   ")
	print("")
	print("")
	print("")

	f = []
	for (dirpath, dirnames, filenames) in walk(path):
		for elt in filenames:
			if elt.lower().endswith('.txt'):
				f.append(elt)
		break
	if len(f) == 0:
		return None

	questions = [
	inquirer.List(
		"datasets_file",
		message="Choose file",
        choices=f,
    ),
	]
	return inquirer.prompt(questions)