#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-01-31
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
    "/home/gbxu",
    "/home/gbxu/app"
]
# classes


class Student(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Student object (name:%s)" %self.name

    def __test(self):
        pass

# functions


def func():
    pass


def _pro():
    """
    this function is protected in the package.
    :return: None
    """
    pass


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:  # only file name
        print('Hello, world!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')