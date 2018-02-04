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
import os
import stat
from multiprocessing import Pool


class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        """
        Uploads the contents of the source directory to the target path. The
        target directory needs to exists. All subdirectories in source are
        created under target.
        :param source:
        :param target:
        :return:
        """
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

    def get_dir(self, remote_dir, local_dir):
        os.path.exists(local_dir) or os.makedirs(local_dir)
        dir_items = self.listdir_attr(remote_dir)
        for item in dir_items:
            local_path = os.path.join(local_dir, item.filename)
            remote_path = remote_dir+"/"+item.filename
            if stat.S_ISDIR(item.st_mode):
                self.get_dir(remote_path, local_path)
            else:
                self.get(remote_path, local_path)


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
        context.verbose("... connected %s with key on Linux" % self.node.name)

    def exec_command(self, command):
        context.verbose("...%s exec the command:" % self.node.name + command)
        stdin, stdout, stderr = self.client.exec_command(command)
        context.verbose("... %s result:" % self.node.name)
        for line in stdout:
            context.verbose(line.strip("\n"))

    def upload(self, localpath, remotepath="./"):
        try:
            sftp = MySFTPClient.from_transport(self.client.get_transport())
            # sftp.put(localpath, remotepath)
            sftp.put_dir(localpath, remotepath)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            try:
                self.close()
            except:
                pass
            sys.exit(1)

    def download(self, remotepath, localpath):
        try:
            sftp = MySFTPClient.from_transport(self.client.get_transport())
            # sftp.get(remotepath, localpath)
            sftp.get_dir(remotepath, localpath)
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


def multi_do_exec_command():
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


def do_upload(ssh, localpath, remotepath="./"):
    ssh.connect()
    ssh.upload(localpath, remotepath)
    ssh.close()


def multi_do_upload(localpath, remotepath="./"):
    remote_nodes, _ = databean.get_nodes(context.path[1])
    if remote_nodes is None:
        context.verbose("there are not the forwarding to localhost")
        return

    ssh = {}  # ssh = {"gpu1":SSHController}
    for node in remote_nodes:
        ssh[node.name] = SSHController(node)

    processes = []
    p = Pool(len(ssh))
    try:
        for tmp in ssh.keys():
            p.apply_async(do_upload, args=(ssh[tmp], localpath, remotepath))
        p.close()
        p.join()
    except:
        print("Error: unable to start process")
    return processes


def do_download(ssh, remotepath, localpath, name):
    ssh.connect()
    ssh.download(remotepath, localpath+name)
    ssh.close()


def multi_do_download(remotepath, localpath):
    remote_nodes, _ = databean.get_nodes(context.path[1])
    if remote_nodes is None:
        context.verbose("there are not the forwarding to localhost")
        return

    ssh = {}  # ssh = {"gpu1":SSHController}
    for node in remote_nodes:
        ssh[node.name] = SSHController(node)

    processes = []
    p = Pool(len(ssh))
    try:
        for tmp in ssh.keys():
            p.apply_async(do_download, args=(ssh[tmp], remotepath, localpath, tmp))
        p.close()
        p.join()
    except:
        print("Error: unable to start process")
    return processes


if __name__ == "__main__":
    """
    test
    """
    # multi_do_exec_command()
    # multi_do_upload("../../resource/upload", "./")
    multi_do_download("./folder_from_server", "../../resource/download/"+"folder_from_server/")
    # test gpu1
    # remote_nodes, server_node = databean.get_nodes(context.path[0])
    # ssh_client = SSHController(server_node)
    # ssh_client.connect()
    # ssh_client.exec_command("ls")
    # ssh_client.upload("../../resource/upload", "./")
    # ssh_client.download("./folder_from_server", "../../resource/download/"+"folder_from_server_new")
    # ssh_client.close()
