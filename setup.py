#!/usr/bin/env python

from distutils.core import setup

setup(name='SensorLoc',
      version='0.1',
      description='Seismic sensor timeseries manipulation tools',
      author='Mike Hearne, Jeremy Fee',
      author_email='mhearne@usgs.gov, jmfee@usgs.gov',
      url='https://github.com/usgs/asl-sensorloc',
      packages=['sensorloc'],
      scripts = ['filter.py','chop.py','rotate.py','coherence.py'],
     )
