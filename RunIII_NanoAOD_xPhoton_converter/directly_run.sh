#!/usr/bin/env sh

inFILE=$1
outFILE=$2
isMC=$3
#executable=`printf 'ForTrigSF_MC.C("%s","%s", %s, "2022")' $inFILE $outFILE $isMC`
#echo $executable
#root -b <<EOF
#.x $executable
#EOF

root -b $inFILE <<EOF
.ls
if (_file0 ) .x ForTrigSF_MC.C(_file0, "$outFILE", $isMC, "2022EE")
EOF
