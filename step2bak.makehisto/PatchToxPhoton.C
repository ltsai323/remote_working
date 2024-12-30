#include <string>
#include <iostream>
using namespace std;

#include "ROOT/RDataFrame.hxx"
#include "TFile.h"
#include "TH1D.h"
#include "TString.h"
#include "TRandom3.h"
#include "TCanvas.h"

#include "MyImportedFileMgr.h"
#include "MyPhoSelections.h"
#include "MyJetSelections.h"
#include "MyIdxSelections.h"
#include "PhotonIDMVA.h"
#include "ShowerShapeCorrector.h"
#include "JsonEvaluateMgr.h"
typedef ROOT::VecOps::RVec<float> RVecFloat;
typedef ROOT::VecOps::RVec<UChar_t> RVecUChar;

double TotalGenWeight(const char* inFILE)
{
  auto tFILE = TFile::Open(inFILE);
  auto hGenW = (TH1D*) tFILE->Get("totWgt");
  if ( hGenW == nullptr ) return -1; // is data
  double totalGenWeight = hGenW->GetBinContent(1);
  tFILE->Close();
  return totalGenWeight;
}
void PatchToxPhoton(const char* inFILE, string outFile, double totalGenWeight = -1, const std::string& dataERA = "")
{
  TRandom3* rnd = new TRandom3();
  //enable multi-threding
  ROOT::EnableImplicitMT();
  ROOT::RDataFrame dfIn("Events", inFILE);

  const bool isData = totalGenWeight<0 ? true : false;
  const bool isMC   = totalGenWeight>=0 ? true : false;

// photon pt smearing for MC from rho measurments
//auto cset_smearing = cset_photon_scale_smearing_file->at("Prompt2022FG_SmearingJSON");
//Float_t rho    = cset_smearing->evaluate({"rho",Photon_eta[ij], Photon_r9[ij]});
//Float_t smearing = gRandom->Gaus(1,rho);
//Photon_pt_nom = Photon_pt[ij]*smearing;
  JsonEvaluateMgr::JsonEvaluateMgr rho_corr_forMC("data/Photon_scale_smearing.json", "Prompt2022FG_SmearingJSON");

// photon pt scaling for data
//auto cset_scale = cset_photon_scale_smearing_file->at("Prompt2022FG_ScaleJSON");
//Float_t scale = 1.0*cset_scale->evaluate({"total_correction",Photon_seedGain[ij],Run,Photon_eta[ij],Photon_r9[ij],Photon_pt[ij]});
  JsonEvaluateMgr::JsonEvaluateMgr pt_smear_forDATA("data/Photon_scale_smearing.json", "Prompt2022FG_ScaleJSON");

  //auto dfFiltered = dfIn.Filter("PassPhoHLT && PassJetHLT && Flag_METFilters == 1");
  auto dfFiltered = dfIn
    .Filter("HLT_Photon200==1")
    .Define("abs_phoeta", "abs(Photon_eta)")
    .Define("is_barrelpho", "abs_phoeta<1.4442")
    .Define("is_endcappho", "abs_phoeta>1.566 && abs_phoeta<2.5")
    .Define("abs_jeteta", "abs(Jet_eta)")
    .Define("sel_barrelpho", "is_barrelpho && (Photon_pfChargedIsoPFPV<1.7 && Photon_sieie<0.015 && Photon_hoe<0.05 && Photon_pfChargedIsoWorstVtx<10)")
    .Define("sel_endcappho", "is_endcappho && (Photon_pfChargedIsoPFPV<1.5 && Photon_sieie<0.04  && Photon_hoe<0.05 && Photon_pfChargedIsoWorstVtx<10)")
    .Define("pass_photon_selection_without_pt_cut", "sel_barrelpho || sel_endcappho");


  // Reject defects from Run2022G
  if ( dataERA == "Run2022G" )
    dfFiltered = dfFiltered.Define("EEVeto", "!(Photon_pt>700 && Photon_pt<900 && Photon_seediEtaOriX+0==-21 && Photon_seediPhiOriY==260)");

  auto canv = new TCanvas("c1", "", 800, 600);
  if ( isData )
  {
    dfFiltered = dfFiltered
        .Define("photon_pt_calib",
          [&](const RVecFloat& phoPT, const RVecUChar& phoSEEDgain, UInt_t evtRUN, const RVecFloat& phoETA, const RVecFloat& phoR9)
          { return JsonEvaluateMgr::PhotonPtScaling_forData(pt_smear_forDATA.entry, phoPT, phoSEEDgain, evtRUN, phoETA, phoR9); }
          , {"Photon_pt", "Photon_seedGain", "run", "Photon_eta", "Photon_r9"});
  }
  if ( isMC )
  {
    dfFiltered = dfFiltered
      .Define("photon_pt_calib",
          [&](const RVecFloat& phoPT, const RVecFloat& phoETA, const RVecFloat& phoR9)
          { return JsonEvaluateMgr::PhotonPtSmearing_RandomRho_forMC(rho_corr_forMC.entry,rnd, phoPT,phoETA,phoR9); }
          , {"Photon_pt", "Photon_eta", "Photon_r9"} );
  }
  auto h = dfFiltered.Histo1D("photon_pt_calib");
  h->Draw();
  canv->SaveAs("hi.png");

  return;



  auto dfDefined = dfFiltered
    .Define("phoFillIdx"              , []() { return 0; })
    .Define("isData"                  , [isData]() { return isData; } )
    .Define("recoPt"                  , "Photon_pt[selectedPhoIdx]")
    .Define("recoEta"                 , "Photon_eta[selectedPhoIdx]")
    .Define("recoPhi"                 , "Photon_phi[selectedPhoIdx]")
    .Define("isRecoSCEtaEB"           , "Photon_isScEtaEB[selectedPhoIdx]")
    .Define("isRecoSCEtaEE"           , "Photon_isScEtaEE[selectedPhoIdx]")
    .Define("r9Full5x5"               , "Photon_r9[selectedPhoIdx]")
    .Define("s4Full5x5"               , "Photon_s4[selectedPhoIdx]")
    .Define("esEnergyOverSCRawEnergy" , "Photon_esEnergyOverRawE[selectedPhoIdx]")
    .Define("HoverE"                  , "Photon_hoe_PUcorr[selectedPhoIdx]") // PU corrected
    .Define("chIsoRaw"                , "Photon_pfChargedIso[selectedPhoIdx]")
    .Define("chIsoRawPFPV"            , "Photon_pfChargedIsoPFPV[selectedPhoIdx]")
    .Define("chWorstRaw"              , "Photon_pfChargedIsoWorstVtx[selectedPhoIdx]")
    //.Define("eleVeto"                 , "Photon_pfChargedIsoWorstVtx[selectedPhoIdx]") // abandoned
    .Define("rawE"                    , "Photon_energyRaw[selectedPhoIdx]")
    .Define("rawEerr"                 , "Photon_energyErr[selectedPhoIdx]")
    .Define("scEtaWidth"              , "Photon_etaWidth[selectedPhoIdx]")
    .Define("scPhiWidth"              , "Photon_phiWidth[selectedPhoIdx]")
    .Define("esRR"                    , "Photon_esEffSigmaRR[selectedPhoIdx]")
    //.Define("esEn"                    , "Photon_es") // not stored in NanoAOD
    // .Define("mva"                     , "mva") // already in data
    .Define("phohasPixelSeed"         , "Photon_pixelSeed[selectedPhoIdx]")
    .Define("sieieFull5x5"            , "Photon_sieie[selectedPhoIdx]")
    .Define("sieipFull5x5"            , "Photon_sieip[selectedPhoIdx]")
    .Define("sipipFull5x5"            , "Photon_sipip[selectedPhoIdx]")


    .Define("jetPt"                   , "Jet_pt[selectedGJetIdx]")
    .Define("jetEta"                  , "Jet_eta[selectedGJetIdx]")
    .Define("JetY"                    , "Jet_eta[selectedGJetIdx]") // no jetY at nanoAOD
    .Define("jetPhi"                  , "Jet_phi[selectedGJetIdx]")
    .Define("jetNSV"                  , "Jet_nSVs[selectedGJetIdx]")

    .Define("jetDeepFlavourB"         , "Jet_btagDeepFlavB[selectedGJetIdx]")
    .Define("jetDeepFlavourCvsB"      , "Jet_btagDeepFlavCvB[selectedGJetIdx]")
    .Define("jetDeepFlavourCvsL"      , "Jet_btagDeepFlavCvL[selectedGJetIdx]")
    .Define("jetDeepFlavourQvsG"      , "Jet_btagDeepFlavQG[selectedGJetIdx]")

    .Define("jetPNetB"                , "Jet_btagPNetB[selectedGJetIdx]")
    .Define("jetPNetCvsB"             , "Jet_btagPNetCvB[selectedGJetIdx]")
    .Define("jetPNetCvsL"             , "Jet_btagPNetCvL[selectedGJetIdx]")
    .Define("jetPNetQvsG"             , "Jet_btagPNetQvG[selectedGJetIdx]")

    .Define("jetRobustParTAK4B"       , "Jet_btagRobustParTAK4B[selectedGJetIdx]")
    .Define("jetRobustParTAK4CvsB"    , "Jet_btagRobustParTAK4CvB[selectedGJetIdx]")
    .Define("jetRobustParTAK4CvsL"    , "Jet_btagRobustParTAK4CvL[selectedGJetIdx]")
    .Define("jetRobustParTAK4QvsG"    , "Jet_btagRobustParTAK4QG[selectedGJetIdx]")

    //.Define("hardSVIdx"               , "ArgMax(SV_pt)")
    //.Define("jetSubVtxPt"             , "SV_pt[hardSVIdx]")
    //.Define("jetSubVtxMass"           , "SV_mass[hardSVIdx]")
    //.Define("jetSubVtx3DSig"          , "SV_dlenSig[hardSVIdx]")
    //.Define("jetSubVtxNtrks"          , "SV_ntracks[hardSVIdx]")
    //.Define("jetSubVtxChi2"           , "SV_chi2[hardSVIdx]/SV_ndof[hardSVIdx]")



    .Define("nVtx"                    , "PV_npvs")
    .Define("rho"                     , "Rho_fixedGridRhoFastjetAll")
    .Define("MET"                     , "PuppiMET_pt")
    .Define("METPhi"                  , "PuppiMET_phi")



    .Define("jetPartonID"               , "Jet_partonFlavour[selectedGJetIdx]")
    .Define("jetHadFlvr"                , "Jet_hadronFlavour[selectedGJetIdx]")
    ;
  if ( isData )
  {
    dfDefined = dfDefined
      .Define("recoPtCalib"             , "Photon_pt[selectedPhoIdx]")
      .Define("calib_chIso"             , "")
      ;
  }
  if ( isMC )
  {
    float xs = 3317.8583;
    float integratedLuminosity = 19.6;
    dfDefined = dfDefined
      .Define("crossSection"         , [xs]() { return xs; })
      .Define("totalGenWeight"       , [totalGenWeight]() { return totalGenWeight; })
      .Define("integratedLuminosity" , [integratedLuminosity]() { return integratedLuminosity; })
      .Define("mcweight"             , "genWeight * crossSection * integratedLuminosity / totalGenWeight")
    //.Define("nPU"                     , "Pileup_nPU") // MC only
    //.Define("puwei"                   , "") // asdf MC only
    .Define("matchedPhoIdx"           , "Photon_genPartIdx[selectedPhoIdx]")
    .Define("isMatched"               , "matchedPhoIdx>=0")
    .Define("mcPt"                    , "GenPart_pt[matchedPhoIdx]")
    .Define("mcEta"                   , "GenPart_eta[matchedPhoIdx]")
    .Define("mcPhi"                   , "GenPart_phi[matchedPhoIdx]")
    .Define("mcMomPID"                , "GenPart_genPartIdxMother[matchedPhoIdx]")

    .Define("genHT"                         , "GenPart_pt[matchedPhoIdx]") // asdf
    //.Define("pthat"                         , IdxSelections::GetFloat, {"matchedPhoIdx", "GenPart_pt"}) // asdf
    .Define("calib_sieieFull5x5"            , "Photon_sieie_calib[selectedPhoIdx]")
    .Define("calib_esRR"                    , "Photon_esEffSigmaRR_calib[selectedPhoIdx]")
    .Define("calib_esEnergyOverSCRawEnergy" , "Photon_esEnergyOverRawE_calib[selectedPhoIdx]")
    .Define("calib_rawE"                    , "Photon_energyRaw_calib[selectedPhoIdx]")
    .Define("calib_scPhiWidth"              , "Photon_phiWidth_calib[selectedPhoIdx]")
    .Define("calib_scEtaWidth"              , "Photon_etaWidth_calib[selectedPhoIdx]")
    .Define("calib_r9Full5x5"               , "Photon_r9_calib[selectedPhoIdx]")
    .Define("calib_s4Full5x5"               , "Photon_s4_calib[selectedPhoIdx]")
    .Define("calib_sieipFull5x5"            , "Photon_sieip_calib[selectedPhoIdx]")
    .Define("calib_HoverE"                  , "Photon_hoe_calib[selectedPhoIdx]")

    //.Define("calib_mva"               , IdxSelections::GetFloat, {"matchedPhoIdx", "calib_mva"}) // has been defined

    .Define("selectedGenJetIdx"         , "Jet_genJetIdx[selectedGJetIdx]")
    .Define("jetGenJetPt"               , "GenJet_pt[selectedGenJetIdx]") // asdf MC
    .Define("jetGenJetEta"              , "GenJet_eta[selectedGenJetIdx]")
    .Define("jetGenJetPhi"              , "GenJet_phi[selectedGenJetIdx]")
    .Define("jetGenJetMass"             , "GenJet_mass[selectedGenJetIdx]")
    .Define("jetGenJetPartonID"         , "GenJet_partonFlavour[selectedGenJetIdx]")
    .Define("jetGenJetHadFlvr"          , "GenJet_hadronFlavour[selectedGenJetIdx]");
  }
  
  
  dfDefined.Snapshot("t", outFile.c_str(), {"r9Full5x5", "phoFillIdx", "isMatched", "matchedPhoIdx", "jetGenJetPt", "mcPt"});
}

int main(int argc, const char* argv[])
{
  // usage:
  //   ./exec in1.root,in2.root out.root
  //   arg 1: input root files, separated by comma
  //   arg 2: output root file name
  if ( argc < 2+1 ) { std::cerr << "Input arguments : 1.in root, 2. outroot 3. data_era\n\n"; return 1; }
  //const bool isMC = true;
  //double totalGenWeight = isMC ? TotalGenWeight(argv[1]) : -1;
  double totalGenWeight = TotalGenWeight(argv[1]);
  const char* iFILE = argv[1];
  const char* oFILE = argv[2];
  const char* dataERA = argv[3];
  /* available dataERA
   * Run2022E Run2022F Run2022G
   * Run2022GJetPythia Run2022GJetMadgraph
   * Run2022QCDMadgraph
   */
  
  PatchToxPhoton(iFILE, oFILE, totalGenWeight, dataERA);
  return 0;
}
