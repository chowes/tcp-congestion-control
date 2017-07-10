#!/usr/bin/python

import sys
import os

from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from dctcp_topo import DCTCPTopo

from time import sleep, time
from subprocess import Popen, PIPE
from multiprocessing import Process

# queue length monitoring tools from
# https://github.com/mininet/mininet-util
from util.monitor import monitor_qlen
from util import tcp_utils


# interface connecting the switch to the "server" node
switch_server_iface = 's1-eth1'

# save test results here
results_dir = './results'


def dctcp_queue_test(use_dctcp, results_file):
    "Run DCTCP queue size tests"

    tcp_utils.disable_dctcp()
    if use_dctcp is True:
        tcp_utils.enable_dctcp()
    else:
        tcp_utils.disable_dctcp()

    topo = DCTCPTopo(use_dctcp=use_dctcp, max_q=466)
    net = Mininet(
        topo=topo, host=CPULimitedHost, link=TCLink, autoPinCpus=True)

    net.start()

    switch = net.getNodeByName('s1')

    queue_monitor = Process(target=monitor_qlen, args=(
        switch_server_iface, 0.01, '%s/%s' % (results_dir, results_file)))
    queue_monitor.start()

    server = net.get("host0")
    client1, client2 = net.get("host1", "host2")

    server_ip = server.IP()
    test_time = 12

    print("Starting iperf server")
    server.sendCmd('iperf -s')
    print("Starting iperf client 1")
    client1.sendCmd('iperf -c %s -t %d -i 1 > %s/iperf_client1.txt'
                    % (server_ip, test_time, results_dir))
    print("Starting iperf client 2")
    client2.sendCmd('iperf -c %s -t %d -i 1 > %s/iperf_client2.txt'
                    % (server_ip, test_time, results_dir))

    print("Waiting for hosts to finish...")

    client1.waitOutput()
    client2.waitOutput()
    server.sendInt()
    server.waitOutput()

    print server.cmd("sysctl -a | grep dctcp")

    queue_monitor.terminate()

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    dctcp_queue_test(use_dctcp=False, results_file="reno_queue.csv")
    dctcp_queue_test(use_dctcp=True, results_file="dctcp_queue.csv")

    tcp_utils.disable_dctcp()