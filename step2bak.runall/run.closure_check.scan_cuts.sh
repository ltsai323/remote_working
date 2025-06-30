#!/usr/bin/env sh
outFOLDER=${1:-runresult}
pPtBinning3=( 210 230 250 300 400 500 600 1000 1500 )
#pPtBinning3=( 210 230 )

pPtRange=("${pPtBinning3[@]}")
#eff_file=WPeff_2022GJetPythiaFlat.root
eff_file=WPeff_2022GJetMadgraph.root

function the_exit() { echo "ERROR - "$1; exit 1; }



function scanning() {
WPc=$1
WPb=$2

merged_info_csv=fake_merged_fitinfo.csv
if [ -f "$merged_info_csv" ]; then /bin/rm $merged_info_csv; fi
merged_info_truth_csv=fake_merged_truthinfo.csv
if [ -f "$merged_info_truth_csv" ]; then /bin/rm $merged_info_truth_csv; fi

for pEtaBin in 0 1; do
    for jEtaBin in 0 1; do
        for (( idx=1; idx<${#pPtRange[@]}; idx++)); do
    pPtBin=$(( $idx - 1 ))
    out_dir=closure_check.result_WPcM_WPbL/bin_${pEtaBin}_${jEtaBin}_${pPtBin}
    python3 closure_check.export_estimation.py $out_dir/out_makehisto.root $pEtaBin $jEtaBin $pPtBin $merged_info_csv $merged_info_truth_csv $WPc $WPb || the_exit "abort scanning"
    bkgjob_submit_with_limitation_Nminus3.sh
done; done; done
wait


calculated_xs_csv='calculated_xs.csv'
python3 calculate_xs.scan.py 2022EE $eff_file $merged_info_csv $WPc $WPb || the_exit "not able to calculate xs"
python3 closure_check.2_truthcheck.py $calculated_xs_csv $merged_info_truth_csv ${pPtRange[@]} || the_exit "closure check error"

outdir=scanres_${WPc}_${WPb}
touch $outdir ; /bin/rm -rf $outdir
mkdir $outdir
mv $merged_info_csv $outdir
mv $merged_info_truth_csv $outdir
mv $calculated_xs_csv $outdir
mv closure_check.2_truthcheck.root $outdir
}

scanning WPcL WPbL
scanning WPcL WPbM
scanning WPcL WPbT

scanning WPcM WPbL
scanning WPcM WPbM
scanning WPcM WPbT

scanning WPcT WPbL
scanning WPcT WPbM
scanning WPcT WPbT


## tar -cf scanres.tar scanres_*
echo output scanres.tar
