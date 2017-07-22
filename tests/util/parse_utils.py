import sys
import os
import re


def parse_iperf(senders, interval_time, cong_ctl, results_dir, results_file):

    """ parse iperf output and save throughput results to file.

        this is meant to fit a specific use case and is kind of hacked
        together... """

    data = re.compile('Mbits')
    delim = re.compile('(\s|-)+')

    start_time = 0

    for s in senders:

        lines = open('%s/%s-converg.txt'
                     % (results_dir, s)).read().split('\n')

        # last line gives an average, which we aren't interested in
        lines = lines[:-2]

        for line in lines:
            if data.search(line):
                line = delim.split(line.strip())
                time = start_time + float(line[6])
                thru = line[14]
                with open('%s/%s' % (results_dir, results_file), 'a') as file:
                    file.write("%s,%s,%s,%s\n" % (s, cong_ctl, time, thru))

        start_time += interval_time
