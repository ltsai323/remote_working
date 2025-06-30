#!/usr/bin/env sh

function runBinnedPsuedodata() {
    outTAG=$1
    folder=$2
ii=1
sed "s/_0$/_$ii/g" test.btag_psuedofit_cvsb.yaml > source.btag_psuedofit_cvsb.yaml
sed "s/_0$/_$ii/g" test.btag_psuedofit_cvsl.yaml > source.btag_psuedofit_cvsl.yaml
sed "s/_0$/_$ii/g" test.btag_psuedofit_btag.yaml > source.btag_psuedofit_btag.yaml


out_dir=${outTAG}_3fit_psuedodata_GJetPythia1
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true
make -j8 -f makefile.runbinned  allbinning  \
    singleMAKEFILE=makefile.3fits_btagcut_psuedodata \
    binningFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLcvsb=source.btag_psuedofit_cvsb.yaml \
    iYAMLcvsl=source.btag_psuedofit_cvsl.yaml \
    iYAMLbtag=source.btag_psuedofit_btag.yaml
}

#runBinnedPsuedodata WPcutallgjets  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_binned_ctagfit
#runBinnedPsuedodata WPcutWPbLoose  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit
#runBinnedPsuedodata WPcutWPbMedium  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbMedium_binned_ctagfit





function runBinnedData() {
    outTAG=$1
    folder=$2


out_dir=${outTAG}_3fit_data
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true
make -j8 -f makefile.runbinned  allbinning_data  \
    singleMAKEFILE=makefile.3fits_btagcut_data \
    binningFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLBDT=test.btag_data_BDTAll.yaml \
    iYAMLcvsb=test.btag_data_cvsb.yaml \
    iYAMLcvsl=test.btag_data_cvsl.yaml \
    iYAMLbtag=test.btag_data_btag.yaml
}


#runBinnedData data_WPcutWPbLoose   /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbLoose_binned_ctagfit_data
#runBinnedData data_WPcutWPbMedium  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbMedium_binned_ctagfit_data
#runBinnedData data_WPcutWPbTight   /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPbTight_binned_ctagfit_data
#runBinnedData data_WPcutWPcLoose   /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcLoose_binned_ctagfit_data
#runBinnedData data_WPcutWPcMedium  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcMedium_binned_ctagfit_data
#runBinnedData data_WPcutWPcTight   /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_WPcTight_binned_ctagfit_data
runBinnedData data_allgjets        /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_binned_ctagfit_data

