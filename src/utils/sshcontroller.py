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
import sys
from multiprocessing import Pool


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
        context.verbose("... connected %s with key on Linux" %self.node.name)

    def exec_command(self, command):
        context.verbose("...%s exec the command:" % self.node.name + command)
        stdin, stdout, stderr = self.client.exec_command(command)
        context.verbose("... %s result:" % self.node.name)
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
        print("... closing the %s socket" % self.node.name)
        if self.client is not None:
            self.client.close()


def do_exec_command(ssh, commands):
    ssh.connect()
    for command in commands:
        ssh.exec_command(command)
    ssh.close()


def multi_ssh():
    """
    connect to local port via ssh.
    :return:
    """
    remote_nodes, _ = databean.get_nodes(context.path[1])
    if remote_nodes is None:
        context.verbose("there are not the forwarding to localhost")
        return

    cmds = databean.get_commands()
    ssh = {}  # ssh = {"gpu1":SSHController}
    for node in remote_nodes:
        if node.name in cmds.keys():
            ssh[node.name] = SSHController(node)

    processes = []
    p = Pool(len(ssh))
    try:
        for tmp in ssh.keys():
            p.apply_async(do_exec_command, args=(ssh[tmp], cmds[tmp]))
        p.close()
        p.join()
    except:
        print("Error: unable to start process")
    return processes


if __name__ == "__main__":
    """
    test
    remote_nodes, server_node = databean.get_nodes()
    # test gpu1
    ssh_client = SSHController(server_node)
    ssh_client.connect()
    ssh_client.exec_command("ls")
    ssh_client.close()
    """
    multi_ssh()
