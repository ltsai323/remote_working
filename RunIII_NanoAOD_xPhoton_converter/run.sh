#!/usr/bin/env sh

idx=0

for inFILE in `cat ../ttt/remoteFileList_GJetPythiaFlat.txt`;do
    make run1 iFILE=$inFILE oFILE=outFile_${idx}.root  > log_outFile_${idx}.log 2>&1

    idx=$(( $idx + 1 ))
done
