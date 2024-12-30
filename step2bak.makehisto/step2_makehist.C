using RDF = ROOT::RDataFrame;

float signal_pho(float eta, float isovar)
{
    float abseta = fabs(eta);
    if ( abseta < 1.4442 ) if ( isovar < 2 ) return 1.;
    if ( abseta > 1.566 && abseta < 2.5 ) if ( isovar < 1.5 ) return 1.;
    return 0.;
}


ROOT::RDF::RNode CommonProcedures( RDF& f, int useHLT, int isMC, int isQCD )
{
    filterfunc::HLTOPTION = useHLT;
    filterfunc::IsMC = isMC;
    filterfunc::IsQCD = isQCD;
    filterfunc::ValidCheck();
    const char* photon_pt = filterfunc::IsMC ? "recoPt" : "recoPtCalib"; // only pt bin used calibrated pt in data
    const char* chargedIsolation = filterfunc::IsMC ? "chIsoRaw" : "calib_chIso";

    auto out = ROOT::RDF::RNode(f);
    out = out
        .Filter( filterfunc::basic_selection, {"recoSCEta","MET", photon_pt, "eleVeto"} )
        .Filter( filterfunc::fiducial_photon, {"recoSCEta", "sieieFull5x5", "HoverE"} )
        .Filter( filterfunc::PassJetAdditionalSelection,
                {"jetPt", "jetEta", "jetDeepCSVTags_c", "jetSubVtxMass", "jetDeepCSVDiscriminatorTags_CvsL"} );

    if ( filterfunc::IsMC == 1 && filterfunc::IsQCD == 1 )
        out = out .Define( "eventweight", "mcweight*puwei" );
    if ( filterfunc::IsMC == 1 && filterfunc::IsQCD != 1 )
        out = out .Define( "eventweight", "mcweight*puwei*weight_passMaxPUcut" );

    if ( filterfunc::IsQCD == 1 )
        out = out
            .Filter( filterfunc::PassJetAdditionalSelection_passPUcut, {"passMaxPUcut"} );
    if ( filterfunc::HLTOPTION == 1 )
        out = out
            .Filter( filterfunc::HLTPassed, {photon_pt, "phoFiredTrgs"} );

    if ( filterfunc::IsMC == 1 )
        out = out
            .Filter( filterfunc::PassJetAdditionalSelection_MC, {"jetID", "jetPUIDbit"} )
            .Define( "weight_btag_central"      , "eventweight*jetSF.DeepCSV.central")
            .Define( "weight_btag_up_lf"        , "eventweight*jetSF.DeepCSV.up_lf")
            .Define( "weight_btag_down_lf"      , "eventweight*jetSF.DeepCSV.down_lf")
            .Define( "weight_btag_up_cferr1"    , "eventweight*jetSF.DeepCSV.up_cferr1")
            .Define( "weight_btag_down_cferr1"  , "eventweight*jetSF.DeepCSV.down_cferr1")
            .Define( "weight_btag_up_hf"        , "eventweight*jetSF.DeepCSV.up_hf")
            .Define( "weight_btag_down_hf"      , "eventweight*jetSF.DeepCSV.down_hf")
            .Define( "isFakePho", filterfunc::IsFakePhoton, {"isMatched", "isConverted", "isMatchedEle"} );

    return out
        .Define( "phoptbin", filterfunc::Ptbin, {photon_pt} )
        .Define( "phoetabin", filterfunc::EBEE, {"recoEta"} )
        .Define( "jetetabin", filterfunc::JetEtaBin, {"jetPt", "jetY"} )
        .Define( "phoSignalRegion", filterfunc::PhoSignalRegion, {chargedIsolation, "recoEta"} )
        .Define( "phoDataSideband", filterfunc::PhoDataSideband, {chargedIsolation, "recoEta"} );
}
ROOT::RDF::RNode CommonProceduresData(RDF& f)
{ return CommonProcedures(f, 1, 0, 0); }
ROOT::RDF::RNode CommonProceduresSigMC(RDF& f)
{ return CommonProcedures(f, 0, 1, 0); }
ROOT::RDF::RNode CommonProceduresQCDMC(RDF& f)
{ return CommonProcedures(f, 1, 1, 1); }
    

void makehist_sig(ROOT::RDF::RNode& dataframe, TDirectory* dir)
{
    filterfunc::HLTOPTION = 0;
    filterfunc::IsMC = 1;
    filterfunc::IsQCD = 0;
    dir->cd();
    const char* photon_pt = filterfunc::IsMC ? "recoPt" : "recoPtCalib"; // only pt bin used calibrated pt in data
    const char* bdt_score = filterfunc::IsMC ? "calib_mva" : "mva";
    
    auto h00 = dataframe.Filter("phoSignalRegion == 1 && isFakePho != 1")
        .Histo1D<float>({"BDT_sig", "BDT", 10, -1.,1.}, bdt_score);
    auto h01 = dataframe.Filter("phoSignalRegion == 1 && isFakePho != 1")
        .Histo1D<float>({"BDT_sig_SScorrUp", "BDT data sideband", 10, -1.,1.}, "mva"); // original bdt score w/o SScorr
    
    /*
    auto h02 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag0_obs", "BvsAll", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_BvsAll");
    auto h03 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag0_background", "BvsAll data sideband", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_BvsAll");

    auto h04 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag1_background", "CvsL data sideband", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsL");
    auto h05 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag1_obs", "CvsL", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsL");

    auto h06 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag2_obs", "CvsB", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsB");
    auto h07 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag2_background", "CvsB data sideband", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsB");

    auto h08 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag3_background", "secVexMass data sideband", 100,0.,5.}, "jetSubVtxMass");
    auto h09 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag3_obs", "secVexMass", 100,0.,5.}, "jetSubVtxMass");
    */



    h00->Write();
    h01->Write();



    if (!filterfunc::checkplots ) return;
}
void makehist_exp(ROOT::RDF::RNode& dataframe, TDirectory* dir)
{
    filterfunc::HLTOPTION = 1;
    filterfunc::IsMC = 0;
    filterfunc::IsQCD = 0;
    dir->cd();
    const char* photon_pt = filterfunc::IsMC ? "recoPt" : "recoPtCalib"; // only pt bin used calibrated pt in data
    const char* bdt_score = filterfunc::IsMC ? "calib_mva" : "mva";
    
    auto h00 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"BDT_obs", "BDT", 10, -1.,1.}, bdt_score);
    auto h01 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"BDT_background", "BDT data sideband", 10, -1.,1.}, bdt_score);
    
    auto h02 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag0_obs", "BvsAll", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_BvsAll");
    auto h03 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag0_background", "BvsAll data sideband", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_BvsAll");

    auto h04 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag1_background", "CvsL data sideband", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsL");
    auto h05 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag1_obs", "CvsL", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsL");

    auto h06 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag2_obs", "CvsB", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsB");
    auto h07 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag2_background", "CvsB data sideband", 10,0.,1.}, "jetDeepCSVDiscriminatorTags_CvsB");

    auto h08 = dataframe.Filter("phoDataSideband == 1")
        .Histo1D<float>({"jettag3_background", "secVexMass data sideband", 100,0.,5.}, "jetSubVtxMass");
    auto h09 = dataframe.Filter("phoSignalRegion == 1")
        .Histo1D<float>({"jettag3_obs", "secVexMass", 100,0.,5.}, "jetSubVtxMass");



    h00->Write();
    h01->Write();
    h02->Write();
    h03->Write();
    h04->Write();
    h05->Write();
    h06->Write();
    h07->Write();
    h08->Write();
    h09->Write();

    if (!filterfunc::checkplots ) return;
}
void makehist_QCD(ROOT::RDF::RNode& dataframe, TDirectory* dir)
{
    filterfunc::HLTOPTION = 1;
    filterfunc::IsMC = 1;
    filterfunc::IsQCD = 1;
    dir->cd();
    const char* photon_pt = filterfunc::IsMC ? "recoPt" : "recoPtCalib"; // only pt bin used calibrated pt in data
    const char* bdt_score = filterfunc::IsMC ? "calib_mva" : "mva";

    if (!filterfunc::checkplots ) return;
    //////////////////////////////
    // jettag0 : BvsAll section //
    //////////////////////////////
    // L quark : jetHadFlvr==0
    auto h000 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetL_signalRegion"      , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_central");
    auto h001 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetL_signalRegionUp"    , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_up_lf");
    auto h002 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetL_signalRegionDown"  , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_down_lf");

    auto h003 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetL_sideband"          , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_central");
    auto h004 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetL_sidebandUp"        , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_up_lf");
    auto h005 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetL_sidebandDown"      , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_down_lf");
    // c quark : jetHadFlvr==4
    auto h006 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetC_signalRegion"      , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_central");
    auto h007 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetC_signalRegionUp"    , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_up_cferr1");
    auto h008 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetC_signalRegionDown"  , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_down_cferr1");

    auto h009 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetC_sideband"          , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_central");
    auto h010 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetC_sidebandUp"        , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_up_cferr1");
    auto h011 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetC_sidebandDown"      , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_down_cferr1");
    // b quark : jetHadFlvr==5
    auto h012 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetB_signalRegion"      , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_central");
    auto h013 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetB_signalRegionUp"    , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_up_hf");
    auto h014 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetB_signalRegionDown"  , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_down_hf");

    auto h015 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetB_sideband"          , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_central");
    auto h016 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetB_sidebandUp"        , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_up_hf");
    auto h017 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag0_DijetB_sidebandDown"      , "BvsAll", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_BvsAll", "weight_btag_down_hf");
    




    //////////////////////////////
    // jettag1 : CvsL   section //
    //////////////////////////////
    // L quark : jetHadFlvr==0
    auto h100 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetL_signalRegion"      , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_central");
    auto h101 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetL_signalRegionUp"    , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_up_lf");
    auto h102 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetL_signalRegionDown"  , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_down_lf");

    auto h103 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetL_sideband"          , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_central");
    auto h104 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetL_sidebandUp"        , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_up_lf");
    auto h105 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetL_sidebandDown"      , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_down_lf");
    // c quark : jetHadFlvr==4
    auto h106 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetC_signalRegion"      , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_central");
    auto h107 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetC_signalRegionUp"    , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_up_cferr1");
    auto h108 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetC_signalRegionDown"  , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_down_cferr1");

    auto h109 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetC_sideband"          , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_central");
    auto h110 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetC_sidebandUp"        , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_up_cferr1");
    auto h111 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetC_sidebandDown"      , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_down_cferr1");
    // b quark : jetHadFlvr==5
    auto h112 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetB_signalRegion"      , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_central");
    auto h113 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetB_signalRegionUp"    , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_up_hf");
    auto h114 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetB_signalRegionDown"  , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_down_hf");

    auto h115 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetB_sideband"          , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_central");
    auto h116 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetB_sidebandUp"        , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_up_hf");
    auto h117 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag1_DijetB_sidebandDown"      , "CvsL", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsL", "weight_btag_down_hf");
    




    //////////////////////////////
    // jettag2 : CvsB   section //
    //////////////////////////////
    // L quark : jetHadFlvr==0
    auto h200 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetL_signalRegion"      , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_central");
    auto h201 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetL_signalRegionUp"    , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_up_lf");
    auto h202 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetL_signalRegionDown"  , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_down_lf");

    auto h203 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetL_sideband"          , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_central");
    auto h204 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetL_sidebandUp"        , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_up_lf");
    auto h205 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetL_sidebandDown"      , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_down_lf");
    // c quark : jetHadFlvr==4
    auto h206 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetC_signalRegion"      , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_central");
    auto h207 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetC_signalRegionUp"    , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_up_cferr1");
    auto h208 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetC_signalRegionDown"  , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_down_cferr1");

    auto h209 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetC_sideband"          , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_central");
    auto h210 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetC_sidebandUp"        , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_up_cferr1");
    auto h211 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetC_sidebandDown"      , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_down_cferr1");
    // b quark : jetHadFlvr==5
    auto h212 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetB_signalRegion"      , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_central");
    auto h213 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetB_signalRegionUp"    , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_up_hf");
    auto h214 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetB_signalRegionDown"  , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_down_hf");

    auto h215 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetB_sideband"          , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_central");
    auto h216 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetB_sidebandUp"        , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_up_hf");
    auto h217 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag2_DijetB_sidebandDown"      , "CvsB", 10,0.,1.},
                "jetDeepCSVDiscriminatorTags_CvsB", "weight_btag_down_hf");
    




    //////////////////////////////
    // jettag3 : secVtx section //
    //////////////////////////////
    // L quark : jetHadFlvr==0
    auto h300 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetL_signalRegion"      , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_central");
    auto h301 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetL_signalRegionUp"    , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_up_lf");
    auto h302 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetL_signalRegionDown"  , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_down_lf");

    auto h303 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetL_sideband"          , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_central");
    auto h304 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetL_sidebandUp"        , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_up_lf");
    auto h305 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==0 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetL_sidebandDown"      , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_down_lf");
    // c quark : jetHadFlvr==4
    auto h306 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetC_signalRegion"      , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_central");
    auto h307 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetC_signalRegionUp"    , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_up_cferr1");
    auto h308 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetC_signalRegionDown"  , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_down_cferr1");

    auto h309 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetC_sideband"          , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_central");
    auto h310 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetC_sidebandUp"        , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_up_cferr1");
    auto h311 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==4 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetC_sidebandDown"      , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_down_cferr1");
    // b quark : jetHadFlvr==5
    auto h312 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetB_signalRegion"      , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_central");
    auto h313 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetB_signalRegionUp"    , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_up_hf");
    auto h314 = dataframe.Filter("phoSignalRegion == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetB_signalRegionDown"  , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_down_hf");

    auto h315 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetB_sideband"          , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_central");
    auto h316 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetB_sidebandUp"        , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_up_hf");
    auto h317 = dataframe.Filter("phoDataSideband == 1 && jetHadFlvr==5 && isFakePho==1")
        .Histo1D<float>({"jettag3_DijetB_sidebandDown"      , "secVtxMass", 10,0.,1.},
                "jetSubVtxMass", "weight_btag_down_hf");
    
    h000->Write();
    h001->Write();
    h002->Write();
    h003->Write();
    h004->Write();
    h005->Write();
    h006->Write();
    h007->Write();
    h008->Write();
    h009->Write();
    h010->Write();
    h011->Write();
    h012->Write();
    h013->Write();
    h014->Write();
    h015->Write();
    h016->Write();
    h017->Write();
    
    h100->Write();
    h101->Write();
    h102->Write();
    h103->Write();
    h104->Write();
    h105->Write();
    h106->Write();
    h107->Write();
    h108->Write();
    h109->Write();
    h110->Write();
    h111->Write();
    h112->Write();
    h113->Write();
    h114->Write();
    h115->Write();
    h116->Write();
    h117->Write();
    
    h200->Write();
    h201->Write();
    h202->Write();
    h203->Write();
    h204->Write();
    h205->Write();
    h206->Write();
    h207->Write();
    h208->Write();
    h209->Write();
    h210->Write();
    h211->Write();
    h212->Write();
    h213->Write();
    h214->Write();
    h215->Write();
    h216->Write();
    h217->Write();
    
    h300->Write();
    h301->Write();
    h302->Write();
    h303->Write();
    h304->Write();
    h305->Write();
    h306->Write();
    h307->Write();
    h308->Write();
    h309->Write();
    h310->Write();
    h311->Write();
    h312->Write();
    h313->Write();
    h314->Write();
    h315->Write();
    h316->Write();
    h317->Write();



    /*
    int narr = filterfunc::vec_ptcut.size() - 1;
    auto h001 = dataframe
        .Histo1D<float>({"allpho", "", narr, &(filterfunc::vec_ptcut.front())}, "recoPt", "eventweight");
    auto h002 = dataframe.Filter("jetHadFlvr==0")
        .Histo1D<float>({"LYield", "", narr, &(filterfunc::vec_ptcut.front())}, "recoPt", "eventweight");
    auto h003 = dataframe.Filter("jetHadFlvr==4")
        .Histo1D<float>({"cYield", "", narr, &(filterfunc::vec_ptcut.front())}, "recoPt", "eventweight");
    auto h004 = dataframe.Filter("jetHadFlvr==5")
        .Histo1D<float>({"bYield", "", narr, &(filterfunc::vec_ptcut.front())}, "recoPt", "eventweight");




    h01->Write();
    h02->Write();
    h03->Write();
    h04->Write();
    */
    //dataframe.Filter( filterfunc::PhoSignalRegion, {chargedIsolation,"recoEta"} )
    //    .Define( "phoDataSideband", filterfunc::PhoDataSideband, {chargedIsolation, "recoEta"} )
}
void step2_makehist()
{
    auto newfile = new TFile("output_step2_makehist_C.root", "RECREATE");
    RDF rdf_QCD("t", "testeroot_QCDmadgraph.root");
    RDF rdf_exp("t", "testeroot_2016data.root");
    //RDF rdf_sig("t", "testeroot_sig.root");

    filterfunc::vec_ptcut = {25,34,41,56,70,85,100,115,135,155,175,190,200,220,250,300,350,400,500,750,1000,1500,2000,3000,10000}; // size = 16. ptbin = [0,15]
    filterfunc::dataera = "2016ReReco";
    filterfunc::cutIndicator = 0;
    filterfunc::checkplots = true;

    auto selRDF_QCD = CommonProceduresQCDMC(rdf_QCD);
    auto selRDF_exp = CommonProceduresData(rdf_exp);
    //auto selRDF_sig = CommonProceduresSigMC(rdf_sig);

    for ( int pEtaBin = 0; pEtaBin < 2; ++pEtaBin )
        for ( int jEtaBin = 0; jEtaBin < 3; ++jEtaBin )
            for ( int pPtBin = 0; pPtBin < filterfunc::vec_ptcut.size() - 1; ++pPtBin )
    {
        TDirectory* dir = newfile->mkdir( Form("bin_%d_%d_%d", pEtaBin, jEtaBin, pPtBin) );

        const char* binning = Form("phoetabin == %d && jetetabin == %d && phoptbin == %d", pEtaBin, jEtaBin, pPtBin);
        auto binnedRDF_QCD = ROOT::RDF::RNode( selRDF_QCD.Filter(binning) );
        makehist_QCD( binnedRDF_QCD, dir );

        auto binnedRDF_exp = ROOT::RDF::RNode( selRDF_exp.Filter(binning) );
        makehist_exp( binnedRDF_exp, dir );

        //auto binnedRDF_sig = ROOT::RDF::RNode( selRDF_sig.Filter(binning) );
        //makehist_sig( binnedRDF_sig, dir );
    }
    newfile->Close();
}
