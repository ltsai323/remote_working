# used for re run step9
aa=WPcutWPbLoose_pull0_2fit_psuedodata_GJetPythia1_new ; for bin_dir in `ls $aa |GREP binned`; do mv $aa/$bin_dir . ; make -f makefile.2fits_btagcut_psuedodata check9_checktruth  oDIR=$bin_dir iYAMLcvsb=source.btag_psuedofit_cvsb.yaml ; mv $bin_dir $aa/; done
