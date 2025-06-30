theROOT=/afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled.root
function linkroot() { /bin/rm -f $theROOT; ln -s $1 $theROOT; }
function runall() {
    ii=$1

sed "s/_0$/_$ii/g" test.psuedofit_btag.yaml > source.psuedofit_btag.yaml
sed "s/_0$/_$ii/g" test.psuedofit_cvsb.yaml > source.psuedofit_cvsb.yaml
sed "s/_0$/_$ii/g" test.psuedofit_cvsl.yaml > source.psuedofit_cvsl.yaml
sed "s/_0$/_$ii/g" test.psuedofit_BDTAll.yaml > source.psuedofit_BDTAll.yaml

make all oDIR=psuedodata_GJetPythiaFlat_$ii/ iYAMLbtag=source.psuedofit_btag.yaml iYAMLcvsb=source.psuedofit_cvsb.yaml iYAMLcvsl=source.psuedofit_cvsl.yaml iYAMLBDT=source.psuedofit_BDTAll.yaml > log_full_$ii
mv log_full_$ii psuedodata_GJetPythiaFlat_$ii/
}





runall 0
runall 1
runall 2
runall 3
runall 4

out_folder=PsuedoDataFit
mkdir $out_folder; mv psuedodata_* $out_folder
