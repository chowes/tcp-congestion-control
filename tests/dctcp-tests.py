#!/usr/bin/python

import sys
import os

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import Link, TCLink
from mininet.node import CPULimitedHost
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from time import sleep, time
from subprocess import Popen, PIPE
from multiprocessing import Process

from util.monitor import monitor_qlen
from util import tcp_utils


class DCTCPTopo(Topo):
    "Single switch topology for testing DCTCP queue length"

    def build(self, n = 3):
        
        link_opts = {
            'bw': 1000, 
            'max_queue_size':1000, 
            'enable_ecn':True
        }

        switch = self.addSwitch('s1')
        
        for h in range(n):
            host = self.addHost('host%s' % h)
            self.addLink(host, switch, **link_opts)


def dctcp_queue_test():
    "Run DCTCP queue size tests"
    topo = DCTCPTopo()
    net = Mininet(topo = topo, link = TCLink)
    net.start()
    print "Dump host connections..."
    dumpNodeConnections(net.hosts)
    print "Test network connectivity..."
    net.pingAll()
    print "Test bandwidth between clients and server..."
    server = net.get("host0")
    client1, client2 = net.get("host1", "host2")
    print "Client 1 - Server"
    net.iperf((client1, server))
    print "Client 2 - Server"
    net.iperf((client2, server))
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    # reset to default state
    tcp_utils.disable_dctcp()

    tcp_utils.enable_dctcp()
    dctcp_queue_test()
    tcp_utils.disable_dctcp()


