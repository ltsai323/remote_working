destinationFOLDER=${1:-../ttt}

oF=${destinationFOLDER}/working.tar
echo "[outfile] $oF"
touch $oF; /bin/rm $oF
tar -cf $oF `ls --hide=*.root`
#### reject root file at current directory but data/*.root is still packed
