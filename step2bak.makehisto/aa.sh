### test command
#python3 makehisto_ctagging_effSF.py ## creating calibrated EFF.
#make -f makefile_binned_ctagfit  test
make -f makefile_binned_ctagfit -j4 test_nobinning_psuedodata0
#make -f makefile_binned_ctagfit step3_collect_binned_hists oDIR=test.onlyetabins.1D40binsAND2D10bins.GJetPythia.madgraphsig
make -f makefile_binned_ctagfit step3_collect_binned_hists oDIR=test.onlyetabins.passWPbM.1D60binsAND2D7vbins.GJetPythiaFlat.madgraphsig

#### full command
#python3 makehisto_ctagging_effSF.py ## creating calibrated EFF.
#make -j10 -f makefile_binned_ctagfit runpsuedodata oDIR=psuedodata.1D40binsAND2D10bins.GJetPythiaFlat.Madgraphsig


#make -j10 -f makefile_binned_ctagfit runpsuedodata oDIR=psuedodata.1D40binsAND2D10bins.GJetPythia.Madgraphsig
