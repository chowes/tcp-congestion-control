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
SWITCH_SERVER_IFACE = 's1-eth1'

# save test results here
RESULTS_DIR = './results'

# time to wait for flows to stabilize
TCP_STABILIZATION_TIME = 10

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


def dctcp_queue_test(use_dctcp, results_file, num_hosts=3, time=10):
    "Run DCTCP queue size tests"

    if use_dctcp is True:
        tcp_utils.enable_dctcp()
    else:
        tcp_utils.disable_dctcp()

    topo = DCTCPTopo(
        bw=100, max_q=200, n=num_hosts, delay='.5ms', use_dctcp=use_dctcp)

    net = Mininet(
        topo=topo, host=CPULimitedHost, link=TCLink, autoPinCpus=True)

    net.start()

    dumpNodeConnections(net.hosts)

    switch = net.getNodeByName('s1')
    receiver = net.getNodeByName('h1')
    senders = []
    for s in range(1, num_hosts):
        senders.append(net.getNodeByName('h%s' % (s + 1)))

    print("Starting iperf server...")
    receiver.popen("iperf -s -w 64m")

    print("Starting iperf clients...")
    for s in senders:
        print("%s sending to %s" % (s.IP(), receiver.IP()))
        s.popen("iperf -c %s -t %d" % (receiver.IP(), (time + 30)))

    print("Waiting for TCP flows to reach steady state")
    sleep(TCP_STABILIZATION_TIME)

    print("Starting queueing test... run time: %d seconds" % time)
    queue_monitor = Process(target=monitor_qlen, args=(
        SWITCH_SERVER_IFACE, 0.01, '%s/%s' % (RESULTS_DIR, results_file)))
    queue_monitor.start()
    sleep(time)
    queue_monitor.terminate()

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    dctcp_queue_test(use_dctcp=False, num_hosts=8,
                     results_file="reno_queue.csv")

    dctcp_queue_test(use_dctcp=True, num_hosts=8,
                     results_file="dctcp_queue.csv")

    tcp_utils.reset_tcp()

    print("Done!")
