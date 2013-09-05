#third party imports
from obspy import core, UTCDateTime
from obspy.iris import Client
import matplotlib.pyplot as mpl
#stdlib imports
import time
import os.path

import math
import matplotlib.mlab as mlab
import scipy.optimize.minpack as solv

from responses import Responses


def normalize360(theta):
    """
    Utility method to normalize an angle to between 0 and 360.

    @param theta angle in degrees
    @return angle in degrees, normalized to between 0 and 360.
    """
    return theta
    while theta < 0:
        theta += 360
    while theta >= 360:
        theta -= 360
    return theta


class StreamsException (Exception):
    """exception used when errors occur in Streams object."""


class Streams (object):
    """
    Used to perform various types of operations (reading, clipping, filtering)
    on Mini-SEED time series data.
    """

    def __init__(self):
        """
        Construct a new sensorloc.Streams object.
        """
        self.data = core.stream.Stream()

    def addStream(self, stream):
        """
        Append to this objects data.

        @param stream {obspy.core.stream.Stream} object.
        @see obspy.iris.Client.getWaveform.
        """
        self.data += stream

    def addFile(self, filename):
        """
        Wrapper for addStream and obspy.core.read.

        @param filename path to miniseed file.
        @see obspy.core.read.
        """
        self.addStream(core.read(filename))

    def getTimeExtent(self, common=True):
        """
        Get the time extent of all associated streams.
        @param common {Boolean} default True.
                When True, compute shared time extent across all streams.
                When False, compute minimum/maximum times across all streams.
        """
        start = None
        end = None
        for trace in self.data:
            traceStart = trace.stats['starttime']
            traceEnd = trace.stats['endtime']
            if start == None:
                # first start time
                start = traceStart
                end = traceEnd
            else:
                if common:
                    # common start, end times
                    if traceStart > start:
                        # earliest shared start time
                        start = traceStart
                    if traceEnd < end:
                        # latest shared end time
                        end = traceEnd
                else:
                    # min/max start, end times
                    if traceStart < start:
                        start = traceStart
                    if traceEnd > end:
                        end = traceEnd
            if end < start:
                raise StreamsException("endtime '%s' is less than starttime '%s'" %
                        (end, start))
        return {
            "start":start,
            "end":end
        }


    def trim(self, starttime=None, endtime=None):
        """
        Trim all traces to a specific data extent.

        @param starttime {UTCDateTime} Default None.
                When None, use start returned by getTimeExtent(True).
        @param endtime {UTCDateTime} Default None.
                When None, use end returned by getTimeExtent(True).
        @throws StreamsException when start < extent or end > extent.
        """
        extent = self.getTimeExtent(True)
        errors = []
        if starttime is None:
            # default is common data extent
            starttime = extent['start']
        elif starttime < extent['start']:
            # verify within extent
            errors.append("starttime '%s' is less than data start '%s'" %
                    (starttime, extent['start']))
        if endtime is None:
            # default is common data extent
            endtime = extent['end']
        elif endtime > extent['end']:
            # verify within extent
            errors.append("endtime '%s' is greater than data start '%s'" %
                    (endtime, extent['end']))
        if len(errors) > 0:
            # validation errors
            raise StreamsException("\n".join(errors))
        self.data.trim(starttime, endtime)

    def plot(self,filename=None):
        if filename is not None:
            self.data.plot(outfile=filename)
        else:
            self.data.plot()

    def write(self, outputdir, format='MSEED', encoding=None, reclen=None, suffix=''):
        """
        Write traces in stream to separate files in a directory.

        Filenames are determined by the method getTraceFilename.

        @param outputdir {String} the directory where files are written.
        @param format {String} Default MSEED.
        @param encoding {String} Default None (automatic).
        @param reclen {int} Default None (automatic).
        @param suffix {String} suffix to append to normal filename.
        """
        extent = self.getTimeExtent(True)
        # suffix depends on operations performed
        for trace in self.data:
            if hasattr(trace.stats,'encoding'):
                traceEncoding = trace.stats.encoding
            else:
                traceEncoding = encoding
            trace.write(
                filename=os.path.join(outputdir,
                        self.getTraceFilename(trace, 'mseed') + suffix),
                format=format,
                encoding=traceEncoding,
                reclen=reclen)

    def getTraceFilename(self, trace, format):
        s = trace.stats
        return '%s.%s.%s.%s.%s.%s' % (
                    s.network,
                    s.station,
                    s.channel,
                    s.location,
                    s.starttime.strftime('%Y.%j.%H.%M.%S'),
                    format
                )

    def simulate(self, responses=None, response_units='ACC', **kwargs):
        """
        Call simulate method on all traces in Streams.

        @param responses {sensorloc.responses.Responses} default None.
                Source of Response information.
                When present simulate is called with seedresp argument,
                and combined with response_units.
        @param response_units default 'ACC', used with responses argument.
        @param **kwargs any additional arguments to pass to trace simulate method.
        """
        for trace in self.data:
            # load response file for trace
            if responses:
                kwargs["seedresp"] = {
                    "filename": responses.getResponseFile(trace),
                    "date": trace.stats.starttime,
                    "units": response_units
                }
            else:
                kwargs["seedresp"] = None
            trace.simulate(**kwargs)

    def lowpassFilter(self,freq, sampleRate, corners=4):
        """
        Use a lowpass filter with specified parameters

        @param freq filter corner frequency
        @param sampleRate sampling rate in Hz
        @keyword corners number of corners
        """
        self.filter('lowpass', freq, sampleRate, corners=corners)

    def highpassFilter(self,freq, sampleRate, corners=4):
        """
        Use a highpass filter with specified parameters

        @param freq filter corner frequency
        @param sampleRate sampling rate in Hz
        @keyword corners number of corners
        """
        self.filter('highpass', freq, sampleRate, corners=corners)
            
    def bandpassFilter(self, freqmin=.1, freqmax=15, corners=2):
        """
        Use a bandpass filter with specified parameters

        @param freqmin minimum frequency
        @param freqmax maximum frequency
        @param corners number of corners
        """
        self.filter('bandpass', freqmin=freqmin, freqmax=freqmax, corners=corners)

    def filter(self, type, **kwargs):
        """
        Call filter method on all traces in Streams.

        @param type type of filter
        @param **kwargs options that are type dependent
        @see obspy.core.trace.Trace.filter
        """
        for trace in self.data:
            trace.filter(type, **kwargs)

    def coherence(self, referenceStream, referenceAzimuth, NFFT=None, noverlap=None, Fs=None):
        """
        Determine angle of a north and east channel based on a reference north channel.

        @param referenceStream stream containing a reference North channel.
        @param referenceAzimuth reference angle of North channel.
        @param NFFT number of points to use in FFT.
        @param noverlap number of overlapping points between FFTs.
        @param Fs sampling frequency. If omitted, uses referenceStream sampling_rate.
        @return relative angle from unknown north to reference north
                (referenceAngle-angle = actual angle of unknown channel).
        """
        referenceExtent = referenceStream.getTimeExtent()
        unknownExtent = self.getTimeExtent()
        if referenceExtent['start'] != unknownExtent['start'] or referenceExtent['end'] != unknownExtent['end']:
            raise StreamsException("reference and unknown streams must have same time extent")
        if Fs is None:
            Fs = referenceStream.data.traces[0].stats.sampling_rate
        if noverlap is None:
            noverlap = NFFT / 4
        # internal function to determine the coherence of unrotated and rotated data
        def cohere1(theta):
            theta_r = math.radians(theta)
            rotated = (self.data[0].data)*math.cos(theta_r) + (self.data[1].data)*math.sin(theta_r)
            coh,fre = mlab.cohere(referenceStream.data[0].data, rotated,
                    NFFT=NFFT, noverlap=noverlap, Fs=Fs)
            return (coh - 1).sum()
        # most coherent angle of rotation
        theta1 = solv.leastsq(cohere1, 0)
        theta1 = normalize360(theta1[0][0])

        # rotate data and compare against reference stream
        rotated = self.rotate(theta1)
        rotatedData1 = rotated.data[0].data.astype('Float64')
        referenceData1 = referenceStream.data[0].data.astype('Float64')
        scale1 = sum(abs(rotatedData1)) / sum(abs(referenceData1))
        residual1 = sum(referenceData1**2-rotatedData1*scale1)**2
        rotatedData2 = rotated.data[1].data.astype('Float64')
        referenceData2 = referenceStream.data[1].data.astype('Float64')
        scale2 = sum(abs(rotatedData2)) / sum(abs(referenceData2))
        residual2 = sum(referenceData2**2-rotatedData2*scale2)**2

        return {
            'theta': theta1,
            'azimuth': referenceAzimuth - theta1,
            'rotated': rotated,
            'scale1': scale1,
            'residual1': residual1,
            'scale2': scale2,
            'residual2': residual2
        }

    def rotate(self, angle):
        """
        Rotate 2 channels by a specified angle.

        @param angle the angle to rotate in degrees
        @return new streams object with rotated channels.
        """
        theta_r = math.radians(angle)
        # create new trace objects with same info as previous
        rotatedN = self.data[0].copy()
        rotatedE = self.data[1].copy()
        # assign rotated data
        rotatedN.data = self.data[0].data*math.cos(theta_r) + self.data[1].data*math.sin(theta_r)
        rotatedE.data = self.data[1].data*math.cos(theta_r) - self.data[0].data*math.sin(theta_r)
        # return new streams object with rotated traces
        streams = Streams()
        streams.addStream(rotatedN)
        streams.addStream(rotatedE)
        return streams


    def __str__(self):
        """
        Convert Streams to a string.
        Lists associated traces, and information about time extent.
        """
        s = '%d traces' % len(self.data)
        try:
            extent = self.getTimeExtent(False)
            s += '\nmin/max extent:  %s - %s' % (extent['start'], extent['end'])
            extent = self.getTimeExtent(True)
            s += '\ncommon  extent:  %s - %s' % (extent['start'], extent['end'])
        except StreamsException,msg:
            s += '\nno common extent' + str(msg)
        for trace in self.data:
            s += "\n" + str(trace)
        return s
