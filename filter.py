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
    # filter traces
    if options.verbose:
        print 'removing instrument response'
    streams.simulate(
            responses=sensorloc.Responses(options.responseDirectory),
            response_units=options.responseUnits,
            pre_filt=options.prefilt,
            taper=not options.no_taper)
    # trim traces after filtering
    try:
        if options.startTime is not None or options.endTime is not None:
            if options.verbose:
                print 'trimming'
            streams.trim(starttime=options.startTime, endtime=options.endTime)
    except Exception,msg:
        print 'Error trimming: "%s"' % msg
    # run whichever filters are chosen
    if options.bandpass:
        if options.verbose:
            print 'running bandpass filter'
        streams.filter('bandpass',
                freqmin=options.bandpass[0],
                freqmax=options.bandpass[1],
                corners=options.bandpass[2])
    if options.lowpass:
        if options.verbose:
            print 'running lowpass filter'
        streams.filter('lowpass',
                freq=options.lowpass[0],
                corners=options.lowpass[1])
    if options.highpass:
        if options.verbose:
            print 'running highpass filter'
        streams.filter('highpass',
                freq=options.highpass[0],
                corners=options.highpass[1])
    # write output
    if not os.path.isdir(options.outputDirectory):
        os.makedirs(options.outputDirectory)
    try:
        if options.verbose:
            print 'writing output to ' + options.outputDirectory
        suffix = ''
        if options.simulate:
            suffix += '.d'
        if options.bandpass or options.lowpass or options.highpass:
            suffix += '.f'
        streams.write(options.outputDirectory, encoding='FLOAT64', suffix=suffix)
    except Exception,msg:
        print 'Error writing output: "%s"' % msg
    # generate plot - test
    if options.plot:
        streams.plot()




# when script is run instead of imported
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter Mini-SEED files')

    parser.add_argument('miniseeds', metavar='SEED', nargs='+',
            help='Mini-SEED files to process')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-p', '--plot', default=False, action='store_true',
            help='Save a plot (PNG format) of the filtered data.')
    parser.add_argument('-bp', dest='bandpass', nargs=3, metavar=('MIN','MAX','NPOLES'),
            help='Bandpass filter (after) removing instrument response',type=float)
    parser.add_argument('-lp', dest='lowpass', nargs=2, metavar=('FREQ','NPOLES'),
            help='Lowpass filter (after) removing instrument response',type=float)
    parser.add_argument('-hp', dest='highpass', nargs=2, metavar=('FREQ','NPOLES'),
            help='Highpass filter (after) removing instrument response',type=float)
    parser.add_argument('--outputDirectory', default='.',
            help='Output directory for processed Mini-SEED files')
    parser.add_argument('--simulate', default=False, action='store_true',
            help='Remove instrument response using RESP files')
    parser.add_argument('--prefilt', nargs=4, default=None, type=float, 
            metavar=('corner1','corner2','corner3','corner4'),
            help='Bandpass filter to apply before simulate, 4 corner frequencies')
    parser.add_argument('--responseDirectory', default='.',
            help='Directory with response files for traces in input Mini-SEEDs')
    parser.add_argument('--responseUnits', default='ACC',
            help='Units for simulate call')
    parser.add_argument('--no-taper', default=True, action='store_false')
    parser.add_argument('-s', '--start', dest='startTime', metavar='STARTTIME',
            help='Trim time series (YYYY,DDD,HH:MM:SS) after simulate and filter',
            type=UTCDateTime)
    parser.add_argument('-e', '--end', dest='endTime', metavar='ENDTIME',
            help='Trim time series (YYYY,DDD,HH:MM:SS) after simulate and filter',
            type=UTCDateTime)

    main(parser.parse_args(),parser)
