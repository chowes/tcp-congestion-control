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

from time import sleep, time
from subprocess import Popen, PIPE
from multiprocessing import Process

# queue length monitoring tools from:
# https://github.com/mininet/mininet-util
from util.monitor_utils import monitor_qlen, monitor_throughput
from util import tcp_utils


# interface connecting the switch to the "server" node
SWITCH_SERVER_IFACE = 's1-eth1'

# save test results here
RESULTS_DIR = '/home/ubuntu/tcp-congestion-control/tests/results'

# time to wait for flows to stabilize
TCP_STABILIZATION_TIME = 10


def dctcp_queue_test(use_dctcp, testname, queue_file, throughput_file,
                     k=20, bw=100, num_flows=2, time=10):

    "Run DCTCP queue size and throughput tests"

    num_hosts = num_flows + 1

    if use_dctcp is True:
        tcp_utils.enable_dctcp()
    else:
        tcp_utils.disable_dctcp()

    topo = DCTCPTopo(
        bw=bw, max_q=400, k=20, n=num_hosts, delay='.5ms', use_dctcp=use_dctcp)

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
    receiver.popen("iperf -s", shell=True)

    print("Starting iperf clients...")
    for s in senders:
        print("%s sending to %s" % (s.IP(), receiver.IP()))
        s.popen("iperf -c %s -t %d -i 0.1" %
                (receiver.IP(), (time + 30)), shell=True)

    print("Waiting for TCP flows to reach steady state")
    sleep(TCP_STABILIZATION_TIME)

    print("Starting tests... run time: %d seconds" % time)
    queue_monitor = Process(target=monitor_qlen, args=(
        SWITCH_SERVER_IFACE, testname, '%s/%s' %
        (RESULTS_DIR, queue_file), time, 0.1))

    throughput_monitor = Process(target=monitor_throughput, args=(
        SWITCH_SERVER_IFACE, testname, '%s/%s' %
        (RESULTS_DIR, throughput_file), time))

    throughput_monitor.start()
    queue_monitor.start()

    queue_monitor.join()
    throughput_monitor.join()

    net.stop()


def dctcp_convergence_test(use_dctcp, results_file, bw=100, num_flows=5,
                           interval_time=30):
    "Run DCTCP convergence test"

    num_hosts = num_flows + 1

    if use_dctcp is True:
        tcp_utils.enable_dctcp()
    else:
        tcp_utils.disable_dctcp()

    topo = DCTCPTopo(
        bw=bw, max_q=200, n=num_hosts, delay='.5ms', use_dctcp=use_dctcp)

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
    receiver.popen("iperf -s -w 32m -i 1 > test.txt &", shell=True)

    print("Starting iperf clients...")
    i = num_flows
    for s in senders:
        run_time = (i * 2 - 1) * interval_time
        print("%s sending to %s - run time: %d" %
              (s.name, receiver.name, run_time))
        s.popen("iperf -c %s -w 32m -t %d -i 0.1 > %s/%s-%s &" %
                (receiver.IP(), run_time, RESULTS_DIR, s.name, results_file),
                shell=True)
        sleep(interval_time)
        i -= 1

    wait_time = (num_flows - 1) * interval_time
    print("waiting %d seconds", wait_time)
    sleep(wait_time)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    # results files for throughput and queue length tests
    queue_file = "queue.csv"
    throughput_file = "thru.csv"

    # results files for testing for ideal k value
    queue_k_file = "dctcp_k_queue.csv"
    throughput_k_file = "dctcp_k_thru.csv"

    # delete old results files if they exist
    try:
        os.remove('%s/%s' % (RESULTS_DIR, queue_file))
    except OSError:
        pass

    try:
        os.remove('%s/%s' % (RESULTS_DIR, throughput_file))
    except OSError:
        pass

    try:
        os.remove('%s/%s' % (RESULTS_DIR, queue_k_file))
    except OSError:
        pass

    try:
        os.remove('%s/%s' % (RESULTS_DIR, throughput_k_file))
    except OSError:
        pass

    # setup csv headers
    with open('%s/%s' % (RESULTS_DIR, queue_file), 'w') as new_file:
        new_file.write("%s,%s,%s,%s\n"
                       % ('cong_ctl', 'iface', 'time', 'q_len'))

    with open('%s/%s' % (RESULTS_DIR, throughput_file), 'w') as new_file:
        new_file.write("%s,%s,%s\n"
                       % ('cong_ctl', 'iface', 'thru'))

    with open('%s/%s' % (RESULTS_DIR, queue_k_file), 'w') as new_file:
        new_file.write("%s,%s,%s,%s\n"
                       % ('k', 'iface', 'time', 'q_len'))

    with open('%s/%s' % (RESULTS_DIR, throughput_k_file), 'w') as new_file:
        new_file.write("%s,%s,%s\n"
                       % ('k', 'iface', 'thru'))

    # test queue size with two flows over a shared bottleneck
    print "queue test: tcp reno - 2 flows"
    dctcp_queue_test(
        use_dctcp=False,
        testname="reno_2",
        queue_file=queue_file,
        throughput_file=throughput_file,
        bw=100,
        num_flows=2,
        time=60)

    print "queue test: dctcp - 2 flows"
    dctcp_queue_test(
        use_dctcp=True,
        testname="dctcp_2",
        queue_file=queue_file,
        throughput_file=throughput_file,
        bw=100,
        num_flows=2,
        time=60)

# test queue size with twenty flows over a shared bottleneck
    print "queue test: tcp reno - 20 flows"
    dctcp_queue_test(
        use_dctcp=False,
        testname="reno_20",
        queue_file=queue_file,
        throughput_file=throughput_file,
        bw=100,
        num_flows=20,
        time=60)

    print "queue test: dctcp - 20 flows"
    dctcp_queue_test(
        use_dctcp=True,
        testname="dctcp_20",
        queue_file=queue_file,
        throughput_file=throughput_file,
        bw=100,
        num_flows=20,
        time=60)

    # dctcp_convergence_test(
    #     use_dctcp=True,
    #     results_file="convergence-test.txt",
    #     bw=1000,
    #     num_flows=5,
    #     interval_time=5)

    for i in range(100):
        dctcp_queue_test(
             use_dctcp=True,
             testname=i+1,
             queue_file=queue_k_file,
             throughput_file=throughput_k_file,
             bw=100,
             k=i+1,
             num_flows=2,
             time=60)

    tcp_utils.reset_tcp()

    print("Done!")
