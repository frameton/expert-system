import inquirer
from tools import colors
from app_format_src.display_comments_settings import display_comments_settings
from app_format_src.display_nested_list_settings import display_nested_list_settings
from app_format_src.display_facts_settings import interactive_facts_settings
from app_format_src.display_queries_settings import interactive_queries_settings


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
        choices=["Display comments", "Display nested list", "Interactive facts", "Interactive queries", "Back"],
    ),
	]
	return inquirer.prompt(questions)


def settings_step(params):
    while True:
        answer = settings_step_display()
        if answer["settings_step_answer"] == "Display comments":
            params = display_comments_settings(params)
        if answer["settings_step_answer"] == "Display nested list":
            params = display_nested_list_settings(params)
        if answer["settings_step_answer"] == "Interactive facts":
            params = interactive_facts_settings(params)
        if answer["settings_step_answer"] == "Interactive queries":
            params = interactive_queries_settings(params)
        if answer["settings_step_answer"] == "Back":
            break
    return params