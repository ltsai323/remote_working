#!/usr/bin/env sh
pPtRange=( 210 230 250 300 400 500 600 800 1000 -1 )

echo "[Collecting results]"
total_fitinfo_gjet_fitting=fitinfo.gjet_fitting.csv
total_fitinfo_signalregion=fitinfo.signalregion.csv
total_fitinfo_datasideband=fitinfo.datasideband.csv

function init_file() { touch $1; /bin/rm -r $1; echo "[CleanUp] file $1 is cleaned up."; }
init_file $total_fitinfo_gjet_fitting
init_file $total_fitinfo_signalregion
init_file $total_fitinfo_datasideband
for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtL=${pPtRange[$idx-1]}
    pPtR=${pPtRange[$idx]}
    
    out_dir=bin_${pEtaBin}_${jEtaBin}_${idx}
    
    echo "[Procesing folder] $out_dir"
    python3 collect_fitinfo.py  $out_dir/fitinfo_gjet_inclusive.yaml $total_fitinfo_gjet_fitting 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_gjet_fitting}.collect_fitinfo.log
    python3 collect_fitinfo.py  $out_dir/fitinfo.signal_region.yaml  $total_fitinfo_signalregion 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_signalregion}.collect_fitinfo.log
    python3 collect_fitinfo.py  $out_dir/fitinfo_sideband.yaml       $total_fitinfo_datasideband 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_datasideband}.collect_fitinfo.log
done; done; done
echo "[exported file] $total_fitinfo_gjet_fitting "
echo "[exported file] $total_fitinfo_signalregion "
echo "[exported file] $total_fitinfo_datasideband "

csv_to_root.py $total_fitinfo_gjet_fitting | tee ${total_fitinfo_gjet_fitting}.csv_to_root.log
csv_to_root.py $total_fitinfo_signalregion | tee ${total_fitinfo_signalregion}.csv_to_root.log
csv_to_root.py $total_fitinfo_datasideband | tee ${total_fitinfo_datasideband}.csv_to_root.log
