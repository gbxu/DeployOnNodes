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
from src.utils.databean import Node
import sys
from multiprocessing import Process


class SSHController(object):
    def __init__(self, node):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.node = node

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def connect(self):
        self.client.connect(hostname=self.node.host, port=self.node.port,
                            username=self.node.user, key_filename=self.node.key)
        context.verbose("... connected with key on Linux")

    def exec_command(self, command):
        context.verbose("... exec the command:"+"\n"+command)
        stdin, stdout, stderr = self.client.exec_command(command)
        context.verbose("... result:")
        for line in stdout:
            context.verbose(line.strip("\n"))

    def upload(self):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.put('demo_sftp.py', 'demo_sftp_folder/demo_sftp.py')
            self.close()
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            try:
                self.close()
            except:
                pass
            sys.exit(1)

    def download(self):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.client.get_transport())
            sftp.get('demo_sftp_folder/README', 'README_demo_sftp')
            self.close()
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            try:
                self.close()
            except:
                pass
            sys.exit(1)

    def close(self):
        print("... closing the socket")
        if self.client is not None:
            self.client.close()


def multi_ssh():
    """
    connect to local port via ssh.
    :return:
    """
    local_key = context.get_local_key()
    data = databean.get_forward_local()
    forward_local_ports = []
    for tmp in data:
        forward_local_ports.append(Node(tmp.name, "localhost", tmp.port, Node, Node))
    ssh = {}
    for tmp in forward_local_ports:
        ssh[tmp.name] =  SSHController(Node(tmp.name, "localhost", tmp.port, context.username, local_key))

    processes = []
    try:
        lambda ssh[] # 添加command的host 产生对应进程，执行
        p = Process(target=do_forward, args=(options, free_port))
        p.start()
        processes.append((remote_node.name, p))
    except:
        print("Error: unable to start process")
    with open(context.path[1], "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(forward_local_ports))
    return processes


if __name__ == "__main__":
    """
    test
    """
    remote_nodes, server_node = databean.get_nodes()
    # test gpu1
    ssh_client = SSHController(server_node)
    ssh_client.connect()
    ssh_client.exec_command("ls")
    ssh_client.close()

