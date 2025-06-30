theROOT=/afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled.root
function linkroot() { /bin/rm -f $theROOT; ln -s $1 $theROOT; }
function runall() {
    oTAG=$1
    inROOT=$2
    linkroot $inROOT

echo [RunAll] oTAG $1 inROOT $2
make all oDIR=psuedodata_GJetPythiaFlat/ iYAML=test.psuedofit.yaml > log_full
make all oDIR=psuedodata_pureLjet_GJetPythiaFlat iYAML=test.psuedofit_pureL.yaml > log_pureL
make all oDIR=psuedodata_pureCjet_GJetPythiaFlat iYAML=test.psuedofit_pureC.yaml > log_pureC
make all oDIR=psuedodata_pureBjet_GJetPythiaFlat iYAML=test.psuedofit_pureB.yaml > log_pureB
make collect_psuedofit_result_nonote outputFOLDER=$oTAG
}





#runall output_SV0to5All_flowbin           /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto5_flowbins.root
runall output_SV0to5All__highbin_flowbin  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto5_highbin_flowbins.root




#runall output_SV0to10All         /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto10.root 
#runall output_SV0to10All_highbin /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto10_highbin.root 
#runall output_SV0to15All         /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto15.root 
#runall output_SV0to15All_highbin /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto15_highbin.root 
#runall output_SV0to5All          /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto5.root 
#runall output_SV0to5All_highbin  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto5_highbin.root 
#runall output_SV0to8All          /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto8.root 
#runall output_SV0to8All_highbin  /afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.makehisto/makehisto_psuedodata_rescaled_SVto8_highbin.root 

out_folder=WPbLoose__
mkdir $out_folder; mv output_* $out_folder
