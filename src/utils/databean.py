import json
import platform
from src.utils import context


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


def get_nodes():
    with open(context.path[0], "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    rdata = data["remote_nodes"]
    sdata = data["server_node"]
    remote_nodes = []
    for tmp in rdata:
        if platform.system() == "Linux":
            node = Node(tmp["name"], tmp["host"], tmp["port"], tmp["user"], tmp["key_linux"])
        elif platform.system() == "Darwin":
            node = Node(tmp["name"], tmp["host"], tmp["port"], tmp["user"], tmp["key_darwin"])
        else:
            # TODO: need modify in Windows
            context.verbose("Windows" + " isn't fit")
        remote_nodes.append(node)
    tmp = sdata
    server_node = Node(tmp["name"], tmp["host"], tmp["port"], tmp["user"], tmp["key_darwin"])
    return remote_nodes, server_node


def get_forward_local():
    with open(context.path[1], "r", encoding="utf-8") as nodes_forward_local:
        data = json.load(nodes_forward_local)
    return data


if __name__ == '__main__':
    """
    test
    """
