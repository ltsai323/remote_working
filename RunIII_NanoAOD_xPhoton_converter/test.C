#include <string>
#include <iostream>
using namespace std;
#include "PhotonIDMVA.h"

//#include "MyPhoSelections.h"
//#include "MyJetSelections.h"


typedef ROOT::VecOps::RVec<float> RVecFloat;
typedef ROOT::VecOps::RVec<int  > RVecInt;
typedef ROOT::VecOps::RVec<short> RVecShort;

void test()
{
  //enable multi-threding
  ROOT::EnableImplicitMT();
  ROOT::RDataFrame dfIn("Events", "testsample.root");

  double wgt = dfIn.Sum("genWeight").GetValue();



  auto mydf = dfIn
    .Define("hardSVIdx"               , "ArgMax(SV_pt)")
    .Define("jetSubVtxPt"            , "SV_pt[hardSVIdx]")
    .Define( "passed", "GenPart_status==1 && GenPart_pdgId==22" )
    .Define( "passPhoSel", "Photon_pt>20 && Photon_eta <1.4" )
    .Filter( "nPhoton>0" )
    .Filter( "nJet>0" )
    .Define( "selPtIdx", "ArgMax(Photon_pt*passPhoSel)")
    .Define( "selPt", "Photon_pt[selPtIdx]")
    .Define( "dPhiGJet", "DeltaPhi(Photon_phi[selPtIdx], Jet_phi)")
    .Define( "dEtaGJet", "Photon_eta[selPtIdx] - Jet_eta")
    .Define( "dRGJet2", "sqrt(dPhiGJet*dPhiGJet + dEtaGJet*dEtaGJet)")
    .Define( "goodGJet", "dRGJet2 > 0.5")
    .Define( "jetIdx", "ArgMax(goodGJet * Jet_pt)");
    //.Define( "passed", "GenPart_status==1 && GenPart_pdgId==22" ).Filter("Sum(passed)>0");


  mydf.Snapshot("Events", "aa.root", { "selPtIdx", "selPt", "Photon_pt", "dPhiGJet", "dEtaGJet", "dRGJet2", "jetIdx", "jetSubVtxPt" } );
}
void test_()
{
  TMVA::Experimental::RReader modelBarrel("aa/TMVAClassification_BDTG.weights_Barrel.xml");
  TMVA::Experimental::RReader modelEndcap("aa/TMVAClassification_BDTG.weights_Endcap.xml");
  //model.AddSpectator("photon_eta");
  auto variables = modelBarrel.GetVariableNames();

  ROOT::RDataFrame dfIn("Events", "testsample.root");
  auto df__ = dfIn.Filter("nPhoton>1 && nJet>1");
  auto newF = df__.Define("photon_esEffSigmaRR"    , "Photon_esEffSigmaRR[0]"    ) // declare variables inside xml file.
                  .Define("photon_energyRaw"       , "Photon_energyRaw[0]"       )
                  .Define("photon_esEnergyOverRawE", "Photon_esEnergyOverRawE[0]")
                  .Define("photon_etaWidth"        , "Photon_etaWidth[0]"        )
                  .Define("photon_hoe"             , "Photon_hoe[0]"             )
                  .Define("photon_phiWidth"        , "Photon_phiWidth[0]"        )
                  .Define("photon_r9"              , "Photon_r9[0]"              )
                  .Define("photon_s4"              , "Photon_s4[0]"              )
                  .Define("photon_sieie"           , "Photon_sieie[0]"           )
                  .Define("photon_sieip"           , "Photon_sieip[0]"           )
                  .Define("photon_rho"             , "Rho_fixedGridRhoFastjetAll")
                  .Define("photon_eta"             , "Photon_eta[0]")
                  .Define("mvaoutputbarrel", TMVA::Experimental::Compute<11,float>(modelBarrel), variables)
                  .Define("mvaoutputendcap", TMVA::Experimental::Compute<11,float>(modelEndcap), variables)
                  .Define("mvaOutputBarrel", "mvaoutputbarrel[0]")
                  .Define("mvaOutputEndcap", "mvaoutputendcap[0]")
                  .Define("mvaOutput", [](float eta, float mvaBARREL, float mvaENDCAP) { return fabs(eta)<1.5 ? mvaBARREL:mvaENDCAP; }, {"photon_eta", "mvaOutputBarrel", "mvaOutputEndcap"});
  auto newF2= newF.Redefine("photon_esEffSigmaRR"    , "Photon_esEffSigmaRR[1]"    ) // declare variables inside xml file.
                  .Redefine("photon_energyRaw"       , "Photon_energyRaw[1]"       )
                  .Redefine("photon_esEnergyOverRawE", "Photon_esEnergyOverRawE[1]")
                  .Redefine("photon_etaWidth"        , "Photon_etaWidth[1]"        )
                  .Redefine("photon_hoe"             , "Photon_hoe[1]"             )
                  .Redefine("photon_phiWidth"        , "Photon_phiWidth[1]"        )
                  .Redefine("photon_r9"              , "Photon_r9[1]"              )
                  .Redefine("photon_s4"              , "Photon_s4[1]"              )
                  .Redefine("photon_sieie"           , "Photon_sieie[1]"           )
                  .Redefine("photon_sieip"           , "Photon_sieip[1]"           )
                  .Redefine("photon_rho"             , "Rho_fixedGridRhoFastjetAll")
                  .Redefine("photon_eta"             , "Photon_eta[1]")
                  .Define("mvaoutputbarrel1", TMVA::Experimental::Compute<11,float>(modelBarrel), variables)
                  .Define("mvaoutputendcap1", TMVA::Experimental::Compute<11,float>(modelEndcap), variables)
                  .Define("mvaOutputBarrel1", "mvaoutputbarrel1[0]")
                  .Define("mvaOutputEndcap1", "mvaoutputendcap1[0]")
                  .Define("mvaOutput1", [](float eta, float mvaBARREL, float mvaENDCAP) { return fabs(eta)<1.5 ? mvaBARREL:mvaENDCAP; }, {"photon_eta", "mvaOutputBarrel1", "mvaOutputEndcap1"});
  //auto display = newF2.Display({"mvaOutput", "mvaOutput1"});
  //display->Print();
  const char* _tmva_lacking_showershape_file_barrel_ = "aa/TMVAClassification_BDTG.weights_Barrel.xml";//"/Users/noises/workspace/remote_working/RunIII_NanoAOD_xPhoton_converter/TMVAClassification_BDTG.weights_Barrel.xml";
  const char* _tmva_lacking_showershape_file_endcap_ = "aa/TMVAClassification_BDTG.weights_Endcap.xml";//"/Users/noises/workspace/remote_working/RunIII_NanoAOD_xPhoton_converter/TMVAClassification_BDTG.weights_Endcap.xml";
  PhotonMVACalculator mvaMgr(
      _tmva_lacking_showershape_file_barrel_,
      _tmva_lacking_showershape_file_endcap_
  );
  //auto newF3 = newF2.Define( "mva", [mvaMgr] (
  //        const RVecFloat& c0,
  //        const RVecFloat& c1,
  //        const RVecFloat& c2,
  //        const RVecFloat& c3,
  //        const RVecFloat& c4,
  //        const RVecFloat& c5,
  //        const RVecFloat& c6,
  //        const RVecFloat& c7,
  //        const RVecFloat& c8,
  //        const RVecFloat& c9,
  //        const RVecFloat& c10,
  //        const RVecFloat& eta )
  //      { return mvaMgr.Score(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,eta); }, {
  //                                  "Photon_esEffSigmaRR"    ,
  //                                  "Photon_energyRaw"       ,
  //                                  "Photon_esEnergyOverRawE",
  //                                  "Photon_etaWidth"        ,
  //                                  "Photon_hoe"             ,
  //                                  "Photon_phiWidth"        ,
  //                                  "Photon_r9"              ,
  //                                  "Photon_s4"              ,
  //                                  "Photon_sieie"           ,
  //                                  "Photon_sieip"           ,
  //                                  "Rho_fixedGridRhoFastjetAll",
  //                                  "Photon_eta" } );

  std::vector<const char*> iii({
    "Photon_esEffSigmaRR[0]"    ,
    "Photon_energyRaw[0]"       ,
    "Photon_esEnergyOverRawE[0]",
    "Photon_etaWidth[0]"        ,
    "Photon_hoe[0]"             ,
    "Photon_phiWidth[0]"        ,
    "Photon_r9[0]"              ,
    "Photon_s4[0]"              ,
    "Photon_sieie[0]"           ,
    "Photon_sieip[0]"           ,
    "Rho_fixedGridRhoFastjetAll" });


  auto newF3 = mvaMgr.DefineMVAScore(newF2, "mva", iii, "Photon_eta[0]");
  newF3.Snapshot("ee", "aa.root", {"mva", "mvaOutput", "mvaOutput1"});
}
