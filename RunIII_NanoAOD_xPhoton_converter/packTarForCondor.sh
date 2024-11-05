destinationFOLDER=$1

oF=${destinationFOLDER}/working.tar
touch $oF; /bin/rm $oF
tar -cf $oF `ls --hide=*.root`
#### reject root file at current directory but data/*.root is still packed
