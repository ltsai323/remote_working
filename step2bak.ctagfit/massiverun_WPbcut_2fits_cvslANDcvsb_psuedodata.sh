function runAllWPcut() {
    outTAG=$1
    folder=$2
ii=1
sed "s/_0$/_$ii/g" test.btag_psuedofit_cvsb.yaml > source.btag_psuedofit_cvsb.yaml
sed "s/_0$/_$ii/g" test.btag_psuedofit_cvsl.yaml > source.btag_psuedofit_cvsl.yaml


out_dir=${outTAG}_2fit_psuedodata_GJetPythia1
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true
make -j8 -f makefile.runbinned  allbinning  \
    singleMAKEFILE=makefile.2fits_btagcut_psuedodata \
    binningFOLDER=$folder \
    oDIR=${out_dir} \
    iYAMLcvsb=source.btag_psuedofit_cvsb.yaml \
    iYAMLcvsl=source.btag_psuedofit_cvsl.yaml
    #iYAMLcvsb=test.fixedfake_psuedofit_cvsb.yaml \
    #iYAMLcvsl=test.fixedfake_psuedofit_cvsl.yaml
}
function runBinnedData() {
    outTAG=$1
    folder=$2


out_dir=${outTAG}_2fit_data
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true
make -j8 -f makefile.runbinned  allbinning_data  \
    singleMAKEFILE=makefile.2fits_btagcut_data_ \
    binningFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLBDT=test.btag_data_BDTAll.yaml \
    iYAMLcvsb=test.btag_data_cvsb.yaml \
    iYAMLcvsl=test.btag_data_cvsl.yaml
}

#runAllWPcut WPcutallgjets  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_binned_ctagfit
#runAllWPcut WPcutWPcTight  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcTight_binned_ctagfit
#runAllWPcut WPcutWPcMedium /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcMedium_binned_ctagfit
#runAllWPcut WPcutWPcLoose  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcLoose_binned_ctagfit
#runAllWPcut WPcutWPbTight  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbTight_binned_ctagfit
#runAllWPcut WPcutWPbMedium /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbMedium_binned_ctagfit
#runAllWPcut WPcutWPbLoose  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit

#runBinnedData WPcutWPbMedium /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbMedium_binned_ctagfit_data/
#runBinnedData WPcutWPbLoose  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit_data/

#runAllWPcut WPcutWPbLoose_pull0  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_bin10_binned_ctagfit_generate_pull
runAllWPcut WPcutWPbLoose_40bins_numLconstraint  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit___
