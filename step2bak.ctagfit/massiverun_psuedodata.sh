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
function runWPcut() {
    inROOT=$1
    cc=${inROOT##*__}; dd=${cc%.*}
    binningSTR=$dd

    out_dir=binned_${binningSTR}


make all oDIR=$out_dir iYAMLbtag=test.psuedofit_btag.yaml iYAMLcvsb=test.psuedofit_cvsb.yaml iYAMLcvsl=test.psuedofit_cvsl.yaml rootMAKEHISTO=$inROOT > log_full_$binningSTR
mv log_full_$binningSTR $out_dir
}





#runall 0
#runall 1
#runall 2
#runall 3
#runall 4
#
#out_folder=PsuedoDataFit
#mkdir $out_folder; mv psuedodata_* $out_folder



runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_210_230.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_230_250.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_250_300.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_300_400.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_400_500.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_500_600.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_600_1000.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_0_1000_1500.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_210_230.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_230_250.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_250_300.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_300_400.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_400_500.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_500_600.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_600_1000.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__0_1_1000_1500.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_210_230.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_230_250.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_250_300.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_300_400.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_400_500.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_500_600.root
runWPcut /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit/makehisto_binned_ctagfit_psuedodata__1_0_600_1000.root

out_folder=WPbLoose_ctagfit_psueoddata_GJetPythia
mkdir $out_folder; mv binned_* $out_folder
