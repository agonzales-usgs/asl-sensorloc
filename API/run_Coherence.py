#!/usr/bin/env python

import coherence 
import os

# Example of running coherence with *args and **kwargs
#coherence.Help()
homedir = os.getcwd()
telemdir = '/home/agonzales/Documents/telemetry_days/'
stationdir = 'IU_BBSR/2014/2014_049'
seeddir = os.path.join(telemdir, stationdir)
print "seeddir = %s" % seeddir
tstseed1 = os.path.join(seeddir, '00_LH1.512.seed')
tstseed2 = os.path.join(seeddir, '00_LH2.512.seed')
refseed1 = os.path.join(seeddir, '10_LH1.512.seed')
refseed2 = os.path.join(seeddir, '10_LH2.512.seed')
coherence.Help()
