#!/usr/bin/env sh

filelist=$1

idx=0
for infilename in `cat $filelist`;do
  oFILE=out_${idx}.root
  echo ./a.out $infilename $oFILE  2022EE
  ./a.out $infilename $oFILE  2022EE > log_$idx 2>&1
  sh bkgjob_submitN.sh 5

  idx=$(($idx+1))
done

echo "[AllJobSubmitted]"
wait
echo "[AllJobFinished]"

