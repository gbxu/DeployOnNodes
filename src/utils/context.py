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
# Variables with simple values
version = "0.0.1"
g_verbose = True

# variables with complex values
path = [
    "../../conf/nodes_forward.json",
    "../../conf/nodes_forward_local.json"
]

keyfile = [
    "/home/gbxu/.ssh/id_rsa",
    "/Users/gbxu/.ssh/id_rsa"
]

username = "gbxu"
# classes

# functions


def get_local_key():
    if platform.system() == "Linux":
        return keyfile[0]
    elif platform.system() == "Darwin":
        return keyfile[1]
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