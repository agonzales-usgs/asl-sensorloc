#!/usr/bin/env python

# -------------------------------------------------------------------
# Authors: Alejandro Gonzales, Jeremy Fee, Mike Hearne
# Filename: chop.py
# -------------------------------------------------------------------
# Purpose: Chop a Mini-SEED file by two bounding times, and
# save each trace in a separate file. If start/end times 
# are NOT set, the output files will be chopped to the 
# common extent of all of the obspy streams input
# -------------------------------------------------------------------
# Methods/Functions:
#	* Chop() - main parent class (handles all bckgrnd processing)
#		-> chopMiniSeed() - main processing method
#		-> toBool() - converts input strings to booleans
#	* ChopArgs() - subclass to Chop() (handles input args)
#	* Help() - help option for user
# -------------------------------------------------------------------

import argparse
import sys
import time
import os.path
import os, re, string

# import the object that does all of the work
from sensorloc import streams

# third party imports
from obspy.core.utcdatetime import UTCDateTime

# Parent class will receive vars from inherited
# subclass ChopArgs() using super()
class Chop(object):
	# intialize input vars	
	def __init__(self, miniseed, **kwargs):
		print 'Chop() parent class'	
		print '--------------------'	

		# intialize mseed files
		print "printing miniseed files..."
		print "----------------------------"	
		self.miniseed = miniseed	
		for i in range(len(miniseed)):
			print "mseed = " + miniseed[i]
		print 
		
		# loop through **kwargs and assign optional args (global)	
		self.outFolder = ""	# init output directory
		self.startTime = ""	# init start obspy UTC (YYYY-MM-DDTHH:MM:SS.sss)	
		self.endTime = ""	# init end obspy UTC (YYYY-MM-DDTHH:MM:SS.sss)	
		self.makePlot = False	# init make plot (jpg format)
		self.getRange = False	# init get time range of all traces in mseed 
		self.interactiveMode = False	# init select time windows interactively	
		print "printing **kwargs..."	
		print "-----------------------"	
		for key, value in kwargs.iteritems():
			if key == "output": self.outFolder = value
			elif key == "start": self.startTime = UTCDateTime(value)
			elif key == "end": self.endTime = UTCDateTime(value)
			elif key == "plot": self.makePlot = self.toBool(value)
			elif key == "timerange": self.getRange = self.toBool(value)
			elif key == "interactive": self.interactiveMode = self.toBool(value)
		print "outputFolder = " + self.outFolder
		print "startTime = " + str(self.startTime)
		print "endTime = " + str(self.endTime)
		print "makePlot = " + str(self.makePlot)
		print "getRange = " + str(self.getRange)
		print "interactiveMode = " + str(self.interactiveMode)
		print 

		# interactive mode not implemented (exit program)	
		if self.interactiveMode:
			print '\nInteractive mode is not yet implemented.'
			print 'Program exiting...\n'
			sys.exit(1)
		
		# if miniseed list does not contain file exit
		# *args check in ChopArgs() should take care of 
		# this exception (additional check)
		if len(self.miniseed) != 0:
			self.chopMiniSeed()
		else:
			print '\nNo miniseed files present.'
			print 'Program exiting...\n'
			sys.exit(1)

	# chop Mini-SEED data
	def chopMiniSeed(self):
		print "chopMiniSeed()"
		print "--------------------"
		st = None
		try:
			st = streams.Streams()	# create streams list
			for seed in self.miniseed:
				st.addFile(seed)
		except streams.StreamsException, msg:
			print '\nThere was an error trying to process your file. "%s"' % msg
			print 'Program exiting...\n'	
			sys.exit(1)

		# get time extent of stream(s) (00:00:00.0 - 23:59:59.0)
		# note: this will not allow you to chop the data (?)	
		cliprange = st.getTimeExtent()
		if self.getRange:
			print 'Start: %s\nFinish: %s\n' % (cliprange['start'], cliprange['end'])
			sys.exit(0)

		try:
			# create output directory if one DNE
			if self.outFolder == "":
				outfolder = os.getcwd()	
			else:
				outfolder = self.outFolder
			if not os.path.isdir(outfolder):
				print "outFolder DNE. Creating..."	
				os.makedirs(outfolder)
		
			# trim data using startTime/endTime (write to outfolder)	
			clipstart = self.startTime
			clipend = self.endTime
			print "clipstart = " + str(clipstart)
			print "clipend = " + str(clipend)
			print	
			st.trim(starttime=clipstart, endtime=clipend)
			st.write(outfolder)
		
			# plot stream
			if self.makePlot:
				print "plotting stream..."	
				for seed in self.miniseed:
					seedpath, seedfile = os.path.split(seed)
					seedbase, seedext = os.path.splitext(seedfile)
					seedimg = os.path.join(outfolder, seedbase+'.jpg')
					st.plot(filename=seedimg)
		except Exception, msg:
			print '\nThere was an error trying to parse your start or end times. "%s"' % msg
			print 'Program exiting...\n'
			sys.exit(1)
	
	# convert optional boolean strings to boolean vars
	def toBool(self, value):
		"""
		Converts 'string' to boolean. Raises exception for invalid formats
			True values: 1, True, true, "1", "True", "true", "yes", "y", "t"
			False values: 0, False, false, "0", "False", "false", "no", "n", "f" 
		"""
		if str(value).lower() in ("true", "yes", "t", "y", "1"): return True
		if str(value).lower() in ("false", "no", "f", "n", "0"): return False
		raise Exception('Invalid value for boolean conversion: ' + str(value))

# Subclass uses super() to pass individual params 
# to parent class Chop()
class ChopArgs(Chop):	
	def __init__(self, *args, **kwargs):	
		print 'ChopArgs() subclass'	
		print '--------------------'	
		
		# check for empty args (no mseed files) 
		if not args:
			print '\nYou must pass in the name of an input Mini-SEED file.'
			print 'Program exiting...\n'
			sys.exit(1)
		
		# initialize positional arguments (*args defines mseed files)	
		miniseed = []	# initialize mseed file list	
		for f in args:
			miniseed.append(f)	
	
		# pass variables to parent class Chop()
		super(ChopArgs, self).__init__(miniseed, **kwargs)	

def Help():
	"""
	UTCTime:
		- utc:					YYYY-MM-DD HH:MM:SS.sss
		- utc.strftime(%Y%m%d_%H:00:00): 	YYYYMMDD_HH:MM:SS
		- UTCDateTime(utc.strftime()):		YYYY-MM-DDTHH:MM:SS.sssZ 
	"""
	
	usage = """Usage: Chop a Mini-SEED file by two bounding times, and
	save each trace in a separate file. If start/end times
	are NOT set, the output files will be chopped to the 
	common extent of all of the obspy streams input.
	Optionally the user can:
		- plot the chopped traces
		- specify the output directory where chopped traces/plots are written
		- get the range of the input data file
		- chop the input data interactively (NOT YET IMPLEMENTED)
	Arguments will be passed to:
		- chop.ChopArgs(posargs, optargs)
		- posargs - positional arguments (miniseed file(s))
		- optargs - optional arguments (output, start, end, plot, timerange, interactive)
	"""

	posargs = """postional arguments:
	('x.seed', 'y.seed',...)	   \tMini-SEED file(s) to process 	
	"""

	optargs = """optional arguments:
	(output = '/path/to/dir/')	   \tSelect output directory where chopped time 
					   \tseries files will be written 
					   \t(default: cwd)
	(start = 'YYYY-MM-DDTHH:MM:SS.sss')\tSelect left edge of time series window
					   \t(UTCDateTime)
	(end = 'YYYY-MM-DDTHH:MM:SS.sss')  \tSelect right edge of time series window
				           \t(UTCDateTime) 
	(plot = 'True/False')		   \tSave plot(s) (JPG format) of chopped data
	(timerange = 'True/False')	   \tGet time range of all traces in MSEED file
	(interactive = 'True/False')	   \tSelect time windows interactively (NOT IMPLEMENTED)
	"""

	print usage 
	print posargs
	print optargs
