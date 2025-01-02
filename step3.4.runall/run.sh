#!/usr/bin/env sh
outFOLDER=${1:-hiiii}

pPtRange=( 210 230 250 300 400 500 600 800 1000 -1 )

echo ${#pPtRange[@]}

for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtL=${pPtRange[$idx-1]}
    pPtR=${pPtRange[$idx]}
    
    out_dir=bin_${pEtaBin}_${jEtaBin}_${idx}
    out_log=bin_${pEtaBin}_${jEtaBin}_${idx}.log
    echo "[Running to bkg] $out_dir"
    sh run.fit.parameters.sh $out_dir $pEtaBin $jEtaBin $pPtL $pPtR > $out_log 2>&1 &
    bkgjob_submit_with_limitation_Nminus3.sh
done; done; done

echo "[All fitting job submitted]"
wait
echo "[All fitting job finished]"


echo "[Collecting results]"
total_fitinfo_gjet_fitting=fitinfo.gjet_fitting.csv
total_fitinfo_signalregion=fitinfo.signalregion.csv
total_fitinfo_datasideband=fitinfo.datasideband.csv

function clean_up_file() { touch $1; /bin/rm -r $1; echo "[CleanUp] file $1 is cleaned up."; }
clean_up_file $total_fitinfo_gjet_fitting
clean_up_file $total_fitinfo_signalregion
clean_up_file $total_fitinfo_datasideband
for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtL=${pPtRange[$idx-1]}
    pPtR=${pPtRange[$idx]}
    
    out_dir=bin_${pEtaBin}_${jEtaBin}_${idx}
    
    echo "[Running to bkg] $out_dir"
    python3 collect_fitinfo.py  $out_dir/fitinfo_gjet_inclusive.yaml $total_fitinfo_gjet_fitting 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_gjet_fitting}.collect_fitinfo.log
    python3 collect_fitinfo.py  $out_dir/fitinfo.signal_region.yaml  $total_fitinfo_signalregion 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_signalregion}.collect_fitinfo.log
    python3 collect_fitinfo.py  $out_dir/fitinfo_sideband.yaml       $total_fitinfo_datasideband 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_datasideband}.collect_fitinfo.log
done; done; done
echo "[exported file] $total_fitinfo_gjet_fitting "
echo "[exported file] $total_fitinfo_signalregion "
echo "[exported file] $total_fitinfo_datasideband "

python3 csv_to_root.py $total_fitinfo_gjet_fitting | tee ${total_fitinfo_gjet_fitting}.csv_to_root.log
python3 csv_to_root.py $total_fitinfo_signalregion | tee ${total_fitinfo_signalregion}.csv_to_root.log
python3 csv_to_root.py $total_fitinfo_datasideband | tee ${total_fitinfo_datasideband}.csv_to_root.log

echo "[CollectOutputs] Put all files into output folder $outFOLDER"
touch $outFOLDER ; /bin/rm -r $outFOLDER; mkdir $outFOLDER
mv bin_* $outFOLDER/
mv fitinfo.* $outFOLDER/

echo "[all job finished]"
wget -nc 'https://api.day.app/Qc9reVSUWxKgJ6cqNckgbB/Job Finished/all binning fit accomplished' -O aabark > /dev/null ; /bin/rm aabark
