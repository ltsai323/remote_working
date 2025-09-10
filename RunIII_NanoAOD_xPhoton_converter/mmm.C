#include <string>
#include <iostream>
using namespace std;

#include "ROOT/RDataFrame.hxx"
#include "TH1D.h"
#include "TString.h"

#include "MyImportedFileMgr.h"
#include "MyPhoSelections.h"
#include "MyJetSelections.h"
#include "MyIdxSelections.h"
#include "PhotonIDMVA.h"
#include "ShowerShapeCorrector.h"
typedef ROOT::VecOps::RVec<float> RVecFloat;

void mmm(TFile* fIN, string outFile, bool isMC = false, const char* dataERA = "2022")
{
  //enable multi-threding
  ROOT::EnableImplicitMT();
  auto t = (TTree*) fIN->Get("Events");
  ROOT::RDataFrame dfIn(t);
  //ROOT::RDataFrame dfIn("Events", inFILEs);

  std::map<std::string,const char*> usedfiles = ImportedFileMgr::Factory("relative");
  ShowerShapeCorrector::ShowerShapeCalibGraphManager SScorrMgr( usedfiles["SScorrBarrel"], usedfiles["SScorrEndcap"] );
  PhotonMVACalculator mvaMgr( usedfiles["tmvaBarrel"], usedfiles["tmvaEndcap"] );



  auto df_def = dfIn
    .Define( "PassPhoHLT", PhoSelections::EventPassedPhoHLT().Data() )
    //.Define( "PreselectedPhoton", PhoSelections::PhotonPreselection().Data() )
    .Define( "PreselectedPhoton", PhoSelections::PhotonSaikatSelection().Data() )
    //.Define( "goodPhoton", "PassPhoHLT && PreselectedPhoton" )
    .Define( "goodPhoton", "PreselectedPhoton" ) // pass HLT requirement at PactoToxPhoton
    //.Define("selectedPhoIdx", IdxSelections::IndexOfSelectedLeadingCandidate, {"goodPhoton", "Photon_pt"})
    .Define("selectedPhoIdx", "ArgMax(Photon_pt * goodPhoton)")

    .Define( "PassJetHLT", JetSelections::EventPassedAllJetHLT().Data() )
    .Define( "PreselectedJet", JetSelections::JetPreselection().Data() )
    .Define( "goodJet", "PassJetHLT && PreselectedJet" ) // pass HLT requirement at PactoToxPhoton
    .Define( "dPhiGJet", "DeltaPhi(Photon_phi[selectedPhoIdx], Jet_phi)")
    .Define( "dEtaGJet",          "Photon_eta[selectedPhoIdx] - Jet_eta")
    .Define( "dRGJet", "sqrt(dPhiGJet*dPhiGJet + dEtaGJet*dEtaGJet)")
    .Define( "dRGJetCut", "dRGJet > 0.4")
    .Define( "goodGJet", "goodJet && dRGJetCut")
    //.Define("selectedJetIdx", IdxSelections::IndexOfSelectedLeadingCandidate, {"goodGJet"   , "Jet_pt"})
    .Define("selectedGJetIdx", "ArgMax(goodGJet*Jet_pt)");
    //.Define("selectedGJetIdx", "ArgMax(Jet_pt)");

    df_def = mvaMgr.DefineMVAScore(df_def,"mva", {
          "Photon_esEffSigmaRR[selectedPhoIdx]"     ,
          "Photon_energyRaw[selectedPhoIdx]"        ,
          "Photon_esEnergyOverRawE[selectedPhoIdx]" ,
          "Photon_etaWidth[selectedPhoIdx]"         ,
          "Photon_hoe[selectedPhoIdx]"              ,
          "Photon_phiWidth[selectedPhoIdx]"         ,
          "Photon_r9[selectedPhoIdx]"               ,
          "Photon_s4[selectedPhoIdx]"               ,
          "Photon_sieie[selectedPhoIdx]"            ,
          "Photon_sieip[selectedPhoIdx]"            ,
          "Rho_fixedGridRhoFastjetAll"   ,
        }, "Photon_eta[selectedPhoIdx]" );

  
  if ( isMC )
  {
    df_def = df_def
      .Define("Photon_sieie_calib"            , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_sieie"           , eta,col); }, {"Photon_eta", "Photon_sieie"           })
      .Define("Photon_esEffSigmaRR_calib"     , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_esEffSigmaRR"    , eta,col); }, {"Photon_eta", "Photon_esEffSigmaRR"    })
      .Define("Photon_esEnergyOverRawE_calib" , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_esEnergyOverRawE", eta,col); }, {"Photon_eta", "Photon_esEnergyOverRawE"})
      .Define("Photon_energyRaw_calib"        , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_energyRaw"       , eta,col); }, {"Photon_eta", "Photon_energyRaw"       })
      .Define("Photon_phiWidth_calib"         , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_phiWidth"        , eta,col); }, {"Photon_eta", "Photon_phiWidth"        })
      .Define("Photon_etaWidth_calib"         , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_etaWidth"        , eta,col); }, {"Photon_eta", "Photon_etaWidth"        })
      .Define("Photon_r9_calib"               , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_r9"              , eta,col); }, {"Photon_eta", "Photon_r9"              })
      .Define("Photon_s4_calib"               , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_s4"              , eta,col); }, {"Photon_eta", "Photon_s4"              })
      .Define("Photon_sieip_calib"            , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_sieip"           , eta,col); }, {"Photon_eta", "Photon_sieip"           })
      .Define("Photon_hoe_calib"              , [SScorrMgr](const RVecFloat& eta, const RVecFloat& col) { return SScorrMgr.ApplyCalibration("Photon_hoe"             , eta,col); }, {"Photon_eta", "Photon_hoe"             })
    ;
    df_def = mvaMgr.DefineMVAScore(df_def,"mva_calib", {
          "Photon_esEffSigmaRR_calib[selectedPhoIdx]"     ,
          "Photon_energyRaw_calib[selectedPhoIdx]"        ,
          "Photon_esEnergyOverRawE_calib[selectedPhoIdx]" ,
          "Photon_etaWidth_calib[selectedPhoIdx]"         ,
          "Photon_hoe_calib[selectedPhoIdx]"              ,
          "Photon_phiWidth_calib[selectedPhoIdx]"         ,
          "Photon_r9_calib[selectedPhoIdx]"               ,
          "Photon_s4_calib[selectedPhoIdx]"               ,
          "Photon_sieie_calib[selectedPhoIdx]"            ,
          "Photon_sieip_calib[selectedPhoIdx]"            ,
          "Rho_fixedGridRhoFastjetAll"   ,
        }, "Photon_eta[selectedPhoIdx]" );

    /*
    df_def = df_def
      .Define( "PhotonGen_genPartIdxMother", "GenPart_genPartIdxMother[Photon_genPartIdx]")
      .Define( "PhotonGen_statusFlags"     , "GenPart_statusFlags[Photon_genPartIdx]"     )
      .Define( "PhotonGen_pdgId"           , "GenPart_pdgId[Photon_genPartIdx]"           )
      .Define( "PhotonGen_status"          , "GenPart_status[Photon_genPartIdx]"          )
      .Define( "PhotonGen_eta"             , "GenPart_eta[Photon_genPartIdx]"             )
      .Define( "PhotonGen_mass"            , "GenPart_mass[Photon_genPartIdx]"            )
      .Define( "PhotonGen_phi"             , "GenPart_phi[Photon_genPartIdx]"             )
      .Define( "PhotonGen_pt"              , "GenPart_pt[Photon_genPartIdx]"              );
    */
  }

  auto df_filtered  = df_def
    //.Filter("Sum(goodGJet)>0")
    //.Filter("Sum(goodPhoton)>0");
    .Filter("Sum(goodPhoton)>0");


  // set output variables
  std::vector<std::string> storedVariables({
      "selectedPhoIdx",
      "selectedGJetIdx",
      "PassJetHLT",
      "PassPhoHLT",
      "run",
      "luminosityBlock",
      "event",
      "bunchCrossing", 				   
      "Photon_seediEtaOriX",
      "Photon_cutBased",
      "Photon_isScEtaEB",
      "Photon_isScEtaEE",
      "Photon_mvaID_WP80",
      "Photon_mvaID_WP90",
      "Photon_pixelSeed",
      "Photon_seedGain",
      "Photon_electronIdx",
      "Photon_seediPhiOriY",
      "Photon_vidNestedWPBitmap",
      "Photon_energyErr",
      "Photon_energyRaw",
      "Photon_esEffSigmaRR",
      "Photon_esEnergyOverRawE",
      "Photon_eta",
      "Photon_etaWidth",
      "Photon_haloTaggerMVAVal",
      "Photon_hoe",
      "Photon_hoe_PUcorr",
      "Photon_mvaID",
      "Photon_pfChargedIso",
      "Photon_pfChargedIsoPFPV",
      "Photon_pfChargedIsoWorstVtx",
      "Photon_pfPhoIso03",
      "Photon_pfRelIso03_all_quadratic",
      "Photon_pfRelIso03_chg_quadratic",
      "Photon_phi",
      "Photon_phiWidth",
      "Photon_pt",
      "Photon_r9",
      "Photon_s4",
      "Photon_sieie",
      "Photon_sieip",
      "Photon_sipip",
      "Photon_trkSumPtHollowConeDR03",
      "Photon_trkSumPtSolidConeDR04",
      "Photon_x_calo",
      "Photon_y_calo",
      "Photon_z_calo",
      "mva",
      "Rho_fixedGridRhoFastjetAll",
      "nJet",
      "Jet_jetId",
      "Jet_nConstituents",
      "Jet_nElectrons",
      "Jet_nMuons",
      "Jet_nSVs",
      //"Jet_electronIdx1",
      //"Jet_electronIdx2",
      //"Jet_muonIdx1",
      //"Jet_muonIdx2",
      //"Jet_svIdx1", // index to SV not related to SV_* // skip this index because they are not related to SV_* variables
      //"Jet_svIdx2", // index to SV not related to SV_* // skip this index because they are not related to SV_* variables
      "Jet_hfadjacentEtaStripsSize",
      "Jet_hfcentralEtaStripSize",
      "Jet_PNetRegPtRawCorr",
      "Jet_PNetRegPtRawCorrNeutrino",
      "Jet_PNetRegPtRawRes",
      "Jet_area",
      "Jet_chEmEF",
      "Jet_chHEF",
      "Jet_eta",
      "Jet_hfsigmaEtaEta",
      "Jet_hfsigmaPhiPhi",
      "Jet_mass",
      "Jet_muEF",
      "Jet_muonSubtrFactor",
      "Jet_neEmEF",
      "Jet_neHEF",
      "Jet_phi",
      "Jet_pt",
      "Jet_rawFactor",
      //"TrigObj_l1charge",
      //"TrigObj_id",
      //"TrigObj_l1iso",
      //"TrigObj_filterBits",
      //"TrigObj_pt",
      //"TrigObj_eta",
      //"TrigObj_phi",
      //"TrigObj_l1pt",
      //"TrigObj_l1pt_2",
      //"TrigObj_l2pt",
      "PV_npvs",
      "PV_npvsGood",
      "PuppiMET_phi",
      "PuppiMET_pt",
      "Flag_METFilters",
      "HLT_Photon200",
      "HLT_Photon175",
      "HLT_Photon150",
      //  "HLT_Photon120",
      //  "HLT_PFJet40",
      //  "HLT_PFJet60",
      //  "HLT_PFJet80",
      //  "HLT_PFJet110",
      //  "HLT_PFJet140",
      //  "HLT_PFJet200",
      //  "HLT_PFJet260",
      //  "HLT_PFJet320",
      //  "HLT_PFJet400",
      //  "HLT_PFJet450",
      //  "HLT_PFJet500",
      //  "HLT_PFJet550"
      "nSV",
      "SV_dxySig",
      "SV_dlenSig",
      "SV_ntracks",
      "SV_chi2",
      "SV_eta",
      "SV_mass",
      "SV_ndof",
      "SV_phi",
      "SV_pt",
      "SV_x",
      "SV_y",
      "SV_z",

      "Jet_btagPNetB",
      "Jet_btagPNetCvB",
      "Jet_btagPNetCvL",
      "Jet_btagPNetQvG",
      
      "Jet_btagRobustParTAK4B",
      "Jet_btagRobustParTAK4CvB",
      "Jet_btagRobustParTAK4CvL",
      "Jet_btagRobustParTAK4QG",

      "Jet_btagDeepFlavB",
      "Jet_btagDeepFlavCvB",
      "Jet_btagDeepFlavCvL",
      "Jet_btagDeepFlavQG",
  });

  // merge column
  if ( isMC )
  {
      std::vector<std::string> genVars({
      "Photon_genPartIdx",
      "Jet_genJetIdx",
      "GenPart_genPartIdxMother",
      "GenPart_statusFlags",
      "GenPart_pdgId",
      "GenPart_status",
      "GenPart_eta",
      "GenPart_mass",
      "GenPart_phi",
      "GenPart_pt",
      "GenJet_eta",
      "GenJet_pt",
      "GenJet_phi",
      "GenJet_mass",
      "GenJet_partonFlavour",
      "GenJet_hadronFlavour",
      "genWeight",
      "GenIsolatedPhoton_eta",
      "GenIsolatedPhoton_mass",
      "GenIsolatedPhoton_phi",
      "GenIsolatedPhoton_pt",
      "Generator_id1",
      "Generator_id2",
      "Generator_scalePDF",
      "Generator_weight",
      "Generator_x1",
      "Generator_x2",
      //"LHEPdfWeight",
      //"LHEReweightingWeight",
      //"LHEScaleWeight",
      "Pileup_nPU",
      "Jet_partonFlavour",
      "Jet_hadronFlavour",
      "PSWeight"
      });
    storedVariables.insert( storedVariables.end(), genVars.begin(), genVars.end() );
    std::vector<std::string> SScalibratedColumns({
      "Photon_sieie_calib"           ,
      "Photon_esEffSigmaRR_calib"    ,
      "Photon_esEnergyOverRawE_calib",
      "Photon_energyRaw_calib"       ,
      "Photon_phiWidth_calib"        ,
      "Photon_etaWidth_calib"        ,
      "Photon_r9_calib"              ,
      "Photon_s4_calib"              ,
      "Photon_sieip_calib"           ,
      "Photon_hoe_calib"             ,
      "mva_calib",
      });
    storedVariables.insert( storedVariables.end(), SScalibratedColumns.begin(), SScalibratedColumns.end() );
  }

  TString outputFILENAME(outFile);
  std::cout << "filtered entries : " << *(df_filtered.Count()) << std::endl;
  df_filtered.Snapshot("Events", outputFILENAME, storedVariables);


  TFile *f = new TFile(outputFILENAME,"UPDATE");
  f->cd();



  if ( isMC )
  {
      const double wgt = dfIn.Sum("genWeight").GetValue();
      cout<< "Sum weight = "<<wgt<<endl;
      std::cout << "original entries : " << *(dfIn.Count()) << std::endl;
      TH1D *h1 = new TH1D("totWgt","totWgt",1,1,2);
      h1->Fill(1.,wgt);
      h1->Write();

      const double wgt_phoPassed = df_def.Filter("Sum(goodPhoton)>0").Sum("genWeight").GetValue();
      const double wgt_jetPassed = df_def.Filter("Sum(goodJet)>0").Sum("genWeight").GetValue();
      TH1D* hSelections = new TH1D("selectionRec", "Entries * genWeight", 5, 0., 5.);
      // 0 : total entries * gen weight
      // 1 : entries passed photon Selection * gen weight
      // 2 : entries passed jet Selection * gen weight
      hSelections->Fill(0.+0.0001, wgt);
      hSelections->Fill(1.+0.0001, wgt_phoPassed);
      hSelections->Fill(2.+0.0001, wgt_jetPassed);
      hSelections->Write();
  }

  f->Close();
}
std::vector<std::string> splitString(const std::string &input, char delimiter) {
    std::vector<std::string> result;
    std::stringstream ss(input);
    std::string item;

    // Split by the delimiter and add to the result vector
    while (std::getline(ss, item, delimiter)) {
        result.push_back(item);
    }

    return result;
}
void splitString_testfunc(const char* argv[])
{
  std::cout << "The split string is : " << std::endl;
  for ( const auto& str : splitString(argv[1], ',') )
    std::cout << str << std::endl;
}
void ForTrigSF_MC(const char* inFILEs, string outFile, bool isMC, const char* dataERA)
{ ForTrigSF_MC( splitString(inFILEs,','), outFile, isMC, dataERA ); }

bool isMC(const char* input) {
    if (
            strcmp(input, "data") == 0 ||
            strcmp(input, "DATA") == 0 ||
            strcmp(input, "Data") == 0 ||
            strcmp(input, "0") == 0)
        return false;
    if (
            strcmp(input, "MC") == 0 ||
            strcmp(input, "mc") == 0 ||
            strcmp(input, "1") == 0)
        return true;
    throw std::invalid_argument(Form("\n\n[isMC] Unknown input '%s' received\n\n", input));
}

int main(int argc, const char* argv[])
{
  // usage:
  //   ./exec in1.root,in2.root out.root isMC 2022
  //   arg 1: input root files, separated by comma
  //   arg 2: output root file name
  //   arg 3: a flag : is MC or not (1 / 0)
  //   arg 4: data era
  if ( argc < 3+1 ) { std::cerr << "Input arguments : 1.in root, 2. outroot 3. isMC(1/0) \n\n"; return 1; }
  bool is_mc = isMC(argv[3]);
  ForTrigSF_MC(argv[1],argv[2], is_mc, "2022EE");
  //splitString_testfunc(argv);

  return 0;
}
