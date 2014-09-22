#!/bin/sh

<<COMMENT1
* SEED, Mini-SEED file to process
* -o, output directory
* -s, start time (YYYY-MM-DDTHH:MM:SS.sss)
* -e, end time (YYYY-MM-DDTHH:MM:SS.sss)
	-> Start/End times String->UTC:
	   date --utc --date "2014-03-03T07:30:00.0Z" (+%s to Gregorian String)
* -p, save plot(s) of the chopped data
* -r, get time range of all traces in Mini-SEED file
* -i, select time windows interactively (not implemented)
	-> Plot/Range/Interaction booleans:
	   plot=true
COMMENT1

seeddir=/home/agonzales/Documents/telem/IU_ANMO/2014/2014_062
seedfile=$seeddir/00_LHZ.512.seed
homedir=${PWD}
outputdir=$homedir/chopOut
#start=$(date --utc --date "2014-03-05T07:00:00.0Z" +%s)
#end=$(date --utc --date "2014-03-05T17:30:00.0Z" +%s)
start="2014-03-03T07:00:00.0Z"
end="2014-03-03T17:30:00.0Z"
plot="True"
timerange="False"
interactive="False"
makedir="mkdir $outputdir"
cmd="./chop.py $seedfile -o $outputdir -s $start -e $end -p $plot -r $timerange -i $interactive"
echo $makedir
echo $cmd
echo
if [ ! -d "$outputdir" ]; then
	echo "Directory $outputdir DNE creating..."
	$makedir
fi
$cmd
