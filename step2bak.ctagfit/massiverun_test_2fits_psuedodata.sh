function runAllWPcut() {
    outTAG=$1
    folder=$2
ii=1

out_dir=${outTAG}_2fit_psuedodata_GJetPythia1
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true
make -j8 -f makefile.runbinned  allbinning  \
    singleMAKEFILE=makefile.2fits_btagcut_psuedodata \
    binningFOLDER=$folder \
    oDIR=${out_dir} \
    iYAMLcvsb=test.cvsb.yaml \
    iYAMLcvsl=test.cvsl.yaml \
    BINNING_FILELIST=" \
        makehisto_binned_ctagfit_psuedodata__0_0_210_230.root \
        makehisto_binned_ctagfit_psuedodata__0_0_230_250.root \
        makehisto_binned_ctagfit_psuedodata__0_0_250_300.root \
        makehisto_binned_ctagfit_psuedodata__0_0_300_400.root \
        makehisto_binned_ctagfit_psuedodata__0_0_400_500.root \
        makehisto_binned_ctagfit_psuedodata__0_0_500_800.root \
        makehisto_binned_ctagfit_psuedodata__0_0_800_1500.root \
        makehisto_binned_ctagfit_psuedodata__0_1_210_230.root \
        makehisto_binned_ctagfit_psuedodata__0_1_230_250.root \
        makehisto_binned_ctagfit_psuedodata__0_1_250_300.root \
        makehisto_binned_ctagfit_psuedodata__0_1_300_400.root \
        makehisto_binned_ctagfit_psuedodata__0_1_400_500.root \
        makehisto_binned_ctagfit_psuedodata__0_1_500_800.root \
        makehisto_binned_ctagfit_psuedodata__0_1_800_1500.root \
        makehisto_binned_ctagfit_psuedodata__1_0_210_230.root \
        makehisto_binned_ctagfit_psuedodata__1_0_230_250.root \
        makehisto_binned_ctagfit_psuedodata__1_0_250_300.root \
        makehisto_binned_ctagfit_psuedodata__1_0_300_400.root \
        makehisto_binned_ctagfit_psuedodata__1_0_400_500.root \
        makehisto_binned_ctagfit_psuedodata__1_0_500_800.root \
        makehisto_binned_ctagfit_psuedodata__1_0_800_1500.root \
        makehisto_binned_ctagfit_psuedodata__1_1_210_230.root \
        makehisto_binned_ctagfit_psuedodata__1_1_230_250.root \
        makehisto_binned_ctagfit_psuedodata__1_1_250_300.root \
        makehisto_binned_ctagfit_psuedodata__1_1_300_400.root \
        makehisto_binned_ctagfit_psuedodata__1_1_400_500.root \
        makehisto_binned_ctagfit_psuedodata__1_1_500_800.root \
        makehisto_binned_ctagfit_psuedodata__1_1_800_1500.root"
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
    iYAMLcvsl=test.btag_data_cvsl.yam
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
/bin/rm -f datacard_btag_psuedofit.template.txt; ln -s datacard_btag_psuedofit_numLconstraint.template.txt datacard_btag_psuedofit.template.txt
#runAllWPcut WPcutWPbLoose_testbinning_40bins_numLconstraint  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_testbinning_bin40_ctagfit_psuedodata
runAllWPcut WPcutWPbLoose_testbinning_40bins_numLconstraint_2fit_psuedodata_GJetPythia1  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_testbinning_bin40_ctagfit_psuedodata__psuedodataGJetMadgraph_sigGJetPythiaFlat
