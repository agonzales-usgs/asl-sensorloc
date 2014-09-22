#!/usr/bin/env python

import chop
import os

# Example of running chop with *args and **kwargs
"""
kwargs:
	- output: output directory for chopped traces (string) 
	- start: start time (YYYY-MM-DDTHH:MM:SS.sss)
	- end:	end time (YYYY-MM-DDTHH:MM:SS.sss)
	- plot: make plot (True/False)
	- range: get time range of all traces in mseed (True/False)
	- interactive: select time windows interactively (True/False)
"""

#chop.Help()
# Changing seed directory to telemetry_days from 
# asldcc01/tr1/ mount point
homedir = os.getcwd()
telemdir = '/home/agonzales/Documents/telemetry_days'
station = 'IU_ANMO/2014'
day = '2014_110'
sdfile = '10_LHZ.512.seed'
stationdir = os.path.join(telemdir, station)
seeddir = os.path.join(stationdir, day)
seedfile = os.path.join(seeddir, sdfile)
outputdir = os.path.join(homedir, 'chopOutput')
obj1 = chop.ChopArgs(seedfile, output=outputdir,\
			start="2014-04-20T07:00:00.0Z",\
			end="2014-04-20T17:30:00.0Z",\
			plot="true", timerange="false", interactive="false")
'''
# Passing no mseed files should result in error
obj2 = chop.ChopArgs(output="name.txt", start="02/04/14:13:30", end="02/06/14:13:30",\
			plot="true", interactive="true")
'''
