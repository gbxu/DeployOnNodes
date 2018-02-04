#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-02-03
@author: gb.xu
@mail: gb.xu@outlook.com
"""

import json
from src.utils import context

conf = context.get_conf()

class ForwardOptions(object):
    def __init__(self, user, key, shost, sport, rhost, rport):
        self.user = user
        self.key = key
        self.server = [shost, sport]
        self.remote = [rhost, rport]


class Node(object):
    """
    parse nodes_*.json from configuration file to the
    """
    def __init__(self, name, host, port, user, key):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.key = key


def get_nodes(filepath):
    with open(filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    remote_nodes = []
    server_node = None
    if "remote_nodes" in data:
        rdata = data["remote_nodes"]
        sdata = data["server_node"]
        for tmp in rdata:
            node = Node(tmp["name"], tmp["host"], tmp["port"], conf["user"], conf["key"])
            remote_nodes.append(node)

        tmp = sdata
        server_node = Node(tmp["name"], tmp["host"], tmp["port"], conf["user"], conf["key"])
    else:
        for tmp in data:
            node = Node(tmp["name"], tmp["host"], tmp["port"], conf["user"], conf["key"])
            remote_nodes.append(node)
    return remote_nodes, server_node


def get_commands():
    with open(context.path[3],"r",encoding="utf-8") as json_file:
        data = json.load(json_file)
    cmds = {}
    for tmp in data:
        cmds[tmp["name"]] = tmp["commands"]
    return cmds


if __name__ == '__main__':
    """
    test
    """
