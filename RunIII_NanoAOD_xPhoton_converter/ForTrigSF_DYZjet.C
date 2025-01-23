#include <string>
#include <iostream>
using namespace std;

#include "ROOT/RDataFrame.hxx"
#include "TH1D.h"
#include "TString.h"
#include "TCanvas.h"

#include "MyImportedFileMgr.h"
#include "MyDYjet_ZmmSelections.h"
#include "MyPhoSelections.h"
#include "MyJetSelections.h"
#include "MyIdxSelections.h"
#include "PhotonIDMVA.h"
#include "ShowerShapeCorrector.h"
typedef ROOT::VecOps::RVec<Float_t> RVecFloat;
typedef ROOT::VecOps::RVec<Int_t  > RVecInt;
typedef ROOT::VecOps::RVec<UChar_t> RVecUChar;
typedef ROOT::VecOps::RVec<Bool_t > RVecBool;

void ForTrigSF_DYZjet(const std::vector<std::string>& inFILEs, string outFile, bool isMC = false, const char* dataERA = "2022")
{
  //enable multi-threding
  ROOT::EnableImplicitMT();
  ROOT::RDataFrame dfIn("Events", inFILEs);



  //auto df_def = dfIn
  //  .Filter( "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==1" )
  //  .Filter( "nMuon>1" )
  //  .Filter( "nJet>0" )
  //  .Define("sel_muon_pair", [](const RVecFloat& pt, const RVecBool& tkID) { return DYjet_ZmmSelections::selectMuonPair(pt,tkID); }, {"Muon_pt", "Muon_mediumPromptId"})
  //  .Filter("sel_muon_pair.first")
  //  .Define("sel_muon1_idx", "sel_muon_pair.second.first")
  //  .Define("sel_muon2_idx", "sel_muon_pair.second.second")
  //  .Define("sel_muon1", "ROOT::Math::PtEtaPhiMVector(Muon_pt[sel_muon1_idx],Muon_eta[sel_muon1_idx],Muon_phi[sel_muon1_idx],Muon_mass[sel_muon1_idx])")
  //  .Define("sel_muon2", "ROOT::Math::PtEtaPhiMVector(Muon_pt[sel_muon2_idx],Muon_eta[sel_muon2_idx],Muon_phi[sel_muon2_idx],Muon_mass[sel_muon2_idx])")
  //  .Define("recZ", "sel_muon1+sel_muon2")
  //  .Filter("recZ.Pt()>15.")
  //  ;

  //auto df_out = df_def
  //  .Define("recZ_pt", "recZ.Pt()")
  //  .Define("recZ_eta", "recZ.Eta()")
  //  .Define("recZ_phi", "recZ.Phi()")
  //  .Define("recZ_mass", "recZ.M()")
  //  .Define("selMuon1_idx", "sel_muon1_idx")
  //  .Define("selMuon2_idx", "sel_muon2_idx");
  auto df_def = dfIn
    .Filter( "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==1" )
    .Filter( "nMuon>1" )
    .Filter( "nJet>0" );

  auto df_out = df_def;




  // set output variables
  std::vector<std::string> storedVariables({
      "Muon_highPtId",
      "Muon_highPurity",
      "Muon_inTimeMuon",
      "Muon_isGlobal",
      "Muon_isPFcand",
      "Muon_isStandalone",
      "Muon_isTracker",
      "Muon_jetNDauCharged",
      "Muon_looseId",
      "Muon_mediumId",
      "Muon_mediumPromptId",
      "Muon_miniIsoId",
      "Muon_multiIsoId",
      "Muon_mvaMuID_WP",
      "Muon_nStations",
      "Muon_nTrackerLayers",
      "Muon_pfIsoId",
      "Muon_puppiIsoId",
      "Muon_softId",
      "Muon_softMvaId",
      "Muon_tightCharge",
      "Muon_tightId",
      "Muon_tkIsoId",
      "Muon_triggerIdLoose",
      "Muon_jetIdx",
      "Muon_svIdx",
      "Muon_fsrPhotonIdx",
      "Muon_charge",
      "Muon_pdgId",
      "Muon_dxy",
      "Muon_dxyErr",
      "Muon_dxybs",
      "Muon_dz",
      "Muon_dzErr",
      "Muon_eta",
      "Muon_ip3d",
      "Muon_jetPtRelv2",
      "Muon_jetRelIso",
      "Muon_mass",
      "Muon_miniPFRelIso_all",
      "Muon_miniPFRelIso_chg",
      "Muon_mvaMuID",
      "Muon_pfRelIso03_all",
      "Muon_pfRelIso03_chg",
      "Muon_pfRelIso04_all",
      "Muon_phi",
      "Muon_pt",
      "Muon_ptErr",
      "Muon_segmentComp",
      "Muon_sip3d",
      "Muon_softMva",
      "Muon_tkRelIso",
      "Muon_tunepRelPt",
      "Muon_bsConstrainedChi2",
      "Muon_bsConstrainedPt",
      "Muon_bsConstrainedPtErr",
      "Muon_mvaLowPt",
      "Muon_mvaTTH",


      "run",
      "luminosityBlock",
      "event",
      "bunchCrossing", 				   
      "Rho_fixedGridRhoFastjetAll",
      "nJet",
      "Jet_jetId",
      "Jet_nConstituents",
      "Jet_nElectrons",
      "Jet_nMuons",
      "Jet_nSVs",
      "Jet_electronIdx1",
      "Jet_electronIdx2",
      "Jet_muonIdx1",
      "Jet_muonIdx2",
      "Jet_svIdx1", // index to SV not related to SV_* // skip this index because they are not related to SV_* variables
      "Jet_svIdx2", // index to SV not related to SV_* // skip this index because they are not related to SV_* variables
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
      "PV_npvs",
      "PV_npvsGood",
      "PuppiMET_phi",
      "PuppiMET_pt",
      "Flag_METFilters",
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
      "Jet_btagDeepFlavQG"
  });

  // merge column
  if ( isMC )
  {
      std::vector<std::string> genVars({
      "Muon_genPartIdx",
      "Muon_genPartFlav",

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
  }

  TString outputFILENAME(outFile);
  std::cout << "filtered entries : " << *(df_out.Count()) << std::endl;
  df_out.Snapshot("Events", outputFILENAME, storedVariables);


  TFile *f = new TFile(outputFILENAME,"UPDATE");
  f->cd();



  if ( isMC )
  {
      const double wgt = dfIn.Sum("genWeight").GetValue();
      const double sumEntries = dfIn.Count().GetValue();
      cout<< "Sum weight = "<<wgt<<endl;
      std::cout << "original entries : " << *(dfIn.Count()) << std::endl;
      TH1D *h1 = new TH1D("totWgt","bin1:IntegratedGenW bin2:IntegratedEntries",2,1,3);
      h1->Fill(1.+0.0001,wgt);
      h1->Fill(2.+0.0001,sumEntries);
      h1->Write(); // only MC contains this histogram. This histogram will be used to identify Data or MC in further analysis.

      const double wgt_presel = df_out.Sum("genWeight").GetValue();
      TH1D* hSelections = new TH1D("selectionRec", "bin1:IntegratedGenW bin2:bin1passPreSel", 5, 1, 6);
      // 0 : total entries * gen weight
      // 1 : entries passed photon Selection * gen weight
      // 2 : entries passed jet Selection * gen weight
      hSelections->Fill(1.+0.0001, wgt);
      hSelections->Fill(2.+0.0001, wgt_presel);
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
void ForTrigSF_DYZjet(const char* inFILEs, string outFile, bool isMC, const char* dataERA)
{ ForTrigSF_DYZjet( splitString(inFILEs,','), outFile, isMC, dataERA ); }

bool ___IsMC___(const char* input) {
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
bool IsMC_fromFile(const char* inFILE)
{
  const std::vector<std::string> all_files = splitString(inFILE, ',');
  if ( all_files.size() == 0 )
  { throw "Invalid input. No any file as input.\n\n"; }
  auto iFILE = TFile::Open(all_files[0].c_str());
  if (!iFILE || iFILE->IsZombie() )
  {
    std::cerr << "[FileNotOpened] Not able to open file : " << inFILE << std::endl;
    throw "Invalid Input. TFile got nothing\n\n";
    return false;
  }
  
  auto iTREE = (TTree*) iFILE->Get("Events");
  if (!iTREE )
  {
    std::cerr << "[InvalidTreeInFile] Tree 'Events' does not exists in file\n";
    return false;
  }

  bool is_mc = iTREE->GetBranch("genWeight") ? true : false;

  iFILE->Close();
  return is_mc;
}

int main(int argc, const char* argv[])
{
  // usage:
  //   ./exec in1.root,in2.root out.root isMC 2022
  //   arg 1: input root files, separated by comma
  //   arg 2: output root file name
  //   arg 3: data era
  if ( argc < 3+1 ) { std::cerr << "Input arguments : 1.in root, 2. outroot 3. data era \n\n"; return 1; }
  bool is_mc = IsMC_fromFile(argv[1]);
  std::cout << "i@ [IsMC] is mc ? " << is_mc << std::endl;
  //bool is_mc = ___IsMC___(argv[3]);
  ForTrigSF_DYZjet(argv[1],argv[2], is_mc, "2022EE");
  //splitString_testfunc(argv);

  return 0;
}
