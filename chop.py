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
from obspy.core.utcdatetime import UTCDateTime

def main(arguments,parser):
    print "interactiveMode = " + str(arguments.interactiveMode) + "\n" 
    if toBool(arguments.interactiveMode):
        print '\nInteractive mode is not yet implemented.\n'
        parser.print_help()
        sys.exit(1)

    if arguments.miniseed is None:
        print '\nYou must pass in the name of an input Mini-SEED file.\n'
        parser.print_help()
        sys.exit(1)

    # parse input Mini-SEED files (posargs) 
    sl = None
    try:
        sl = streams.Streams()
        for seed in arguments.miniseed:
            print "seed = " + str(seed) + "\n"
	    sl.addFile(seed)
   	print "sl = " + str(sl) 
    except streams.StreamsException,msg:
        print 'There was an error trying to process your file.  "%s"' % msg
        parser.print_help()
        sys.exit(1)
    
    cliprange = sl.getTimeExtent()
    print "cliprange = " + str(cliprange) + "\n"
    
    # get time range (start/end)
    print "getRange = " + str(arguments.getRange) + "\n" 
    if toBool(arguments.getRange):
        print 'Start: %s\nFinish: %s\n' % (cliprange['start'],cliprange['end'])
        sys.exit(0)
   
    # trim data by start/end times
    try:
        print "outFolder = " + str(arguments.outFolder) + "\n"
	if arguments.outFolder is None:
            outfolder = os.getcwd()
        else:
            outfolder = arguments.outFolder
            
        print "startTime = " + str(arguments.startTime) + "\n" 
	print "endTime = " + str(arguments.endTime) + "\n"	
	clipstart = UTCDateTime(arguments.startTime)
        clipend = UTCDateTime(arguments.endTime)
	print "clipstart = " + str(clipstart) + "\n"
	print "clipend = " + str(clipend) + "\n"

        sl.trim(starttime=clipstart,endtime=clipend)
	if not os.path.isdir(outfolder):
            os.makedirs(outfolder)
        sl.write(outfolder)

        print "makePlot = " + str(arguments.makePlot) + "\n" 
	if toBool(arguments.makePlot):
            for seed in arguments.miniseed:
                seedpath,seedfile = os.path.split(seed)
                seedbase,seedext = os.path.splitext(seedfile)
                seedimg = os.path.join(outfolder,seedbase+'.jpg')
                sl.plot(filename=seedimg)
        
    except Exception,msg:
        print 'There was an error trying to parse your start or end times.  "%s"' % msg
        parser.print_help()
        sys.exit(1)

# convert optional boolean strings to boolean vars
def toBool(value):
	"""
	Converts 'string' to boolean. Raises exception for invalid formats
		True values: 1, True, true, "1", "True", "true", "yes", "y", "t"
		False values: 0, False, false, "0", "False", "false", "no", "n", "f"
	"""
	if str(value).lower() in ("true", "yes", "t", "y", "1"): return True
	if str(value).lower() in ("false", "no", "f", "n", "0"): return False
	raise Exception('Invalid value for boolean conversion: ' + str(value))

#sort of awkward, but using the syntax below makes it explicit that the "if" code block is the entry
#point to the program.  The reason for then passing the arguments to a main() function
#is that variables declared in the block below are **GLOBAL**, and can hence cause confusion 
#later on when re-using those variable names in another function.  Doing all of the main work
#in the main() function ensures that main() variables stay in their expected scope.
if __name__ == '__main__':
    usage = """Chop a Mini-SEED file by two bounding times, and save each trace in a separate file.
    If start/end times are NOT set, the output files will be chopped to the common extent of all of the
    obspy streams input. 
    Optionally the user can:
     - plot the chopped traces
     - specify the output directory where chopped traces and plots are written.
     - get the range of the input data file
     - chop the input data interactively (NOT YET IMPLEMENTED)
    
    """
    
    cmdparser = argparse.ArgumentParser(usage=usage)
    
    cmdparser.add_argument('miniseed', metavar='SEED', nargs='+',
                           help='Mini-SEED file to process')
    
    cmdparser.add_argument("-o", "--outputDirectory", dest="outFolder", nargs='?',
                           help="""Select output directory where chopped time series files will be written 
    (defaults to current working directory)""", metavar="OUTPUTFOLDER")
    
    cmdparser.add_argument("-s", "--start", dest="startTime", default=None,
                           help="Select left edge of time series window (YYYY-MM-DDTHH:MM:SS.sss)'", metavar="STARTTIME")
    
    cmdparser.add_argument("-e", "--end", dest="endTime", default=None,
                           help="Select right edge of time series window (YYYY-MM-DDTHH:MM:SS.sss)'", metavar="ENDTIME")
   
    #action="store_true"
    cmdparser.add_argument("-p", "--plot",
    			   dest="makePlot", default="False",
                           help="Save plot(s) (JPG format) of the chopped data.")
   
    #action="store_true"
    cmdparser.add_argument("-r", "--range",
                           dest="getRange", default="False",
                           help="Get the time range of all traces in Mini-SEED file.")
    
    #action="store_true"
    cmdparser.add_argument("-i", "--interactive",
                           dest="interactiveMode", default=False,
                           help="Select time windows interactively")
    
    cmdargs = cmdparser.parse_args()
    main(cmdargs,cmdparser)
