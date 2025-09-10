#!/usr/bin/env sh
function runBinnedCMD() {
    outDIR=$1
    folder=$2
    runCMD=$3 # allbinning_psuedodata allbinning_data
    iYAMLbtag=$4
    iYAMLcvsb=$5
    iYAMLcvsl=$6
    iYAMLBDT=$7
    binningFILELIST=$8
    echo runcmd is $runCMD
    echo filelist is $8

make -f makefile.runbinned  cleanworkspace oDIR=$outDIR forcerun=true


#make -f makefile.runbinned  merge_binning_comparetruth_LCB binningDIR=$outDIR \
make -j8 -f makefile.runbinned  $runCMD \
    singleMAKEFILE=makefile.3fits \
    sourceFOLDER=$folder \
    oDIR=$outDIR \
    iYAMLcvsb=$iYAMLcvsb \
    iYAMLcvsl=$iYAMLcvsl \
    iYAMLbtag=$iYAMLbtag \
    iYAMLBDT=$iYAMLBDT \
    BINNING_FILELIST="$binningFILELIST" \
    BINNING_FILELIST_DATA="$binningFILELIST"
}
function runBinnedPsuedodata_origweight() {
    outTAG=$1
    folder=$2
    out_dir=${outTAG}_3fit_psuedodata_origweight
    runBinnedCMD $out_dir $folder allbinning_psuedodata \
        test.btag_numLconstraint.psuedodata.origweight.yaml \
        test.cvsb_numLconstraint.psuedodata.origweight.yaml \
        test.cvsl_numLconstraint.psuedodata.origweight.yaml \
        "nothing" \
        "
makehisto_binned_ctagfit_psuedodata__0_0_1000_1500.root \
makehisto_binned_ctagfit_psuedodata__0_0_210_230.root \
makehisto_binned_ctagfit_psuedodata__0_0_230_250.root \
makehisto_binned_ctagfit_psuedodata__0_0_250_300.root \
makehisto_binned_ctagfit_psuedodata__0_0_300_400.root \
makehisto_binned_ctagfit_psuedodata__0_0_400_500.root \
makehisto_binned_ctagfit_psuedodata__0_0_500_600.root \
makehisto_binned_ctagfit_psuedodata__0_0_600_800.root \
makehisto_binned_ctagfit_psuedodata__0_1_210_230.root \
makehisto_binned_ctagfit_psuedodata__0_1_230_250.root \
makehisto_binned_ctagfit_psuedodata__0_1_250_300.root \
makehisto_binned_ctagfit_psuedodata__0_1_300_400.root \
makehisto_binned_ctagfit_psuedodata__0_1_400_500.root \
makehisto_binned_ctagfit_psuedodata__0_1_500_600.root \
makehisto_binned_ctagfit_psuedodata__0_1_600_800.root \
makehisto_binned_ctagfit_psuedodata__1_0_210_230.root \
makehisto_binned_ctagfit_psuedodata__1_0_230_250.root \
makehisto_binned_ctagfit_psuedodata__1_0_250_300.root \
makehisto_binned_ctagfit_psuedodata__1_0_300_400.root \
makehisto_binned_ctagfit_psuedodata__1_0_400_500.root \
makehisto_binned_ctagfit_psuedodata__1_0_500_600.root \
makehisto_binned_ctagfit_psuedodata__1_0_600_800.root \
makehisto_binned_ctagfit_psuedodata__1_1_210_230.root \
makehisto_binned_ctagfit_psuedodata__1_1_230_250.root \
makehisto_binned_ctagfit_psuedodata__1_1_250_300.root \
makehisto_binned_ctagfit_psuedodata__1_1_300_400.root \
makehisto_binned_ctagfit_psuedodata__1_1_400_500.root \
makehisto_binned_ctagfit_psuedodata__1_1_500_600.root \
makehisto_binned_ctagfit_psuedodata__1_1_600_800.root"
}
function runBinnedPsuedodata() {
    outTAG=$1
    folder=$2
    out_dir=${outTAG}_3fit_psuedodata
    runBinnedCMD $out_dir $folder allbinning_psuedodata \
        test.btag_numLconstraint.psuedodata.yaml \
        test.cvsb_numLconstraint.psuedodata.yaml \
        test.cvsl_numLconstraint.psuedodata.yaml \
        "nothing" \
        "
makehisto_binned_ctagfit_psuedodata__0_0_1000_1500.root \
makehisto_binned_ctagfit_psuedodata__0_0_210_230.root \
makehisto_binned_ctagfit_psuedodata__0_0_230_250.root \
makehisto_binned_ctagfit_psuedodata__0_0_250_300.root \
makehisto_binned_ctagfit_psuedodata__0_0_300_400.root \
makehisto_binned_ctagfit_psuedodata__0_0_400_500.root \
makehisto_binned_ctagfit_psuedodata__0_0_500_600.root \
makehisto_binned_ctagfit_psuedodata__0_0_600_800.root \
makehisto_binned_ctagfit_psuedodata__0_0_800_1000.root \
makehisto_binned_ctagfit_psuedodata__0_1_210_230.root \
makehisto_binned_ctagfit_psuedodata__0_1_230_250.root \
makehisto_binned_ctagfit_psuedodata__0_1_250_300.root \
makehisto_binned_ctagfit_psuedodata__0_1_300_400.root \
makehisto_binned_ctagfit_psuedodata__0_1_400_500.root \
makehisto_binned_ctagfit_psuedodata__0_1_500_600.root \
makehisto_binned_ctagfit_psuedodata__0_1_600_800.root \
makehisto_binned_ctagfit_psuedodata__1_0_210_230.root \
makehisto_binned_ctagfit_psuedodata__1_0_230_250.root \
makehisto_binned_ctagfit_psuedodata__1_0_250_300.root \
makehisto_binned_ctagfit_psuedodata__1_0_300_400.root \
makehisto_binned_ctagfit_psuedodata__1_0_400_500.root \
makehisto_binned_ctagfit_psuedodata__1_0_500_600.root \
makehisto_binned_ctagfit_psuedodata__1_0_600_800.root \
makehisto_binned_ctagfit_psuedodata__1_1_210_230.root \
makehisto_binned_ctagfit_psuedodata__1_1_230_250.root \
makehisto_binned_ctagfit_psuedodata__1_1_250_300.root \
makehisto_binned_ctagfit_psuedodata__1_1_300_400.root \
makehisto_binned_ctagfit_psuedodata__1_1_400_500.root \
makehisto_binned_ctagfit_psuedodata__1_1_500_600.root \
makehisto_binned_ctagfit_psuedodata__1_1_600_800.root \
"
}
function runBinneddata() {
    outTAG=$1
    folder=$2
    out_dir=${outTAG}_3fit_data
    runBinnedCMD $out_dir $folder allbinning_data \
        test.btag_numLconstraint.data.yaml \
        test.cvsb_numLconstraint.data.yaml \
        test.cvsl_numLconstraint.data.yaml \
        test.BDTAll_numLconstraint.data.yaml \
        " \
makehisto_binned_ctagfit_data__0_0_1000_1500.root \
makehisto_binned_ctagfit_data__0_0_210_230.root \
makehisto_binned_ctagfit_data__0_0_230_250.root \
makehisto_binned_ctagfit_data__0_0_250_300.root \
makehisto_binned_ctagfit_data__0_0_300_400.root \
makehisto_binned_ctagfit_data__0_0_400_500.root \
makehisto_binned_ctagfit_data__0_0_500_600.root \
makehisto_binned_ctagfit_data__0_0_600_800.root \
makehisto_binned_ctagfit_data__0_0_800_1000.root \
makehisto_binned_ctagfit_data__0_1_210_230.root \
makehisto_binned_ctagfit_data__0_1_230_250.root \
makehisto_binned_ctagfit_data__0_1_250_300.root \
makehisto_binned_ctagfit_data__0_1_300_400.root \
makehisto_binned_ctagfit_data__0_1_400_500.root \
makehisto_binned_ctagfit_data__0_1_500_600.root \
makehisto_binned_ctagfit_data__0_1_600_800.root \
makehisto_binned_ctagfit_data__0_1_800_1000.root \
makehisto_binned_ctagfit_data__1_0_210_230.root \
makehisto_binned_ctagfit_data__1_0_230_250.root \
makehisto_binned_ctagfit_data__1_0_250_300.root \
makehisto_binned_ctagfit_data__1_0_300_400.root \
makehisto_binned_ctagfit_data__1_0_400_500.root \
makehisto_binned_ctagfit_data__1_0_500_600.root \
makehisto_binned_ctagfit_data__1_0_600_800.root \
makehisto_binned_ctagfit_data__1_0_800_1000.root \
makehisto_binned_ctagfit_data__1_1_210_230.root \
makehisto_binned_ctagfit_data__1_1_230_250.root \
makehisto_binned_ctagfit_data__1_1_250_300.root \
makehisto_binned_ctagfit_data__1_1_300_400.root \
makehisto_binned_ctagfit_data__1_1_400_500.root \
makehisto_binned_ctagfit_data__1_1_500_600.root \
makehisto_binned_ctagfit_data__1_1_600_800.root"
}


function runBinnedPsuedodata_numLConstraint() {
    outTAG=$1
    folder=$2

out_dir=${outTAG}_3fit_psuedodata_GJetPythia1
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true


make -j8 -f makefile.runbinned  allbinning_psuedodata \
    singleMAKEFILE=makefile.3fits \
    sourceFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLcvsb=test.cvsb_numLconstraint.psuedodata.yaml \
    iYAMLcvsl=test.cvsl_numLconstraint.psuedodata.yaml \
    iYAMLbtag=test.btag_numLconstraint.psuedodata.yaml \
    BINNING_FILELIST="
makehisto_binned_ctagfit_psuedodata__0_0_1000_1500.root \
makehisto_binned_ctagfit_psuedodata__0_0_210_230.root \
makehisto_binned_ctagfit_psuedodata__0_0_230_250.root \
makehisto_binned_ctagfit_psuedodata__0_0_250_300.root \
makehisto_binned_ctagfit_psuedodata__0_0_300_400.root \
makehisto_binned_ctagfit_psuedodata__0_0_400_500.root \
makehisto_binned_ctagfit_psuedodata__0_0_500_600.root \
makehisto_binned_ctagfit_psuedodata__0_0_600_800.root \
makehisto_binned_ctagfit_psuedodata__0_0_800_1000.root \
makehisto_binned_ctagfit_psuedodata__0_1_1000_1500.root \
makehisto_binned_ctagfit_psuedodata__0_1_210_230.root \
makehisto_binned_ctagfit_psuedodata__0_1_230_250.root \
makehisto_binned_ctagfit_psuedodata__0_1_250_300.root \
makehisto_binned_ctagfit_psuedodata__0_1_300_400.root \
makehisto_binned_ctagfit_psuedodata__0_1_400_500.root \
makehisto_binned_ctagfit_psuedodata__0_1_500_600.root \
makehisto_binned_ctagfit_psuedodata__0_1_600_800.root \
makehisto_binned_ctagfit_psuedodata__0_1_800_1000.root \
makehisto_binned_ctagfit_psuedodata__1_0_1000_1500.root \
makehisto_binned_ctagfit_psuedodata__1_0_210_230.root \
makehisto_binned_ctagfit_psuedodata__1_0_230_250.root \
makehisto_binned_ctagfit_psuedodata__1_0_250_300.root \
makehisto_binned_ctagfit_psuedodata__1_0_300_400.root \
makehisto_binned_ctagfit_psuedodata__1_0_400_500.root \
makehisto_binned_ctagfit_psuedodata__1_0_500_600.root \
makehisto_binned_ctagfit_psuedodata__1_0_600_800.root \
makehisto_binned_ctagfit_psuedodata__1_0_800_1000.root \
makehisto_binned_ctagfit_psuedodata__1_1_1000_1500.root \
makehisto_binned_ctagfit_psuedodata__1_1_210_230.root \
makehisto_binned_ctagfit_psuedodata__1_1_230_250.root \
makehisto_binned_ctagfit_psuedodata__1_1_250_300.root \
makehisto_binned_ctagfit_psuedodata__1_1_300_400.root \
makehisto_binned_ctagfit_psuedodata__1_1_400_500.root \
makehisto_binned_ctagfit_psuedodata__1_1_500_600.root \
makehisto_binned_ctagfit_psuedodata__1_1_600_800.root \
makehisto_binned_ctagfit_psuedodata__1_1_800_1000.root"

}




function runBinnedData() {
    outTAG=$1
    folder=$2


out_dir=${outTAG}_3fit_data
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true
make -j8 -f makefile.runbinned  allbinning_data  \
    singleMAKEFILE=makefile.3fits \
    sourceFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLBDT=test.BDTAll_numLconstraint.data.yaml \
    iYAMLcvsb=test.cvsb_numLconstraint.data.yaml \
    iYAMLcvsl=test.cvsl_numLconstraint.data.yaml \
    iYAMLbtag=test.btag_numLconstraint.data.yaml \
    BINNING_FILELIST_DATA="
makehisto_binned_ctagfit_data__0_0_1000_1500.root \
makehisto_binned_ctagfit_data__0_0_210_230.root \
makehisto_binned_ctagfit_data__0_0_230_250.root \
makehisto_binned_ctagfit_data__0_0_250_300.root \
makehisto_binned_ctagfit_data__0_0_300_400.root \
makehisto_binned_ctagfit_data__0_0_400_500.root \
makehisto_binned_ctagfit_data__0_0_500_600.root \
makehisto_binned_ctagfit_data__0_0_600_800.root \
makehisto_binned_ctagfit_data__0_0_800_1000.root \
makehisto_binned_ctagfit_data__0_1_210_230.root \
makehisto_binned_ctagfit_data__0_1_230_250.root \
makehisto_binned_ctagfit_data__0_1_250_300.root \
makehisto_binned_ctagfit_data__0_1_300_400.root \
makehisto_binned_ctagfit_data__0_1_400_500.root \
makehisto_binned_ctagfit_data__0_1_500_600.root \
makehisto_binned_ctagfit_data__0_1_600_800.root \
makehisto_binned_ctagfit_data__0_1_800_1000.root \
makehisto_binned_ctagfit_data__1_0_210_230.root \
makehisto_binned_ctagfit_data__1_0_230_250.root \
makehisto_binned_ctagfit_data__1_0_250_300.root \
makehisto_binned_ctagfit_data__1_0_300_400.root \
makehisto_binned_ctagfit_data__1_0_400_500.root \
makehisto_binned_ctagfit_data__1_0_500_600.root \
makehisto_binned_ctagfit_data__1_0_600_800.root \
makehisto_binned_ctagfit_data__1_0_800_1000.root \
makehisto_binned_ctagfit_data__1_1_210_230.root \
makehisto_binned_ctagfit_data__1_1_230_250.root \
makehisto_binned_ctagfit_data__1_1_250_300.root \
makehisto_binned_ctagfit_data__1_1_300_400.root \
makehisto_binned_ctagfit_data__1_1_400_500.root \
makehisto_binned_ctagfit_data__1_1_500_600.root \
makehisto_binned_ctagfit_data__1_1_600_800.root"
#    BINNING_FILELIST_DATA="
#makehisto_binned_ctagfit_data__0_0_1000_1500.root \
#makehisto_binned_ctagfit_data__0_0_210_230.root \
#makehisto_binned_ctagfit_data__0_0_230_250.root \
#makehisto_binned_ctagfit_data__0_0_250_300.root \
#makehisto_binned_ctagfit_data__0_0_300_400.root \
#makehisto_binned_ctagfit_data__0_0_400_500.root \
#makehisto_binned_ctagfit_data__0_0_500_600.root \
#makehisto_binned_ctagfit_data__0_0_600_800.root \
#makehisto_binned_ctagfit_data__0_0_800_1000.root \
#makehisto_binned_ctagfit_data__0_1_1000_1500.root \
#makehisto_binned_ctagfit_data__0_1_210_230.root \
#makehisto_binned_ctagfit_data__0_1_230_250.root \
#makehisto_binned_ctagfit_data__0_1_250_300.root \
#makehisto_binned_ctagfit_data__0_1_300_400.root \
#makehisto_binned_ctagfit_data__0_1_400_500.root \
#makehisto_binned_ctagfit_data__0_1_500_600.root \
#makehisto_binned_ctagfit_data__0_1_600_800.root \
#makehisto_binned_ctagfit_data__0_1_800_1000.root \
#makehisto_binned_ctagfit_data__1_0_1000_1500.root \
#makehisto_binned_ctagfit_data__1_0_210_230.root \
#makehisto_binned_ctagfit_data__1_0_230_250.root \
#makehisto_binned_ctagfit_data__1_0_250_300.root \
#makehisto_binned_ctagfit_data__1_0_300_400.root \
#makehisto_binned_ctagfit_data__1_0_400_500.root \
#makehisto_binned_ctagfit_data__1_0_500_600.root \
#makehisto_binned_ctagfit_data__1_0_600_800.root \
#makehisto_binned_ctagfit_data__1_0_800_1000.root \
#makehisto_binned_ctagfit_data__1_1_1000_1500.root \
#makehisto_binned_ctagfit_data__1_1_210_230.root \
#makehisto_binned_ctagfit_data__1_1_230_250.root \
#makehisto_binned_ctagfit_data__1_1_250_300.root \
#makehisto_binned_ctagfit_data__1_1_300_400.root \
#makehisto_binned_ctagfit_data__1_1_400_500.root \
#makehisto_binned_ctagfit_data__1_1_500_600.root \
#makehisto_binned_ctagfit_data__1_1_600_800.root \
#makehisto_binned_ctagfit_data__1_1_800_1000.root"
}


# runBinnedData data_allgjets_40bins_saikatGJetBinging_sigGJetPythiaFlat_numLconstraint  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_ctagfit_sigGJetPythiaFlat_data
#runBinnedData testingjetNOREWEIGHT_data_allgjets_saikatGJetBinning_sigGJetPythiaFlat_3fit__40bins  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist40bins_2dhist6variantbin_ctagfit_sigGJetPythiaFlat_data__

#runBinnedPsuedodata               phojetnjetREWEIGHT_allgjets_saikatGJetBinning_sigGJetPythiaFlat__40bins  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist40bins_2dhist6variantbin_ctagfit_sigGJetPythiaFlat_psuedodata__2_3Dreweight
runBinnedPsuedodata_origweight    phojetnjetREWEIGHT_allgjets_saikatGJetBinning_sigGJetPythiaFlat__40bins  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist40bins_2dhist6variantbin_ctagfit_sigGJetPythiaFlat_psuedodata__2_3Dreweight

#runBinnedPsuedodata               phojetnjetREWEIGHT_allgjets_saikatGJetBinning_sigGJetPythiaFlat__15variantbins /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist15variantbins_2dhist6variantbin_ctagfit_sigGJetPythiaFlat_psuedodata__2_3Dreweight
runBinnedPsuedodata_origweight    phojetnjetREWEIGHT_allgjets_saikatGJetBinning_sigGJetPythiaFlat__15variantbins /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist15variantbins_2dhist6variantbin_ctagfit_sigGJetPythiaFlat_psuedodata__2_3Dreweight
