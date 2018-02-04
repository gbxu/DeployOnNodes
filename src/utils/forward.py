#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################################

"""
Created on 2018-02-02
@author: gb.xu
@mail: gb.xu@outlook.com

this script file is showing how to do local port forwarding over paramiko.
This script connects to the requested SSH server and sets up local port
forwarding (the openssh -L option) from a local port through a tunneled
connection to a destination reachable from the SSH server machine.
"""
from multiprocessing import Pool
import socketserver as SocketServer
import select
import sys
import paramiko
import socket
from contextlib import closing
import json
from src.utils.databean import ForwardOptions
from src.utils import databean
from src.utils import context


class ForwardServer(SocketServer.ThreadingTCPServer):
    # ThreadingTCPServer
    daemon_threads = True
    allow_reuse_address = True


class Handler(SocketServer.BaseRequestHandler):
    # socket server
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   self.request.getpeername())
        except Exception as e:
            context.verbose('Incoming request to %s:%d failed: %s' % (self.chain_host,
                                                                      self.chain_port,
                                                                      repr(e)))
            return
        if chan is None:
            context.verbose('Incoming request to %s:%d was rejected by the SSH server.' %
                            (self.chain_host, self.chain_port))
            return

        context.verbose('Connected!  Tunnel open %r -> %r -> %r' % (self.request.getpeername(),
                                                                    chan.getpeername(),
                                                                    (self.chain_host, self.chain_port)))
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        context.verbose('Tunnel closed from %r' % (peername,))


def forward_tunnel(local_port, remote_host, remote_port, transport):
    # this is a little convoluted, but lets me configure things for the Handler
    # object.  (SocketServer doesn't give Handlers any way to access the outer
    # server normally.)
    class SubHander(Handler):
        chain_host = remote_host
        chain_port = remote_port
        ssh_transport = transport

    ForwardServer(('', local_port), SubHander).serve_forever()


def forward(options, free_port):
    """
    :param options:
        options concludes user,key,local,server,remote
        user: username on server host(bastion host)
        key: in .ssh/id_rsd， to verify the access of user
        server: server host and port
        remote: the destination host and port(22 in most time)
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    context.verbose('Connecting to ssh host %s:%d ...' % (options.server[0],
                                                          options.server[1]))
    try:
        client.connect(hostname=options.server[0], port=options.server[1],
                       username=options.user, key_filename=options.key)
    except Exception as e:
        print('*** Failed to connect to %s:%d: %r' % (options.server[0], options.server[1], e))
        sys.exit(1)
    context.verbose('Now forwarding port %d to %s:%d ...' % (free_port,
                                                             options.remote[0],
                                                             options.remote[1]))
    try:
        forward_tunnel(free_port, options.remote[0], options.remote[1],
                       client.get_transport())
    except KeyboardInterrupt:
        print('C-c: Port forwarding stopped.')
        sys.exit(0)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def multi_forward():
    """
    forwart local port to lan server machines, through the bastion host.
    :return:
    """
    remote_nodes, server_node = databean.get_nodes(context.path[0])
    forward_local_ports = []
    forward_pool = Pool(len(remote_nodes))
    try:
        for remote_node in remote_nodes:
            free_port = find_free_port()
            options = ForwardOptions(server_node.user, server_node.key,
                                     server_node.host, server_node.port,
                                     remote_node.host, remote_node.port)
            forward_pool.apply_async(forward, args=(options, free_port))
            forward_local_ports.append({"name": remote_node.name,
                                        "host": "localhost",
                                        "port": free_port
                                        })
        forward_pool.close()
    except:
        print("Error: unable to start process")
    with open(context.path[1], "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(forward_local_ports))
    forward_pool.join()  # keep


if __name__ == '__main__':
    """
    test
    """
    test = False
    if test:
        remote_nodes, server_node = databean.get_nodes()
        remote_node = remote_nodes[0]
        options = ForwardOptions(server_node.user, server_node.key,
                                 server_node.host, server_node.port,
                                 remote_node.host, remote_node.port)
        forward(options, 50032)
    else:
        multi_forward()