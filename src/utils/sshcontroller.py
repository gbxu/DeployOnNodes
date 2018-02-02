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
import json
import paramiko

# Variables with simple values
node_num = 3
version = "0.0.1"
# variables with complex values
path = [
    "../conf/nodes.json",
    "../conf"
]
# classes


class Node(object):
    def __init__(self, name, host, port, user, passwd, keypair):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.keypair = keypair


class SSHController(object):
    def __init__(self, node):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.node = node
        self.stdin, self.stdout, self.stderr = "", "", ""

    def start_with_passwd(self, node):
        self.client.connect(hostname=node.host, port=node.port, username=node.user, password=node.passwd)

    def start_with_key(self, node):
        self.client.connect(hostname=node.host, port=node.port, username=node.user, key_filename=node.keypair)

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        print(stdout)

    def set_command(self, command):
        pass

    def close(self):
        self.client.close()

# functions


def get_nodes():
    nodes = []
    with open(path[0], "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    for tmp in data:
        node = Node(tmp, tmp["host"], tmp["port"], tmp["user"], tmp["passwd"], tmp["keypair"])
        nodes.append(node)
    return nodes


def multi_ssh():
    pass


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
