#make -j5 -f makefile_binned_ctagfit  test_nobinning_psuedodata
#make -f makefile_binned_ctagfit step3_collect_binned_hists oDIR=test.jetidx0.1D40binsAND2D10bins.GJetPythiaFlat.madgraphsig
make -j8 -f makefile_binned_ctagfit runpsuedodata oDIR=psuedodata.1D40binsAND2D10bins.GJetPythiaFlat.Madgraphsig
