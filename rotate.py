#!/usr/bin/env python

#stdlib imports
import argparse
import sys
import time
import os, os.path

import sensorloc

#third party imports
from obspy import UTCDateTime

def main(options, parser):
    streams = sensorloc.Streams()
    # parse Mini-SEED files
    try:
        for f in options.miniseeds:
            streams.addFile(f)
    except Exception,msg:
        print 'Error reading Mini-SEED: "%s"' % msg
        parser.print_help()
        sys.exit(1)
    # when verbose, list loaded streams
    if options.verbose:
        print streams
    rotated = streams.rotate(options.angle)
    # write output
    if not os.path.isdir(options.outputDirectory):
        os.makedirs(options.outputDirectory)
    try:
        if options.verbose:
            print 'writing output to ' + options.outputDirectory
        suffix = '.r'
        rotated.write(options.outputDirectory, encoding='FLOAT64', suffix=suffix)
    except Exception,msg:
        print 'Error writing output: "%s"' % msg
    if options.plot:
        rotated.plot()


# when script is run instead of imported
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rotate two components clockwise by a specified angle.')

    parser.add_argument('miniseeds', metavar='SEED', nargs=2,
            help='Mini-SEED files to process')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-a', '--angle', dest='angle', type=float)
    parser.add_argument('-d', '--outputDirectory')
    parser.add_argument('-p', '--plot', default=False, action='store_true',
            help='Save a plot (PNG format) of the chopped data.')

    main(parser.parse_args(),parser)
