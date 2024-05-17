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
            raise AssertionError("get settings src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [int(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    return tab[0]


def get_current_epochs_data(path: str):
    """
    Read a txt file
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("get params src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [float(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    if len(tab) != 2:
        print("")
        print("")
        print(colors.clr.fg.red, "Error: invalid current dimension, check current dimension file.", colors.clr.reset)
        exit(1)

    return int(tab[0])



def get_current_learning_rate_data(path: str):
    """
    Read a txt file
    """
    try:
        if not os.path.exists(path):
            raise AssertionError("get params src failed.")
        file = open(path, "r")
        first_line = file.readline()
        tab = [float(x) for x in first_line.split()]
        file.close()
    except AssertionError as error:
        print(colors.clr.fg.red, "Error:", error, colors.clr.reset)
        exit(1)

    if len(tab) != 2:
        print("")
        print("")
        print(colors.clr.fg.red, "Error: invalid current dimension, check current dimension file.", colors.clr.reset)
        exit(1)

    return tab[1]


def get_gen_params():
    path_dic = get_gen_params_settings_path()

    src_dic = {}
    src_dic["tokens"] = None
    src_dic["initial_facts"] = None
    src_dic["queries"] = None
    src_dic["parse_error"] = 0
    #src_dic["dynamic_graph"] = get_int_data(path_dic["dynamic_graph"])
    # src_dic["learning_rate"] = get_current_learning_rate_data(path_dic["current_dimension"])
    # src_dic["epochs"] = get_current_epochs_data(path_dic["current_dimension"])

    # src_dic["X_train"] = None
    # src_dic["y_train"] = None
    # src_dic["X_test"] = None
    # src_dic["y_test"] = None
    # src_dic["parametres"] = None
    # src_dic["dataset_name"] = None

    return src_dic
