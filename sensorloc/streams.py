#third party imports
from obspy import core, UTCDateTime
from obspy.iris import Client
#stdlib imports
import time
import os.path

from responses import Responses

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
		self.data = core.stream.Stream();

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
			raise StreamsException("\n".join(errors));
		self.data.trim(starttime, endtime)

	def plot(self):
		self.data.plot()

	def write(self, outputdir, format='MSEED', encoding=None, reclen=None):
		extent = self.getTimeExtent(True)
		for trace in self.data:
			trace.write(
				filename=os.path.join(outputdir, self.getTraceFilename(trace, 'mseed')),
				format=format,
				encoding=encoding or trace.stats.encoding,
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
