import sys
import os
import re


def parse_iperf(senders, interval_time, results_file):

    """ parse iperf output and save throughput results to file.

        this is meant to fit a specific use case and is kind of hacked
        together... """

    data = re.compile('Mbits')
    delim = re.compile('(\s|-)+')

    # delete old results file if it exists
    try:
        os.remove('%s/%s' % (RESULTS_DIR, results_file))
    except OSError:
        pass

    # setup csv header
    with open('%s/%s' % (RESULTS_DIR, results_file), 'w') as file:
        file.write("%s,%s,%s\n" % ('sender', 'time', 'thru'))

    start_time = 0

    for s in senders:

        lines = open('%s/%s-converg.txt'
                     % (RESULTS_DIR, s)).read().split('\n')

        # last line gives an average, which we aren't interested in
        lines = lines[:-2]

        for line in lines:
            if data.search(line):
                line = delim.split(line.strip())
                time = start_time + float(line[6])
                thru = line[14]
                with open('%s/%s' % (RESULTS_DIR, results_file), 'a') as file:
                    file.write("%s,%s,%s\n" % (s, time, throughput))
            else:
                print line

        start_time += interval_time
