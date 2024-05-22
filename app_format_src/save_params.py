import pandas as pd
import os
from tools import colors
from app_format_src.get_gen_params_settings_path import get_gen_params_settings_path


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


def save_display_comments(params, path):
    string = str(params["display_comments"])

    try:
        file1 = open(path, 'w')
        file1.write(string)
        file1.close()
    except Exception as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)


def save_params(params):
    path_dic = get_gen_params_settings_path()

    save_display_comments(params, path_dic["display_comments"])