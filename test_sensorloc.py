#!/usr/bin/env python

#third party imports
from sensorloc import streams
from obspy import UTCDateTime
from obspy import core
import time
import os.path 

#stdlib imports
import os.path

'''
def test_getTimeExtent():
    seedstart = UTCDateTime('2010-04-15T00:00:00.023145Z')
    seedend = UTCDateTime('2010-04-15T23:59:59.960645Z')
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
    seedfile = os.path.join(homedir,'data','SNZO.seed')
    mystreams = streams.Streams()
    mystreams.addFile(seedfile)
    myrange = mystreams.getTimeExtent()
    assert myrange['start'] == seedstart
    assert myrange['end'] == seedend

def test_trim():
    seedstart = UTCDateTime('2010-04-15T07:00:00.023145Z')
    seedend = UTCDateTime('2010-04-15T20:59:59.010645Z')
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
    seedfile = os.path.join(homedir,'data','SNZO.seed')
    mystreams = streams.Streams()
    mystreams.addFile(seedfile)
    trimstart = UTCDateTime('2010-04-15T07:00:00.0Z')
    trimend = UTCDateTime('2010-04-15T20:59:59.0Z')
    mystreams.trim(starttime=trimstart,endtime=trimend)
    myrange = mystreams.getTimeExtent()
    assert myrange['start'] == seedstart
    assert myrange['end'] == seedend
'''
sl1 = streams.Streams()
sl2 = streams.Streams()
data1 = core.stream.Stream()
data2 = core.stream.Stream()
seed1 = '/home/agonzales/Documents/asl-sensorloc/00_LHZ.512.seed'
seed2 = '/home/agonzales/Documents/telemetry_days/IU_ANMO/2014/2014_062/00_LHZ.512.seed'
sl1.addFile(seed1)
sl2.addFile(seed2)
print
print "sl1 = " + str(sl1)
print "sl2 = " + str(sl2)
print
strm1 = core.read(seed1)
strm2 = core.read(seed2)
print "strm1() xs0 = " + str(strm1);	# test without += stream
print "strm2() tr1 = " + str(strm2);	
data1 += strm1 # add stream to data list
data2 += strm2
print "data1 xs0 = " + str(data1)
print "data2 tr1 = " + str(data2)
