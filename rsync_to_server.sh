#!/usr/bin/env sh
function PrintHelp() {
    echo use this file locally instead of use this code.
    echo This code sync remote and local.
    echo Arg1 : operation purpose [upload/download/uploadALL/downloadALL]
    echo Arg2 : Memo put into history.md
    echo "      (the remote destination is put in remote_path.txt)"
    echo "[error] $1"
    exit
}

operateMODE=$1
# use current directory instead of assign a folder
syncFOLDER=./
newMEMO=$2

### add memo
if [ "$2" != "" ]; then
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

# get variable "remote_destation" from remote_path.txt
#remote_destation=`cat ${remotePATH}`
source $remotePATH

#rsync -avz --delete $syncFOLDER ntu8:~/Work/github/xPhoton/macros/step2.0.triggerTurnOn/
if [ $operateMODE == "upload"   ]; then rsync -avz --delete --exclude=*.root --exclude=log* --exclude=*.exe --exclude=*.pdf --exclude=*.png --exclude=.DS_Store --exclude=HEPlot --exclude=stock_* $syncFOLDER $remote_destation; fi
if [ $operateMODE == "download" ]; then rsync -avz --delete --exclude=*.root --exclude=log* --exclude=*.exe --exclude=*.pdf --exclude=*.png --exclude=.DS_Store --exclude=HEPlot --exclude=stock_* $remote_destation/* $syncFOLDER/; fi
if [ $operateMODE == "uploadALL"   ]; then rsync -avz --delete --exclude=stock_* $syncFOLDER $remote_destation; fi
if [ $operateMODE == "downloadALL" ]; then rsync -avz --delete --exclude=stock_* $remote_destation/* $syncFOLDER/; fi
