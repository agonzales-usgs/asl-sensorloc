#!/bin/sh

<<COMMENT1
* -r, two reference mseed files (N/E)
* -ra, reference Azimuth
* -nfft, number of FFT points (even)
* -noverlap, number of overlapping data pts used in FFT
* -fs, sample per second
* --rotate, after determining reporting angle, rotate data to align with reference
* -d, output directory
* -p, plot (PNG format)
Example (used to find the azimuth between two sensors):

./coherence.py 00_LH1.512.seed 00_LH2.512.seed -r 10_LH1.512.seed 10_LH2.512.seed 
	-ra 90 -p
COMMENT1

seeddir=/home/agonzales/Documents/telemetry_days/IU_BBSR/2014/2014_048/
testNorth=$seeddir/00_LH1.512.seed
testEast=$seeddir/00_LH2.512.seed
refNorth=$seeddir/10_LH1.512.seed
refEast=$seeddir/10_LH2.512.seed
ref="-r"
refAzimuth="-ra"
angle=0.0
cmd="./coherence.py $testNorth $testEast $ref $refNorth $refEast $refAzimuth $angle"
echo "testNorth =" $testNorth
echo "testEast =" $testEast
echo "refNorth =" $refNorth
echo "refEast =" $refEast
echo
$cmd
