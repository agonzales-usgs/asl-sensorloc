#!/usr/bin/env python

#stdlib imports
import optparse
import sys
import time
import os.path

#import the object that does all of the work
from sensorloc.sensorloc import SensorLoc,SensorLocException

#third party imports
from obspy.core import utcdatetime

def main(options,arguments,parser):
    if options.interactiveMode:
        print '\nInteractive mode is not yet implemented.\n'
        parser.print_help()
        sys.exit(1)

    if len(arguments) < 1:
        print '\nYou must pass in the name of an input Mini-SEED file.\n'
        parser.print_help()
        sys.exit(1)

    sl = None
    try:
        sl = SensorLoc(filename=arguments[0])
    except SensorLocException,msg:
        print 'There was an error trying to process your file.  "%s"' % msg
        parser.print_help()
        sys.exit(1)
    clipstart,clipend = sl.getTimeRange()

    if options.getRange:
        print 'Start: %s\nFinish: %s\n' % (clipstart,clipend)
        sys.exit(0)
    
    try:
        if options.startTime is not None:
            clipstart = utcdatetime.UTCDateTime(options.startTime,iso8601=True)
        if options.endTime is not None:
            clipend = utcdatetime.UTCDateTime(options.endTime,iso8601=True)

        sl.chop(clipstart,clipend)
        sl.save('output.mseed')

        if options.makePlot:
            sl.plot('output.png')
        
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
    usage = "usage: %prog [options] inseedfile"
    cmdparser = optparse.OptionParser(usage=usage)
    cmdparser.add_option("-s", "--start", dest="startTime",
                      help="Select left edge of time series window (YYYY-MM-DDTHH:MM:SS.sss'", metavar="STARTTIME")
    cmdparser.add_option("-e", "--end", dest="endTime",
                      help="Select left edge of time series window (YYYY-MM-DDTHH:MM:SS.sss'", metavar="ENDTIME")
    cmdparser.add_option("-p", "--plot",
                      action="store_true", dest="makePlot", default=False,
                      help="Save a plot (PNG format) of the chopped data.")
    cmdparser.add_option("-r", "--range",
                      action="store_true", dest="getRange", default=False,
                      help="Get the time range of all traces in Mini-SEED file.")
    cmdparser.add_option("-i", "--interactive",
                      action="store_true", dest="interactiveMode", default=False,
                      help="Select time windows interactively")
    
    (cmdopts, cmdargs) = cmdparser.parse_args()
    main(cmdopts,cmdargs,cmdparser)
