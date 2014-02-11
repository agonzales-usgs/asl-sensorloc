#!/bin/sh

seeddir=/home/agonzales/Documents/asl-sensorloc/data/coherence_example/telemetry_days/IU_MIDW/2014/2014_031/
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
