#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-01-31
@author: gb.xu
@mail: gb.xu@outlook.com
"""
import sys
from src.utils import forward
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:  # only file name
        print('Hello, world!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

    forward.multi_forward()