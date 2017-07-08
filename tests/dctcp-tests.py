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


# interface connecting the switch to the "server" node
switch_server_iface = 's1-eth1'

# save test results here
results_dir = './results'


class DCTCPTopo(Topo):
    "Single switch topology for testing DCTCP queue length"

    def build(self, n=3):

        link_opts = {
            'bw': 1000,
            'max_queue_size': 1000,
            'enable_ecn': True
        }

        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('host%s' % h)
            self.addLink(host, switch, **link_opts)


def dctcp_queue_test(results_file):
    "Run DCTCP queue size tests"

    topo = DCTCPTopo()
    net = Mininet(topo=topo, link=TCLink)

    net.start()

    switch = net.getNodeByName('s1')

    queue_monitor = Process(target=monitor_qlen, args=(
        switch_server_iface, 0.01, '%s/%s' % (results_dir, results_file)))
    queue_monitor.start()

    server = net.get("host0")
    client1, client2 = net.get("host1", "host2")

    server_ip = server.IP()
    test_time = 5

    print("Starting iperf server")
    server.sendCmd('iperf -s')
    print("Starting iperf client 1")
    client1.sendCmd('iperf -c %s -t %d -i 1 -Z reno > %s/iperf_client1.txt'
                    % (server_ip, test_time, results_dir))
    print("Starting iperf client 2")
    client2.sendCmd('iperf -c %s -t %d -i 1 -Z reno > %s/iperf_client2.txt'
                    % (server_ip, test_time, results_dir))

    print("Waiting for hosts to finish...")

    client1.waitOutput()
    client2.waitOutput()
    server.sendInt()
    server.waitOutput()

    queue_monitor.terminate()

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    # reset to default state
    tcp_utils.disable_dctcp()

    dctcp_queue_test("reno_queue.csv")
    tcp_utils.enable_dctcp()
    dctcp_queue_test("dctcp_queue.csv")
    tcp_utils.disable_dctcp()
