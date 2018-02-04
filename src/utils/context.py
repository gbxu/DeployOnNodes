#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-02-03
@author: gb.xu
@mail: gb.xu@outlook.com
"""
# import
import platform
import json
# Variables with simple values
version = "0.0.1"
g_verbose = True

# variables with complex values
path = [
    "../../conf/nodes_forward.json",
    "../../conf/nodes_local.json",
    "../../conf/conf.json",
    "../../conf/exec_list.json"
]

# classes

# functions


def get_conf():
    with open(path[2], "r", encoding="utf-8") as json_file:
        conf = json.load(json_file)
    local_key_name = get_local_key_name()
    key = conf[local_key_name]
    del conf["key_linux"]
    del conf["key_darwin"]
    conf["key"] = key
    return conf


def get_local_key_name():
    if platform.system() == "Linux":
        return "key_linux"
    elif platform.system() == "Darwin":
        return "key_darwin"
    else:
        # TODO: need modify in Windows
        verbose("Windows" + " isn't fit")
        return None


def verbose(s, flag=g_verbose):
    """
    print
    :param
        s: input string
        flag: turn on/off the print
    :return:
    """
    if flag:
        print(s)