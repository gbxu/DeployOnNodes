#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-02-03
@author: gb.xu
@mail: gb.xu@outlook.com
"""
# import
# Variables with simple values
version = "0.0.1"
g_verbose = True

# variables with complex values
path = [
    "../../conf/nodes_forward.json",
    "../../conf/nodes_forward_local.json"
]
# classes

# functions

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