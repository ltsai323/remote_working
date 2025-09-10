function run() { tag=$1; make -j8 -f ../ttt/makefile_${tag} massiverun; oDIR=/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/$tag; mkdir -p $oDIR ; mv outfile_*.root $oDIR; }
time run G4JetsMadgraph_100to200 
time run G4JetsMadgraph_200to400 
time run G4JetsMadgraph_400to600 
time run G4JetsMadgraph_40to70   
time run G4JetsMadgraph_600toinf 
time run G4JetsMadgraph_70to100  
time run GJetPythiaFlat          
