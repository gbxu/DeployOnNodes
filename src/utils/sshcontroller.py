#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-02-02
@author: gb.xu
@mail: gb.xu@outlook.com
"""
import paramiko
from src.utils import databean
from src.utils import context

class SSHController(object):
    def __init__(self, node):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.node = node
        self.channel = None

    def __del__(self):
        if self.channel is not None:
            self.channel.close()
        if self.client is not None:
            self.client.close()

    def connect_host(self):
        self.client.connect(hostname=self.node.host, port=self.node.port,
                            username=self.node.user, key_filename=self.node.key)
        context.verbose("... connected with key on Linux")

    def exec_command(self, command):
        context.verbose("... exec the command:"+"\n"+command)
        stdin, stdout, stderr = self.client.exec_command(command)
        context.verbose("... result:")
        for line in stdout:
            context.verbose(line.strip("\n"))

    def close_all(self):
        print("... closing the socket")
        if self.channel is not None:
            self.channel.close()
        if self.client is not None:
            self.client.close()


def multi_ssh():
    """
    connect to local port via ssh.
    :return:
    """
    pass


if __name__ == "__main__":
    """
    test
    """
    remote_nodes, server_node = databean.get_nodes()
    # test gpu1
    ssh_client = SSHController(server_node)
    ssh_client.connect_host()
    ssh_client.exec_command("ls")
    ssh_client.close_all()

