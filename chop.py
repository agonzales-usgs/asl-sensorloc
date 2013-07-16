#!/usr/bin/env python

#stdlib imports
import argparse
import sys
import time
import os.path

#import the object that does all of the work
from sensorloc import streams

#third party imports
from obspy.core import utcdatetime

def main(arguments,parser):
    if arguments.interactiveMode:
        print '\nInteractive mode is not yet implemented.\n'
        parser.print_help()
        sys.exit(1)

    if arguments.miniseed is None:
        print '\nYou must pass in the name of an input Mini-SEED file.\n'
        parser.print_help()
        sys.exit(1)

    #foo
    sl = None
    try:
        sl = streams.Streams()
        for seed in arguments.miniseed:
            sl.addFile(seed)
    except streams.StreamsException,msg:
        print 'There was an error trying to process your file.  "%s"' % msg
        parser.print_help()
        sys.exit(1)
    cliprange = sl.getTimeExtent()

    if arguments.getRange:
        print 'Start: %s\nFinish: %s\n' % (cliprange['start'],cliprange['end'])
        sys.exit(0)
    
    try:
        if arguments.outFolder is None:
            outfolder = os.getcwd()
        else:
            outfolder = arguments.outFolder
        if arguments.startTime is not None:
            clipstart = utcdatetime.UTCDateTime(arguments.startTime,iso8601=True)
        if arguments.endTime is not None:
            clipend = utcdatetime.UTCDateTime(arguments.endTime,iso8601=True)

        sl.trim(starttime=clipstart,endtime=clipend)
        if not os.path.isdir(outfolder):
            os.makedirs(outfolder)
        sl.write(outfolder)

        if arguments.makePlot:
            for seed in arguments.miniseed:
                seedpath,seedfile = os.path.split(seed)
                seedbase,seedext = os.path.splitext(seedfile)
                seedimg = os.path.join(outfolder,seedbase+'.jpg')
                sl.plot(filename=seedimg)
        
    except Exception,msg:
        print 'There was an error trying to parse your start or end times.  "%s"' % msg
        parser.print_help()
        sys.exit(1)

    
    

#sort of awkward, but using the syntax below makes it explicit that the "if" code block is the entry
#point to the program.  The reason for then passing the arguments to a main() function
#is that variables declared in the block below are **GLOBAL**, and can hence cause confusion 
#later on when re-using those variable names in another function.  Doing all of the main work
#in the main() function ensures that main() variables stay in their expected scope.
if __name__ == '__main__':
    usage = """Chop a Mini-SEED file by two bounding times, and save each trace in a separate file.
    Optionally the user can:
     - plot the chopped traces
     - specify the output directory where chopped traces and plots are written.
     - get the range of the input data file
     - chop the input data interactively (NOT YET IMPLEMENTED)
    """
    cmdparser = argparse.ArgumentParser(usage=usage)
    cmdparser.add_argument('miniseed', metavar='SEED', nargs='+',
                           help='Mini-SEED file to process')
    cmdparser.add_argument("-o", "--outputDirectory", dest="outFolder",nargs='?',
                           help="""Select output directory where chopped time series files will be written 
    (defaults to current working directory)""", metavar="OUTPUTFOLDER")
    cmdparser.add_argument("-s", "--start", dest="startTime",
                           help="Select left edge of time series window (YYYY-MM-DDTHH:MM:SS.sss'", metavar="STARTTIME")
    cmdparser.add_argument("-e", "--end", dest="endTime",
                           help="Select left edge of time series window (YYYY-MM-DDTHH:MM:SS.sss'", metavar="ENDTIME")
    cmdparser.add_argument("-p", "--plot",
                           action="store_true", dest="makePlot", default=False,
                           help="Save a plot (JPG format) of the chopped data.")
    cmdparser.add_argument("-r", "--range",
                           action="store_true", dest="getRange", default=False,
                           help="Get the time range of all traces in Mini-SEED file.")
    cmdparser.add_argument("-i", "--interactive",
                           action="store_true", dest="interactiveMode", default=False,
                           help="Select time windows interactively")
    
    cmdargs = cmdparser.parse_args()
    main(cmdargs,cmdparser)
