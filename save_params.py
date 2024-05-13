import pandas as pd
import os
from tools import colors
from get_gen_params_settings_path import *


def get_int_data(path: str):
    """
    Read a txt file
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("get params src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [int(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    return tab[0]


def save_current_dimension(params, path):
    string = str(params["epochs"]) + " " + str(params["learning_rate"])

    try:
        file1 = open(path, 'w')
        file1.write(string)
        file1.close()
    except Exception as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)


def save_params(params):
    path_dic = get_gen_params_settings_path()

    # save_current_dimension(params, path_dic["current_dimension"])