#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-01-31
@author: gb.xu
@mail: gb.xu@outlook.com
"""
import sys
from src.utils import sshcontroller
from src.utils import context
from src.utils import databean
import json
import os
conf = context.get_conf()


def check_env():
    if conf["machine"] == "local":
        flag = False
        for str in os.popen("ps -ef|grep forward").readlines():
            if "forward" in str and "grep" not in str:
                flag = True
                break
        if flag is not True:
            context.verbose("run forward.py first!")
            return False
    else:  # on server machine
        # TODO: need to update the nodes_local.json
        remote_nodes, _ = databean.get_nodes(context.path[0])
        local_ports = []
        for remote_node in remote_nodes:
            local_ports.append({"name": remote_node.name,
                                "host": remote_node.host,
                                "port": remote_node.port
                                })
        with open(context.path[1], "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(local_ports))
    return True


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:  # only file name
        print('Hello, world!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

    if check_env():
        # sshcontroller.multi_do_upload("../../resource/upload", "./")
        sshcontroller.multi_do_exec_command()
        # sshcontroller.multi_do_download("./folder_from_server", "../../resource/download/"+"folder_from_server/")
    else:
        sys.exit(0)

    # subprocess.call([sys.executable, "../utils/forward.py"])
    # subprocess.call([sys.executable, "../utils/sshcontroller.py"])

    # p1 = Process(target=forward.multi_forward, args=())
    # p1.start()
    # p2 = Process(target=sshcontroller.multi_ssh, args=())
    # p2.start()
