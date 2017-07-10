#!/usr/bin/python

from mininet.topo import Topo
from mininet.link import TCLink, TCIntf, Link

# RED configuration from
# https://reproducingnetworkresearch.wordpress.com/2013/03/13/cs244-13-dctcp/
red_config = {
    'limit': 1000000,
    'min': 20000,
    'max': 25000,
    'avpkt': 1000,
    'burst': 20,
    'prob': 1
}


class DCTCPTopo(Topo):
    "Single switch topology for testing DCTCP queue length"

    def build(self, n=3, bw=100, max_q=None, use_dctcp=False, cpu=None):

        # set host options
        host_opts = {
            'cpu': cpu
        }

        # set link options
        host_link_opts = {
            'bw': bw,
            'max_queue_size': max_q,
            'enable_ecn': 1 if use_dctcp is True else 0
        }

        switch_link_opts = {
            'bw': bw,
            'max_queue_size': max_q,
            'enable_ecn': 1 if use_dctcp is True else 0,
            'enable_red': 1 if use_dctcp is True else 0,
            'red_params': red_config
        }

        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('host%s' % h)
            self.addLink(host, switch, cls=Link, cls1=TCIntf, cls2=TCIntf,
                         params1=host_link_opts, params2=switch_link_opts)
