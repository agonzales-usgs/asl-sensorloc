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
    
    # parse Mini-SEED files
    streams = sensorloc.Streams()
    try:
        for f in options.miniseeds:
            streams.addFile(f)
   	for i in range(len(streams.data)):
	    print "stream[%d] = %s" % (i, streams.data[i])
    except Exception,msg:
        print 'Error reading Mini-SEED: "%s"' % msg
        parser.print_help()
        sys.exit(1)
    
    # parse reference Mini-SEED files
    referenceStream = sensorloc.Streams()
    try:
        for f in options.reference:
            referenceStream.addFile(f)
   	for i in range(len(referenceStream.data)):
	    print "referenceStream[%d] = %s" % (i, referenceStream.data[i])
    except Exception,msg:
        print 'Error reading reference Mini-SEED: "%s"' % msg
        parser.print_help()
        sys.exit(1)
    
    # when verbose, list loaded streams
    if options.verbose:
        print "reference stream, azimuth='" + str(options.referenceAzimuth) + "':"
        print referenceStream
        print "unknown stream"
        print streams
    
    # compute coherence between reference and test sensors 
    try:
        coherenceInfo = streams.coherence(referenceStream=referenceStream,
                            referenceAzimuth=options.referenceAzimuth,
                            NFFT=options.nfft,
                            noverlap=options.noverlap,
                            Fs=options.fs)
        print "azimuth =", str(coherenceInfo['azimuth'])
        print "scale1 =", str(coherenceInfo['scale1'])
        print "residual1 =", str(coherenceInfo['residual1'])
        print "scale2 =", str(coherenceInfo['scale2'])
        print "residual2 =", str(coherenceInfo['residual2'])
        
        # optionally rotate, output, plot
        if options.rotate:
            rotated = coherenceInfo.rotated
            if options.outputDirectory:
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
    except Exception,msg:
        print 'Error determining coherence: "%s"' % msg


# when script is run instead of imported
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Determine angle between a reference station and a unknown station.')

    parser.add_argument('miniseeds', metavar='SEED', nargs=2,
            help='Mini-SEED files to process (north/east)')
    
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    
    parser.add_argument('-r', '--reference', metavar='SEED', nargs=2,
            help='two reference Mini-SEED files (north/east)')
    
    parser.add_argument('-ra', '--referenceAzimuth', metavar='ANGLE', type=float,
            help='azimuth of reference north component')
    
    parser.add_argument('-nfft', default=256, type=int,
            help='Number of points used in FFT, must be even.')
    
    parser.add_argument('-noverlap', default=None, type=int,
            help='Number of overlapping data points used in FFT, defaults to NFFT/4')
    
    parser.add_argument('-fs', default=None, type=int,
            help='Number of samples per second, defaults to reference miniseed sampling rate')
    
    parser.add_argument('--rotate', action='store_true',
            help='After determining and reporting angle, rotate data to align with reference')
    
    parser.add_argument('-d', '--outputDirectory', default=None)
    
    parser.add_argument('-p', '--plot', default=False, action='store_true',
            help='Save a plot (PNG format) of the chopped data.')
    
    main(parser.parse_args(),parser)
