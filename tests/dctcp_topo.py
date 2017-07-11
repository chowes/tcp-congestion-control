#!/usr/bin/python

from mininet.topo import Topo
from mininet.link import TCLink, TCIntf, Link


# red calibration from:
# <add link to 2013 DCTCP stanford project>
#
# getting DCTCP marking using RED parameters is not intuitive...
# we take min = (K x avgpkt) and max = (min + 1)
# ECN marking should now happen at queue sizes of K
red_params = {
    'limit': 1000000,
    'min': 30000,
    'max': 30001,
    'avpkt': 1500,
    'burst': 20,
    'prob': 1
}


class DCTCPTopo(Topo):
    "Single switch topology for testing DCTCP queue length"

    def __init__(self, n=3, bw=100, max_q=None, delay=None, cpu=None,
                 use_dctcp=False):

        super(DCTCPTopo, self).__init__()

        # set host options
        host_opts = {
            'cpu': cpu
        }

        # set sender link options
        send_link_opts = {
            'bw': bw,
            'delay': delay,
            'max_queue_size': max_q
        }

        recv_link_opts = {
            'bw': bw,
            'delay': 0,
            'max_queue_size': max_q
        }

        switch_link_opts = {
            'bw': bw,
            'delay': 0,
            'max_queue_size': max_q,
            'enable_red': 1 if use_dctcp is True else 0,
            'enable_ecn': 1 if use_dctcp is True else 0,
            'red_params': red_params if use_dctcp is True else None
        }

        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('h%s' % (h + 1))

        # set h1 as our receiver and add a connection to the switch this is our
        # "bottleneck" where we will expect queues to build up
        self.addLink('h1', 's1', cls=Link, cls1=TCIntf, cls2=TCIntf,
                     params1=recv_link_opts, params2=switch_link_opts)

        # add the two senders, traffic should pass through the shared
        # bottleneck in order to reach the receiver
        for h in range(1, n):
            self.addLink(
                'h%s' % (h + 1), 's1', **send_link_opts)
