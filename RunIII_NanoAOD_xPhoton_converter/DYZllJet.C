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
#include "MyComplexFunctions.h"
typedef ROOT::VecOps::RVec<float> RVecFloat;

void DYZllJet(const std::vector<std::string>& inFILEs, string outFile, bool isMC = false, const char* dataERA = "2022")
{
  //enable multi-threding
  ROOT::EnableImplicitMT();
  ROOT::RDataFrame dfIn("Events", inFILEs);

  std::map<std::string,const char*> usedfiles = ImportedFileMgr::Factory("relative");
  ShowerShapeCorrector::ShowerShapeCalibGraphManager SScorrMgr( usedfiles["SScorrBarrel"], usedfiles["SScorrEndcap"] );
  PhotonMVACalculator mvaMgr( usedfiles["tmvaBarrel"], usedfiles["tmvaEndcap"] );



  auto df_def = dfIn
    .Define( "mu_4vec", ComplexFunctions::Particle_PtEtaPhiM, {"Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass"})
    .Define( "goodMuon", "Muon_pt>20 && Muon_tightId==1 && Muon_tkIsoId == 1")
    .Define( "PassMuonHLT", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL == 1" );

  auto df_selected = df_def
    .Filter("nJet>0")
    .Filter("PassMuonHLT")
    .Define("preselected_jet", JetSelections::JetPreselection().Data() )
    .Define("jet0_idx", "ArgMax(preselected_jet*Jet_pt")
    .Define("good_muon_pt", "goodMuon*Muon_pt")
    .Define("mu0_idx", "ArgMax(good_muon_pt)")
    .Define("mu1_idx", ComplexFunctions::SecondaryIdx, {"good_muon_pt"})
    .Filter("mu0_idx>=0 && mu1_idx>=0") // reject event not able to find secondary muon
    .Define("mu0_pid", "Muon_genPartIdx[mu0_idx]<0 ? -1 : GenPart_pdgId[Muon_genPartIdx[mu0_idx]]")
    .Define("mu1_pid", "Muon_genPartIdx[mu1_idx]<1 ? -1 : GenPart_pdgId[Muon_genPartIdx[mu1_idx]]")
    .Define("Z_4vec", "(mu_4vec[mu0_idx]+mu_4vec[mu1_idx])");

  auto df_output = df_selected
    .Define("Mu0_idx"     , "mu0_idx")
    .Define("Mu1_idx"     , "mu1_idx")
    .Define("Jet0_idx"    , "jet0_idx")
    .Define("good_jets"   , "preselected_jet")

    .Define("Mu0_pt"      , "Muon_pt    [mu0_idx]")
    .Define("Mu0_eta"     , "Muon_eta   [mu0_idx]")
    .Define("Mu0_phi"     , "Muon_phi   [mu0_idx]")
    .Define("Mu1_pt"      , "Muon_pt    [mu1_idx]")
    .Define("Mu1_eta"     , "Muon_eta   [mu1_idx]")
    .Define("Mu1_phi"     , "Muon_phi   [mu1_idx]")
    .Define("isMatched", "abs(mu0_pid)==13 && abs(mu1_pid)==13 && Jet_genJetIdx[0]>=0")
    .Define("Z_mass", "Z_4vec.M()")
    .Define("Z_pt", "Z_4vec.Pt()");


  df_output.Snapshot("Events", outFile, {"good_muon_pt", "mu0_idx", "mu1_idx", "Z_mass", "Z_pt", "isMatched", "Z_pdgid"});
  return;

  std::vector<const char*> output_variables = {
      "Mu0_idx",
      "Mu1_idx",
      "Jet0_idx",
      "good_jets",
      
      "Mu0_pt",
      "Mu0_eta",
      "Mu0_phi",
      "Mu1_pt",
      "Mu1_eta",
      "Mu1_phi",
      "isMatched",
      "Z_mass",
      "Z_pt",

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
      "Jet_svIdx1",
      "Jet_svIdx2",
      "Jet_hfadjacentEtaStripsSize",
      "Jet_hfcentralEtaStripSize",
      "Jet_PNetRegPtRawCorr",
      "Jet_PNetRegPtRawCorrNeutrino",
      "Jet_PNetRegPtRawRes",
      "Jet_area",
      "Jet_btagDeepFlavB",
      "Jet_btagDeepFlavCvB",
      "Jet_btagDeepFlavCvL",
      "Jet_btagDeepFlavQG",
      "Jet_btagPNetB",
      "Jet_btagPNetCvB",
      "Jet_btagPNetCvL",
      "Jet_btagPNetQvG",
      "Jet_btagPNetTauVJet",
      "Jet_btagRobustParTAK4B",
      "Jet_btagRobustParTAK4CvB",
      "Jet_btagRobustParTAK4CvL",
      "Jet_btagRobustParTAK4QG",
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
      "Jet_hadronFlavour",
      "Jet_genJetIdx",
      "Jet_partonFlavour",

      "GenJet_eta",
      "GenJet_mass",
      "GenJet_phi",
      "GenJet_pt",
      "GenJet_hadronFlavour",
      "GenJet_partonFlavour",

      "GenMET_phi",
      "GenMET_pt",
      "MET_MetUnclustEnUpDeltaX",
      "MET_MetUnclustEnUpDeltaY",
      "MET_covXX",
      "MET_covXY",
      "MET_covYY",
      "MET_phi",
      "MET_pt",
      "MET_significance",
      "MET_sumEt",
      "MET_sumPtUnclustered",
      "PuppiMET_phi",
      "PuppiMET_phiJERDown",
      "PuppiMET_phiJERUp",
      "PuppiMET_phiJESDown",
      "PuppiMET_phiJESUp",
      "PuppiMET_phiUnclusteredDown",
      "PuppiMET_phiUnclusteredUp",
      "PuppiMET_pt",
      "PuppiMET_ptJERDown",
      "PuppiMET_ptJERUp",
      "PuppiMET_ptJESDown",
      "PuppiMET_ptJESUp",
      "PuppiMET_ptUnclusteredDown",
      "PuppiMET_ptUnclusteredUp",
      "PuppiMET_sumEt",
      "RawMET_phi",
      "RawMET_pt",
      "RawMET_sumEt",
      "RawPuppiMET_phi",
      "RawPuppiMET_pt",
      "RawPuppiMET_sumEt",
      "TkMET_phi",
      "TkMET_pt",
      "TkMET_sumEt",
      "MET_fiducialGenPhi",
      "MET_fiducialGenPt",
      "Flag_METFilters",

      "genWeight",

      "Pileup_nPU",
      "Pileup_sumEOOT",
      "Pileup_sumLOOT",
      "Pileup_nTrueInt",
      "Pileup_pudensity",
      "Pileup_gpudensity",

      "Jet_nSVs",
      "Tau_nSVs",
      "nSV",
      "SV_charge",
      "SV_dlen",
      "SV_dlenSig",
      "SV_dxy",
      "SV_dxySig",
      "SV_pAngle",
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

      "PV_npvs",
      "PV_npvsGood",

      "nMuon",
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
      "Muon_genPartFlav",
      "Muon_genPartIdx",
  };




  TString outputFILENAME(outFile);
  std::cout << "filtered entries : " << *(df_filtered.Count()) << std::endl;
  df_filtered.Snapshot("Events", outputFILENAME, output_variables);


  TFile *f = new TFile(outputFILENAME,"UPDATE");
  f->cd();



  if ( isMC )
  {
      const double wgt = dfIn.Sum("genWeight").GetValue();
      const double sumEntries = dfIn.Count().GetValue();
      cout<< "Sum weight = "<<wgt<<endl;
      std::cout << "original entries : " << *(dfIn.Count()) << std::endl;
      TH1D *h1 = new TH1D("totWgt","totWgt",2,1,3);
      h1->Fill(1.01,wgt);
      h1->Fill(2.01,sumEntries);
      h1->Write(); // only MC contains this histogram. This histogram will be used to identify Data or MC in further analysis.

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
void DYZllJet(const char* inFILEs, string outFile, bool isMC, const char* dataERA)
{ DYZllJet( splitString(inFILEs,','), outFile, isMC, dataERA ); }

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
  auto iFILE = TFile::Open(inFILE);
  if (!iFILE || iFILE->IsZombie() )
  {
    std::cerr << "[FileNotOpened] Not able to open file : " << inFILE << std::endl;
    return false;
  }
  
  auto iTREE = (TTree*) iFILE->Get("Events");
  if (!iTREE )
  {
    std::cerr << "[InvalidTreeInFile] Tree 'Events' does not exists in file\n";
    return false;
  }

  // if genWeight in branch, it is MC.
  if ( iTREE->GetBranch("genWeight") )
    return true;
  iFILE->Close();
  return false;
}

int main(int argc, const char* argv[])
{
  // usage:
  //   ./exec in1.root,in2.root out.root isMC 2022
  //   arg 1: input root files, separated by comma
  //   arg 2: output root file name
  //   arg 3: data era
  /*
  if ( argc < 3+1 ) { std::cerr << "Input arguments : 1.in root, 2. outroot 3. data era \n\n"; return 1; }
  const char* inFILE = argv[1];
  const char* outFILE = argv[2];
  const char* dataERA = argv[3];
  */

  const char* inFILE = "dySAMPLE.root";
  const char* outFILE = "dyOUTPUT.root";
  const char* dataERA = "2022EE";




  bool is_mc = IsMC_fromFile(inFILE);
  //bool is_mc = ___IsMC___(argv[3]);
  DYZllJet(inFILE,outFILE, is_mc, dataERA);
  //splitString_testfunc(argv);

  return 0;
}
