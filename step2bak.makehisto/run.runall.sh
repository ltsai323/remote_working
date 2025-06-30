#!/usr/bin/env sh
outDIR=${1:-tmp}
phoETAbin=$2
jetETAbin=$3
phoPTlow=$4
phoPThigh=$5
dataERA=2022EE

this_file=`realpath $0`
BASE_DIR=`dirname $this_file`
PATH=$BASE_DIR:$PATH
PYTHONPATH=$PWD:$PYTHONPATH




function the_exit() { echo "ERROR - "$1; exit 1; }
cd $outDIR/


if [ "$phoPThigh" == "" ]; then the_exit "[InvalidArgument - makehisto.py] Received arguments: outDIR($outDIR) phoETAbin($phoETAbin) jetETAbin($jetETAbin) phoPTlow($phoPTlow) phoPThigh($phoPThigh)"; fi
python3  $BASE_DIR/makehisto_Run2022_workingpoint.py $dataERA $phoETAbin $jetETAbin $phoPTlow $phoPThigh

# output out_makehisto.root
