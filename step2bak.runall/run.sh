#!/usr/bin/env sh
outFOLDER=${1:-runresult}
pPtBinning3=( 210 230 250 300 400 500 600 1000 1500 )

pPtRange=("${pPtBinning3[@]}")

function estimate_from_data() {
pEtaBin=$1
jEtaBin=$2
pPtBin=$3
pPtLow=$4
pPtHigh=$5
echo "[Running] estimate_from_data $pEtaBin $jEtaBin $pPtBin"

out_dir=bin_${pEtaBin}_${jEtaBin}_${pPtBin}
mkdir -p $out_dir
sh ../step2bak.makehisto/run.runall.sh $out_dir $pEtaBin $jEtaBin $pPtLow $pPtHigh
sh ../step2bak.fit/run.WP.runall.sh $out_dir
}



#python3 GetWPeff.py  2022EE 210 230 250 300 400 500 600 1000 1500 &
eff_file=WPeff_2022GJetMadgraph.root

for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtBin=$(( $idx - 1 ))
    pPtL=${pPtRange[$idx-1]}
    pPtR=${pPtRange[$idx]}
    #estimate_from_data $pEtaBin $jEtaBin $pPtBin $pPtL $pPtR
    estimate_from_data $pEtaBin $jEtaBin $pPtBin $pPtL $pPtR &
    bkgjob_submit_with_limitation_Nminus3.sh
done; done; done
wait



merged_info_csv=merged_fitinfo.csv
if [ -f "$merged_info_csv" ]; then /bin/rm $merged_info_csv; fi

for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtBin=$(( $idx - 1 ))
    out_dir=bin_${pEtaBin}_${jEtaBin}_${pPtBin}
python3 merge_fitinfo.py $pEtaBin $jEtaBin $pPtBin \
    $out_dir/fitinfo_WP0.yaml \
    $out_dir/fitinfo_WPc.yaml \
    $out_dir/fitinfo_WPb.yaml
done; done; done

python3 calculate_xs.py 2022EE $eff_file $merged_info_csv
#python3 collect_fitinfo.py  $out_dir/fitinfo_gjet_inclusive.yaml $total_fitinfo_gjet_fitting 2022EE $pEtaBin $jEtaBin $pPtL $pPtR | tee ${total_fitinfo_gjet_fitting}.collect_fitinfo.log
