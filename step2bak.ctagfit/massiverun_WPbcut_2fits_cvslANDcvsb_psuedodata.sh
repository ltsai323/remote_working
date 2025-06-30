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
    iYAMLcvsl=source.btag_psuedofit_cvsl.yaml \
    iYAMLbtag=hjalskdfjaslkdf
}

#runAllWPcut WPcutallgjets  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_binned_ctagfit
runAllWPcut WPcutWPcTight  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcTight_binned_ctagfit
#runAllWPcut WPcutWPcMedium /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcMedium_binned_ctagfit
#runAllWPcut WPcutWPcLoose  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcLoose_binned_ctagfit
#runAllWPcut WPcutWPbTight  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbTight_binned_ctagfit
#runAllWPcut WPcutWPbMedium /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbMedium_binned_ctagfit
#runAllWPcut WPcutWPbLoose  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit
