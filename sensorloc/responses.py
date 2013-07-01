import os.path


class Responses (object):
	"""
	A utility class for managing station response data.
	"""

	def __init__(self, directory='.', client=None):
		"""
		Create a new Responses object.

		@param directory {String} default '.'.
				directory containing response files,
				or, when used with client, used to store response files.
		@param client {obspy.iris.Client} default None.
				When configured, client is used to download response files,
				when they do not already exist in directory.
		"""
		self.directory = directory or '.'
		self.client = client

	def getResponseFile(self, trace, starttime=None, endtime=None):
		"""
		Get the path to a response file for a specific trace.

		@param trace {obspy.core.trace.Trace} the trace to use.
		@param starttime {obspy.core.UTCDateTime} default trace.stats.starttime
				the start time to use when requesting.
				only used when client is configured.
		@param endtime {obspy.core.UTCDateTime} default trace.stats.endtime
				the end time to use when requesting.
				only used when client is configured.
		"""
		network = trace.stats.network
		station = trace.stats.station
		location = trace.stats.location
		channel = trace.stats.channel
		starttime = starttime or trace.stats.starttime
		endtime = endtime or trace.stats.endtime
		filename = os.path.join(self.directory,
				'RESP.%s.%s.%s.%s' % (network, station, location, channel))
		if (not os.path.exists(filename)) and self.client:
			# request using client
			self.client.saveResponse(
					filename,
					network,
					station,
					location,
					channel,
					starttime or trace.stats.starttime,
					endtime or trace.stats.endtime)
		return filename
