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
        extent = streams.getTimeExtent(True)
    except Exception,msg:
        print 'Error reading Mini-SEED: "%s"' % msg
        parser.print_help()
        sys.exit(1)
    # when verbose, list loaded streams
    if options.verbose:
        print streams
    # output range
    if options.range:
        print 'Start: %s\nEnd: %s\n' % (extent['start'], extent['end'])
        sys.exit(0)
    # filter traces
    streams.simulate(
            responses=sensorloc.Responses(options.responseDirectory),
            response_units=options.responseUnits,
            pre_filt=options.prefilt,
            taper=options.taper)
    # trim traces after filtering
    try:
        if options.startTime is not None or options.endTime is not None:
            streams.trim(starttime=options.startTime, endtime=options.endTime)
    except Exception,msg:
        print 'Error trimming: "%s"' % msg
    # write output
    if not os.path.isdir(options.outputDirectory):
        os.makedirs(options.outputDirectory)
    try:
        streams.write(options.outputDirectory, encoding='FLOAT64')
    except Exception,msg:
        print 'Error writing output: "%s"' % msg
    # generate plot
    if options.plot:
        streams.plot()




#sort of awkward, but using the syntax below makes it explicit that the "if" code block is the entry
#point to the program.  The reason for then passing the arguments to a main() function
#is that variables declared in the block below are **GLOBAL**, and can hence cause confusion 
#later on when re-using those variable names in another function.  Doing all of the main work
#in the main() function ensures that main() variables stay in their expected scope.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter Mini-SEED files')

    parser.add_argument('miniseeds', metavar='SEED', nargs='+',
            help='Mini-SEED files to process')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-s', '--start', dest='startTime', metavar='STARTTIME',
            help='Select left edge of time series (YYYY-MM-DDTHH:MM:SS.sss)', type=UTCDateTime)
    parser.add_argument('-e', '--end', dest='endTime', metavar='ENDTIME',
            help='Select right edge of time series (YYYY-MM-DDTHH:MM:SS.sss)', type=UTCDateTime)
    parser.add_argument('-p', '--plot', default=False, action='store_true',
            help='Save a plot (PNG format) of the chopped data.')
    parser.add_argument('-r', '--range', default=False, action='store_true',
            help='Get the overlapping time range of all traces in Mini-SEED files.')
    parser.add_argument('--outputDirectory', default='.',
            help='Output directory for processed Mini-SEED files')
    parser.add_argument('--responseDirectory', default='.',
            help='Directory with response files for traces in input Mini-SEEDs')
    parser.add_argument('--responseUnits', default='ACC',
            help='Units for simulate call')
    parser.add_argument('--taper', default=False, action='store_true')
    parser.add_argument('--prefilt', default=None, nargs=4, type=float,
            help='Bandpass filter to apply before simulate, 4 corner frequencies')
    main(parser.parse_args(),parser)
