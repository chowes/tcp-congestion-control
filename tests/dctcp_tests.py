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
switch_server_iface = 's0-eth1'

# save test results here
results_dir = './results'


# Enable DCTCP and ECN in the Linux Kernel
def SetDCTCPState():
    Popen("sysctl -w net.ipv4.tcp_dctcp_enable=1", shell=True).wait()
    Popen("sysctl -w net.ipv4.tcp_ecn=1", shell=True).wait()


# Disable DCTCP and ECN in the Linux Kernel
def ResetDCTCPState():
    Popen("sysctl -w net.ipv4.tcp_dctcp_enable=0", shell=True).wait()
    Popen("sysctl -w net.ipv4.tcp_ecn=0", shell=True).wait()


def dctcp_queue_test(use_dctcp, results_file):
    "Run DCTCP queue size tests"

    os.system("sudo sysctl -w net.ipv4.tcp_congestion_control=reno")

    if use_dctcp is True:
        SetDCTCPState()
    else:
        ResetDCTCPState()

    red_params = {
        'limit': 1000000,
        'min': 30000,
        'max': 30001,
        'avpkt': 1500,
        'burst': 20,
        'prob': 1
    }

    # topo = DCTCPTopo(use_dctcp=use_dctcp, max_q=1000, delay='1ms')
    topo = StarTopo(
        n=3,
        bw_host=100,
        delay='1ms',
        bw_net=100,
        maxq=400,
        enable_dctcp=use_dctcp,
        enable_red=use_dctcp,
        red_params=red_params,
        show_mininet_commands=0)

    net = Mininet(
        topo=topo, host=CPULimitedHost, link=TCLink, autoPinCpus=True)

    net.start()

    dumpNodeConnections(net.hosts)

    switch = net.getNodeByName('s0')

    server = net.getNodeByName('h0')
    client1, client2 = net.getNodeByName("h1", "h2")

    server_ip = server.IP()
    test_time = 5

    h0 = net.getNodeByName('h0')
    print "Starting iperf server..."
    server = h0.popen("iperf -s -w 16m")

    h0 = net.getNodeByName('h0')
    for i in range(2):
        print "Starting iperf client..."
        hn = net.getNodeByName('h%d' % (i+1))
        client = hn.popen("iperf -c " + h0.IP() + " -t 100")

    print("Waiting for TCP flows to stabilize")
    sleep(3)

    print("Starting test...")
    queue_monitor = Process(target=monitor_qlen, args=(
        switch_server_iface, 0.5, '%s/%s' % (results_dir, results_file)))
    queue_monitor.start()
    sleep(test_time)
    queue_monitor.terminate()

    print("Test complete, waiting for hosts to finish...")

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    dctcp_queue_test(use_dctcp=False, results_file="reno_queue.csv")
    dctcp_queue_test(use_dctcp=True, results_file="dctcp_queue.csv")

    print("Done!")
