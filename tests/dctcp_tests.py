#!/usr/bin/python

import sys
import os

from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from dctcp_topo import DCTCPTopo
from startopo import StarTopo

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

# configuring RED is kind of complicated, but we can set our own value for k
# by setting min = k * avpacket and max = min + 1 with probability 1
#
# this configuration is from <link 2013 DCTCP project>
red_params = {
    'limit': 1000000,
    'min': 30000,
    'max': 30001,
    'avpkt': 1500,
    'burst': 20,
    'prob': 1
}


def dctcp_queue_test(use_dctcp, results_file, n_hosts=3):
    "Run DCTCP queue size tests"

    if use_dctcp is True:
        tcp_utils.enable_dctcp()
    else:
        tcp_utils.disable_dctcp()

    topo = DCTCPTopo(
        bw=100, max_q=300, n=n_hosts, delay='1ms', use_dctcp=use_dctcp)

    net = Mininet(
        topo=topo, host=CPULimitedHost, link=TCLink, autoPinCpus=True)

    net.start()

    dumpNodeConnections(net.hosts)

    switch = net.getNodeByName('s1')

    server = net.getNodeByName('h1')
    client1, client2 = net.getNodeByName("h2", "h3")

    server_ip = server.IP()
    test_time = 10

    print("Starting iperf server...")
    server.popen("iperf -s -w 16m")

    h1 = net.getNodeByName('h1')
    for i in range(1, n_hosts):
        print "Starting iperf client..."
        client = net.getNodeByName('h%d' % (i+1))
        client.popen("iperf -c %s -t 100" % server_ip)

    print("Waiting for TCP flows to reach steady state")
    sleep(5)

    print("Starting queueing test... run time: %d seconds" % test_time)
    queue_monitor = Process(target=monitor_qlen, args=(
        switch_server_iface, 0.1, '%s/%s' % (results_dir, results_file)))
    queue_monitor.start()
    sleep(test_time)
    queue_monitor.terminate()

    # need to stop hosts...

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    dctcp_queue_test(use_dctcp=False, results_file="reno_queue.csv")
    dctcp_queue_test(use_dctcp=True, results_file="dctcp_queue.csv")

    print("Done!")
