#stdlib imports
import time

#third party imports
from obspy import core
from obspy.iris import Client
import matplotlib.pyplot as mpl

class SensorLocException(Exception):
    """Used to indicate errors with the SensorLoc utilities."""

class SensorLoc(object):
    """
    Used to perform various types of operations (reading, clipping, filtering) on Mini-SEED 
    time series data.
    """
    #miniseed encoding types
    ENCODING = {'ASCII':0,
                'INT16':1,
                'INT32':3,
                'FLOAT32':4,
                'FLOAT64':5,
                'STEIM1':10,
                'STEIM2':11}
    DataStream = None
    StreamStart = None
    StreamEnd = None
    def __init__(self,filename=None):
        """
        Create a SensorLoc object.

        @keyword filename: Mini-SEED filename, containing time series data.
        """
        if filename is not None:
            self.load(filename)

    def load(self,filename):
        """
        Load the data from a Mini-SEED file into an ObsPy Stream object.

        Also captures the time span for all of the Traces in the Stream.

        @param filename: Mini-SEED filename, containing time series data.
        """
        try:
            self.DataStream = core.read(filename)
        except:
            raise SensorLocException('Could not open "%s".  Possibly not a Mini-SEED file?')
        self.getTimeRange()
        
    def getTimeRange(self):
        """
        Capture the time span of all Traces in the Stream.

        @return Two element tuple of ObsPy UTCDateTime (start,end) times.
        """
        if self.StreamStart is not None:
            return (self.StreamStart,self.StreamEnd)
        #get the time range of all traces in the stream
        self.StreamEnd = core.UTCDateTime(0)
        self.StreamStart = core.UTCDateTime(int(time.time()))
        for trace in self.DataStream:
            if trace.stats['starttime'] < self.StreamStart:
                self.StreamStart = trace.stats['starttime']
            if trace.stats['endtime'] > self.StreamEnd:
                self.StreamEnd = trace.stats['endtime']
        return (self.StreamStart,self.StreamEnd)

    def chop(self,starttime,endtime):
        """
        Chop all traces in the Stream to the input start/end times.  This routine modifies
        the internal Stream object.

        @param starttime: UTCDateTime object indicating the desired start time of the new Stream.
        @param endtime: UTCDateTime object indicating the desired end time of the new Stream.
        """
        if starttime < self.StreamEnd and endtime > self.StreamStart:
            clipstart = max(starttime,self.StreamStart)
            clipend = min(endtime,self.StreamEnd)
            outstream = self.DataStream.slice(clipstart,clipend)
        else:
            raise SensorLocException('Your start and/or end times are outside the bounds of the timeseries.')

        self.DataStream = outstream

    def plot(self,filename):
        """
        Save a plot of all Traces in the internal Stream object to a PNG file.

        @param filename: Desired output PNG file name.
        @param endtime: UTCDateTime object indicating the desired end time of the new Stream.
        """
        f = self.DataStream.plot()
        mpl.savefig('output.png')
        
    def save(self,filename):
        """
        Save the (possibly modified) internal Stream object to a Mini-SEED file.

        @param filename: Desired output Mini-SEED file name.
        """
        #encoding = self.ENCODING[self.DataStream[0].stats['mseed']['encoding']]
       	encoding = 'FLOAT64' 
	try:
            self.DataStream.write(filename,format='MSEED',encoding=encoding)
        except Exception,msg:
            raise SensorLocException('Could not save data to file %s due to error "%s"' % (filename,msg))

        
            
        
