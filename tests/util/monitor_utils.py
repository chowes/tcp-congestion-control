#!/bin/bash

from time import sleep, time
from subprocess import *
import re


def monitor_qlen(iface, testname, filename, run_time=10, interval=0.1):

    """ Monitor the queue length of the given interface and appends results
        to a .csv file.

        Modified from Mininet util function 'monitor_qlen':
        https://github.com/mininet/mininet-util/blob/master/monitor.py """

    pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
    cmd = "tc -s qdisc show dev %s" % (iface)
    ret = []
    start_time = time()
    with open(filename, 'a') as outfile:
        while time() < (start_time + run_time):
            p = Popen(cmd, shell=True, stdout=PIPE)
            output = p.stdout.read()
            # Not quite right, but will do for now
            matches = pat_queued.findall(output)
            if matches and len(matches) > 1:
                ret.append(matches[1])
                t = "%f" % (time() - start_time)
                outfile.write("%s,%s,%s,%s\n"
                              % (testname, iface, t, matches[1]))
            sleep(interval)

    return


def monitor_throughput(iface, testname, filename, run_time=10):

    """ Measures the throughput of the specified interace over a given
        run time and appends results to a .csv file """

    iface_pattern = re.compile(iface)
    spaces = re.compile('\s+')

    lines = open('/proc/net/dev').read().split('\n')

    for line in lines:
        line = spaces.split(line.strip())
        interface = line[0]
        if iface_pattern.match(interface) and len(line) > 9:
            start_bytes = int(line[9])

    sleep(run_time)

    lines = open('/proc/net/dev').read().split('\n')

    for line in lines:
        line = spaces.split(line.strip())
        interface = line[0]
        if iface_pattern.match(interface) and len(line) > 9:
            end_bytes = int(line[9])

    # calculate throughout and convert to Mbits/second
    throughput = (8 * (end_bytes - start_bytes) / run_time) / 1e6

    with open(filename, 'a') as outfile:
        outfile.write("%s,%s,%s\n" % (testname, iface, throughput))

    return
