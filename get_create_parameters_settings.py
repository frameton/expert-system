import pandas as pd
import os
from tools import colors
from get_parameters_settings_path import *


def get_int_data(path: str):
    """
    Read a txt file
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("get settings src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [int(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    return tab


def get_tab_int_data(path: str):
    """
    Read a txt file
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("get settings src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [int(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    return tab


def get_tab_float_data(path: str):
    """
    Read a txt file
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("get settings src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [float(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    return tab


def get_create_parameters_settings():
    path_dic = get_parameters_settings_path()
    
    src_dic = {}
    # src_dic["epochs"] = get_tab_int_data(path_dic["epochs"])
    # src_dic["learning_rate"] = get_tab_float_data(path_dic["learning_rate"])

    return src_dic
