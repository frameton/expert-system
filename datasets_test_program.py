from choose_file import *
from tools import colors
from parsing import *


def datasets_test_program(params):
    path = "./datasets_test/"
    answer = choose_file(path)

    if answer is None:
        print(colors.clr.fg.yellow, "WARNING: no valid file found, check your datasets folder.", colors.clr.reset)
        return params
    path = "./datasets_test/" + answer["datasets_file"]
   

    params = ex_parsing(params, path)

    return params