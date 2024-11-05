#!/usr/bin/env sh
function PrintHelp() {
    echo use this file locally instead of use this code.
    echo This code sync remote and local.
    echo Arg1 : upload or download
    echo Arg2 : the folder wants to sync.
    echo "      (the remote destination is put in remote_path.txt)"
    echo "[error] $1"
    exit
}

operateMODE=$1
syncFOLDER=${2}/
newMEMO=$3

### add memo
if [ "$3" != "" ]; then
cat >> ${syncFOLDER}/history.md <<EOF
[$(date '+%y-%m-%d %H:%M')] ${newMEMO}
EOF
fi

if [ "$operateMODE" == "upload"   ]; then pass_state=1; fi
if [ "$operateMODE" == "download" ]; then pass_state=1; fi
if [ "$operateMODE" == "uploadALL"   ]; then pass_state=1; fi
if [ "$operateMODE" == "downloadALL" ]; then pass_state=1; fi
if [ "$pass_state" != 1 ]; then PrintHelp "operation mode only accepts 'upload' or 'download'"; fi

remotePATH=${syncFOLDER}/data/remote_path.txt
if [ ! -d "$syncFOLDER" ]; then PrintHelp "input folder '$syncFOLDER' does not exist"; fi
if [ ! -f "$remotePATH" ]; then PrintHelp "the remote_path.txt not found in input folder '$remotePATH'"; fi

remote_destation=`cat ${remotePATH}`

#rsync -avz --delete $syncFOLDER ntu8:~/Work/github/xPhoton/macros/step2.0.triggerTurnOn/
if [ $operateMODE == "upload"   ]; then rsync -avz --delete --exclude=*.root --exclude=log* --exclude=*.exe --exclude=*.pdf --exclude=*.png --exclude=.DS_Store $syncFOLDER $remote_destation; fi
if [ $operateMODE == "download" ]; then rsync -avz --delete --exclude=*.root --exclude=log* --exclude=*.exe --exclude=*.pdf --exclude=*.png --exclude=.DS_Store $remote_destation/* $syncFOLDER/; fi
if [ $operateMODE == "uploadALL"   ]; then rsync -avz --delete $syncFOLDER $remote_destation; fi
if [ $operateMODE == "downloadALL" ]; then rsync -avz --delete $remote_destation/* $syncFOLDER/; fi
