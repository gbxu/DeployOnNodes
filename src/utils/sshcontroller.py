#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-02-02
@author: gb.xu
@mail: gb.xu@outlook.com
"""
# imports
import sys
import paramiko

# Variables with simple values
nodenum = 3
version = "0.0.1"
# variables with complex values
path = [
    "../conf//",
    "/home/gbxu/app"
]
# classes


class SSHController(object):
    def __init__(self, node):
        self.node = node

    def __str__(self):
        return "Student object (name:%s)" %self.name

    def __test(self):
        pass

# functions


if __name__ == "__main__":
    """
    from here, we will start the SSH connection.
    """
    args = sys.argv
    if len(args) == 1:  # only file name
        print('Hello, world!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')
