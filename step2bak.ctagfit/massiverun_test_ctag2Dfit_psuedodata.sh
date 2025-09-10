#!/usr/bin/env sh

function runBinnedPsuedodata_numLConstraint() {
    outTAG=$1
    folder=$2

out_dir=${outTAG}_3fit_psuedodata_GJetPythia1
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true


make -j8 -f makefile.runbinned  allbinning \
    singleMAKEFILE=makefile.2Dfit \
    binningFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLctag=test.ctag.psuedodata.yaml \
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
function runBinnedPsuedodata() {
    outTAG=$1
    folder=$2

out_dir=${outTAG}_3fit_psuedodata_GJetPythia1
make -f makefile.runbinned  cleanworkspace oDIR=$out_dir forcerun=true


    singleMAKEFILE=makefile.3fits \
make -j8 -f makefile.runbinned  allbinning \
    singleMAKEFILE=makefile.3fits_btagcut_psuedodata \
    binningFOLDER=$folder \
    oDIR=$out_dir \
    iYAMLcvsb=test.cvsb.yaml \
    iYAMLcvsl=test.cvsl.yaml \
    iYAMLbtag=test.btag.yaml \
    BINNING_FILELIST="
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

#runBinnedPsuedodata_numLConstraint psuedo_allgjets_ctag2D10x10bin_saikatGJetBinning_psuedodataSelfToy_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_2dhistbin10_ctagfit_sigGJetPythiaFlat_psuedodata
#runBinnedPsuedodata_numLConstraint psuedo_allgjets_ctag2D5x5bin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_2dhistbin5_ctagfit_sigGJetPythiaFlat_psuedodata
#runBinnedPsuedodata_numLConstraint psuedo_allgjets_ctag2D20x20bin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_2dhistbin20_ctagfit_sigGJetPythiaFlat_psuedodata
# runBinnedData data_allgjets_40bins_saikatGJetBinging_sigGJetPythiaFlat_numLconstraint  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_ctagfit_sigGJetPythiaFlat_data


#runBinnedPsuedodata_numLConstraint psuedo_allgjets_ctag2D20x20bin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_2dhistbin20_ctagfit_sigGJetPythiaFlat_psuedodata
#runBinnedPsuedodata_numLConstraint psuedo_allgjets_ctag2D5x5bin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_2dhistbin5_ctagfit_sigGJetPythiaFlat_psuedodata


#runBinnedPsuedodata_numLConstraint testingjetREWEIGHT_psuedo_allgjets_ctag2D5x5bin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_testing
#runBinnedPsuedodata_numLConstraint testingjetREWEIGHT_psuedo_allgjets_ctag2D5x5bin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_histbin40_2dhistbin5_ctagfit_sigGJetPythiaFlat_psuedodata
#runBinnedPsuedodata_numLConstraint testingjetNOREWEIGHT_psuedo_allgjets_ctag2D15variantbin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist15variantbin_2dhist15variantbin_ctagfit_sigGJetPythiaFlat_psuedodata__noJetPtNJet_reweight
runBinnedPsuedodata_numLConstraint testingjetNOREWEIGHT_psuedo_allgjets_ctag2D6variantbin_saikatGJetBinning_psuedodataGJetMadgraph_sigGJetPythiaFlat /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_allgjets_saikatGJetBins_hist15variantbin_2dhist6variantbin_ctagfit_sigGJetPythiaFlat_psuedodata__noJetPtNJet_reweight

