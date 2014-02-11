#!/usr/bin/env python

# ---------------------------------------------------------------------
# Authors: Alejandro Gonzales, Jeremy Fee, Mike Hearne
# Filename: coherence.py
# ---------------------------------------------------------------------
# Purpose: Determine the angle between a reference station and
# an unknown station
# ---------------------------------------------------------------------
# Methods/Functions:
#	* Coherence() - main parent class (handles bckgrnd processing)
#	* CoherenceArgs() - subclass to Coherence() (handles input args)
#	* Help() - help option for user
# ---------------------------------------------------------------------

import argparse
import sys
import time
import os, os.path

# import local package
import sensorloc

# third party imports
from obspy import UTCDateTime

'''
	posargs = """positional arguments:
	('x.seed', ['y.seed'])		\tMini-SEED files to process (1 OR 2)
	"""
	
	optargs = """optional arguments:
	(verbose = 'True/False')	\tVerbose output
	(ref = 'N.seed, E.seed')	\tTwo reference Mini-SEED files (north/east)
	(refAzimuth = float)		\tAzimuth of reference north component 
	(nfft = int)			\tNumber of points used in FFT, must be even
					\t(default=256)
	(noverlap = int)		\tNumber of overlapping data poins used in FFT,
					\tdefaults to NFFT/4
	(fs = int)			\tNumber of samples per second, defaults to 
					\treference miniseed sampling rate
	(rotate = 'True/False')		\tAfter determining and reporting angle, 
					\trotate data to align with reference
	(output = '/path/to/dir')	\tSpecify output directory (default=None)
	(plot = 'True/False')		\tSave a plot (PNG format) of chopped data
					\t(default=False)
'''

# Parent class will receive vars from inherited
# subclass CoherenceArgs() using super()
class Coherence(object):
	# initialize input vars
	def __init__(self, miniseed, **kwargs):
		print 'Coherence() parent class'
		print '-------------------------'

		# initialize mseed files
		print 'printing miniseed files...'
		self.miniseed = miniseed
		for i in range(len(miniseed)):
			print "mseed = " + miniseed[i]
		print

		# loop through **kwargs and assign optional args (global)
		self.verbose = False	# init output verbosity
		self.ref = []		# init reference mseed files (N/E => LH1/LH2)
		self.refAzimuth = 0.0	# init azimuth of reference north component (LH1)

# Subclass uses super() to pass individual params
# to parent class Coherence()
class CoherenceArgs(Coherence):
	def __init__(self, *args, **kwargs):
		print 'CoherenceArgs() subclass'
		print '-------------------------'
	
		# check for empty args (no mseed files)
		# will also check for count 
		if not args:
			print '\nNo Mini-SEED files given. Pass one/two files.'
			print 'Program exiting...\n'
			sys.exit(1)

		# initialize positional arguments (*args defines mseed files)
		miniseed = []
		for f in args:
			miniseed.append(f)

		# pass variables to parent class Coherence()
		super(CoherenceArgs, self).__init__(miniseed, **kwargs)

def Help():
	usage = """Usage: Determine the angle between a reference station
	sensor and an unknown station sensor.
	Optionally the user can:
		- specify two reference miniseed files (north then east)
		- specify the azimuth of the reference north component
		- specify number of FFT points (must be even)
		- specify number of overlapping data points used in FFT,
		  defaults to NFFT/4
		- specify number of samples per second, defaults to 
		  reference miniseed sampling rate
		- rotate data to align with reference
		- specify output directory
		- save plot (PNG format) of the chopped data
	Arguments will be passed to:
		- coherence.CoherenceArgs(posargs, optargs)
		- posargs - positional arguments (miniseed file(s))
		- optargs - optional arguments (verbose, ref, refAzimuth, nfft,
		noverlap, fs, rotate, output, plot)
	"""
		
	posargs = """positional arguments:
	('x.seed', ['y.seed'])		\tMini-SEED files to process (1 OR 2)
	"""
	
	optargs = """optional arguments:
	(verbose = 'True/False')	\tVerbose output
	(ref = 'N.seed, E.seed')	\tTwo reference Mini-SEED files (north/east)
	(refAzimuth = float)		\tAzimuth of reference north component 
	(nfft = int)			\tNumber of points used in FFT, must be even
					\t(default=256)
	(noverlap = int)		\tNumber of overlapping data poins used in FFT,
					\tdefaults to NFFT/4
	(fs = int)			\tNumber of samples per second, defaults to 
					\treference miniseed sampling rate
	(rotate = 'True/False')		\tAfter determining and reporting angle, 
					\trotate data to align with reference
	(output = '/path/to/dir')	\tSpecify output directory (default=None)
	(plot = 'True/False')		\tSave a plot (PNG format) of chopped data
					\t(default=False)
	"""

	print usage
	print posargs
	print optargs
