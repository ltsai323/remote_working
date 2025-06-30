#!/usr/bin/env sh
outFOLDER=${1:-runresult}
pPtBinning3=( 210 230 250 300 400 500 600 1000 1500 )
#pPtBinning3=( 210 230 250 )

pPtRange=("${pPtBinning3[@]}")

function estimate_from_psuedodata() {
pEtaBin=$1
jEtaBin=$2
pPtBin=$3
pPtLow=$4
pPtHigh=$5
echo "[Running] estimate_from_data $pEtaBin $jEtaBin $pPtBin"

out_dir=bin_${pEtaBin}_${jEtaBin}_${pPtBin}
mkdir -p $out_dir
sh ../step2bak.makehisto/run.closure_check.sh $out_dir $pEtaBin $jEtaBin $pPtLow $pPtHigh
}



echo python3 GetWPeff.py  2022EE ${pPtRange[@]}
     python3 GetWPeff.py  2022EE ${pPtRange[@]}
eff_file=WPeff_2022GJetPythiaFlat.root

for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtBin=$(( $idx - 1 ))
    pPtL=${pPtRange[$idx-1]}
    pPtR=${pPtRange[$idx]}
    #estimate_from_data $pEtaBin $jEtaBin $pPtBin $pPtL $pPtR
    #estimate_from_psuedodata $pEtaBin $jEtaBin $pPtBin $pPtL $pPtR &
    #bkgjob_submit_with_limitation_Nminus3.sh
    estimate_from_psuedodata $pEtaBin $jEtaBin $pPtBin $pPtL $pPtR
done; done; done
wait



merged_info_csv=fake_merged_fitinfo.csv
if [ -f "$merged_info_csv" ]; then /bin/rm $merged_info_csv; fi
merged_info_truth_csv=fake_merged_truthinfo.csv
if [ -f "$merged_info_truth_csv" ]; then /bin/rm $merged_info_truth_csv; fi

for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtBin=$(( $idx - 1 ))
    out_dir=bin_${pEtaBin}_${jEtaBin}_${pPtBin}
    python3 closure_check.export_estimation.py $out_dir/out_makehisto.root $pEtaBin $jEtaBin $pPtBin $merged_info_csv $merged_info_truth_csv
done; done; done

calculated_xs_csv='calculated_xs.csv'
python3 calculate_xs.py 2022EE $eff_file $merged_info_csv
python3 closure_check.2_truthcheck.py $calculated_xs_csv $merged_info_truth_csv ${pPtRange[@]}
