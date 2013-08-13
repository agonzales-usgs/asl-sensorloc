#!/usr/bin/env python

#third party imports
from sensorloc import streams
from obspy import UTCDateTime

#stdlib imports
import os.path

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




    
    
