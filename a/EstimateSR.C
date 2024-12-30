#include "TH1.h"
#include "TH2.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCut.h"
#include "TPaveText.h"
#include "TGaxis.h"
#include "TProfile.h"
#include "TCut.h"
#include "TChain.h"
#include "TString.h"
#include "TGraphErrors.h"
#include "TRandom.h"
#include "TMVA/Factory.h"

#include "TMVA/Reader.h"
#include "TMVA/Config.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/MethodCuts.h"
#include "TString.h"
#include <iostream>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include "TLorentzVector.h"
#include "extlib/correction.h"
#include "extlib/GetPhotonSF.h"
#include "extlib/ExternalFilesMgr.h"

using correction::CorrectionSet;
using namespace std;

double TotalGenWeight(const char* inFILE)
{
  auto tFILE = TFile::Open(inFILE);
  auto hGenW = (TH1D*) tFILE->Get("totWgt");
  if ( hGenW == nullptr ) return -1; // is data
  double totalGenWeight = hGenW->GetBinContent(1);
  tFILE->Close();
  return totalGenWeight;
}

//Photon scale and smearing files
auto cset_photon_scale_smearing_file = CorrectionSet::from_file("data/Photon_scale_smearing.json");
auto cset_scale = cset_photon_scale_smearing_file->at("Prompt2022FG_ScaleJSON");
auto cset_smearing = cset_photon_scale_smearing_file->at("Prompt2022FG_SmearingJSON");

//Jet JEC-JER files
auto cset_jet_jerc_file = CorrectionSet::from_file("data/jet_jerc.json");
correction::Correction::Ref jec_sf_L2;
correction::Correction::Ref jec_sf_L3;
correction::Correction::Ref jec_sf_L23;

int main(int argc, char** argv){
  const bool is_problematic_SS_corr_ = true;
  //std::cout << "hiii\n"; // testing
  if ( is_problematic_SS_corr_ ) std::cout << "Disable SS correction on HoverE due to failed validation\n";
  std::cout << "got file : " << ExternalFilesMgr::RooFile_CTagCalib_DeepCSV("UL2018") << std::endl;
  //std::cout << "hiii enddd\n";

  TChain *tr = new TChain("Events");
  TFile *fout;
  string path;
  string fileName = argv[1];

  double normWgt =1.0;
  double lumi = 1.0;
  bool isSignal = false;
  bool isData = false;
  bool isQCD = false;
  bool isOther = false;
  bool isEraG = false;
  bool isDataSideband = false;
  TFile *fpu;
  //Getting the Pileup SF histos
  fpu = new TFile("data/PileupSF_DYJets_EraEFG.root");
  TH1D *h_pu_nom, *h_pu_up, *h_pu_down;
  if(isData==false){
    h_pu_nom = (TH1D*)fpu->Get("pileupSF_nom");
    //h_pu_up = (TH1D*)fpu->Get("pileupSF_up");
    //h_pu_down = (TH1D*)fpu->Get("pileupSF_down");
  }
  //JEC for MC
  if(isData==false){
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2L3Residual_AK4PFPuppi");
  }
  //Getting the CDFs for Shower shape corrections
  TFile *fss_barrel = new TFile("data/output_ShowerShapeCorrection_barrel_1000Bins.root");
  TFile *fss_endcap = new TFile("data/output_ShowerShapeCorrection_endcap_1000Bins.root");

  if(fileName=="DataE"){
    tr->Add("/eos/home-l/ltsai//public/Run2022E.root");
    fout = new TFile("outfile_dataE_signalregion.root","RECREATE");
    isData = true;
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
  }
  else if(fileName=="DataF"){
    tr->Add("/eos/home-l/ltsai//public/Run2022F.root");
    fout = new TFile("outfile_dataF_signalregion.root","RECREATE");
    isData = true; 
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
  }
  else if(fileName=="DataG"){
    tr->Add("/eos/home-l/ltsai//public/Run2022G.root");
    fout = new TFile("outfile_dataG_signalregion.root","RECREATE");
    isData = true;
    isEraG = true;
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
  }
  else if(fileName=="DataEsideband"){
    tr->Add("/eos/home-l/ltsai//public/Run2022E.root");
    fout = new TFile("outfile_dataE_sideband.root","RECREATE");
    isData = true;
    isDataSideband = true;
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
  }
  else if(fileName=="DataFsideband"){
    tr->Add("/eos/home-l/ltsai//public/Run2022F.root");
    fout = new TFile("outfile_dataF_sideband.root","RECREATE");
    isData = true; 
    isDataSideband = true;
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
  }
  else if(fileName=="DataGsideband"){
    tr->Add("/eos/home-l/ltsai//public/Run2022G.root");
    fout = new TFile("outfile_dataG_sideband.root","RECREATE");
    isData = true;
    isDataSideband = true;
    isEraG = true;
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
  }

  //tr->Add("/eos/home-l/ltsai//public/GJetPythia_20_MGG40to80.root");
  //tr->Add("/eos/home-l/ltsai//public/GJetPythia_20to40_MGG80.root");
  //tr->Add("/eos/home-l/ltsai//public/GJetPythia_40_MGG80.root");



  else if(fileName=="GJets40"){
    const char* inFILE = "/eos/home-l/ltsai//public/G4JetsMadgraph_40to70.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_GmJets_40To70.root","RECREATE");
    normWgt = 1.0*lumi*1000*1.506e+4*1.000000/totGenW;
    //  normWgt = 1.0*lumi*1000*1.506e+4*1.000000/4.0377335e+11;
    //1.506e+04+-1.366e+02

    isSignal = true;
  }
  else if(fileName=="GJets70"){
    const char* inFILE = "/eos/home-l/ltsai//public/G4JetsMadgraph_70to100.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_GmJets_70To100.root","RECREATE");
    normWgt = 1.0*lumi*1000*8.187e+03*1.000000/totGenW;
    //  normWgt = 1.0*lumi*1000*8.187e+03*1.000000/4.0377335e+11;
    //8.187e+03+-7.411e+01

    isSignal = true;
  }
  else if(fileName=="GJets100"){
    const char* inFILE = "/eos/home-l/ltsai//public/G4JetsMadgraph_100to200.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_GmJets_100To200.root","RECREATE");
    normWgt = 1.0*lumi*1000*7.351e+03*1.000000/totGenW;
    //  normWgt = 1.0*lumi*1000*7.351e+03*1.000000/4.0377335e+11;
    //7.351e+03+-6.671e+01

    isSignal = true;
  }
  else if(fileName=="GJets200"){
    const char* inFILE = "/eos/home-l/ltsai//public/G4JetsMadgraph_200to400.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_GmJets_200To400.root","RECREATE");
    normWgt = 1.0*lumi*1000*1548*1.42/totGenW;
    //normWgt = 1.0*lumi*1000*1548*1.42/4.0377335e+11;
    // 1553 +- 14.21
    isSignal = true;
  }
  else if(fileName=="GJets400"){
    const char* inFILE = "/eos/home-l/ltsai//public/G4JetsMadgraph_400to600.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_GmJets_400To600.root","RECREATE");
    normWgt = 1.0*lumi*1000*166.1*1.56/totGenW;
    //normWgt = 1.0*lumi*1000*166.1*1.56/4.8090040e+10;
    // 169.2+-1.57
    isSignal = true;
  }
  else if(fileName=="GJets600"){
    const char* inFILE = "/eos/home-l/ltsai//public/G4JetsMadgraph_600toinf.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_GmJets_600_inf.root","RECREATE");
    normWgt = 1.0*lumi*1000*53.91*1.56/totGenW;
    //normWgt = 1.0*lumi*1000*53.91*1.56/2.4486741e+10;
    // 53.87+-0.5038
    isSignal = true;
  }



  else if(fileName=="QCD70"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_70to100.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_70To100.root","RECREATE");
    normWgt = 1.0*lumi*1000*5.910e+07/totGenW;
    // 5.910e+07 +- 5.258e+05
    isQCD = true;
  }
  else if(fileName=="QCD100"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_100to200.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_100To200.root","RECREATE");
    normWgt = 1.0*lumi*1000*2.502e+07/totGenW;
    // 2.502e+07 +- 2.238e+05
    isQCD = true;
  }
  else if(fileName=="QCD200"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_200to400.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_200To400.root","RECREATE");
    normWgt = 1.0*lumi*1000*1.915e+06/totGenW;
    //normWgt = 1.0*lumi*1000*1.915e+06/6.7668799e+13;
    // 1.915e+06 +- 1.776e+04
    isQCD = true;
  }
  else if(fileName=="QCD400"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_400to600.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_400To600.root","RECREATE");
    normWgt = 1.0*lumi*1000*96000/totGenW;
    //normWgt = 1.0*lumi*1000*96000/6.7668799e+13;
    isQCD = true;
  }
  else if(fileName=="QCD600"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_600to800.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    normWgt = 1.0*lumi*1000*13380/totGenW;
    //normWgt = 1.0*lumi*1000*13380/9.8935244e+12;
    isQCD = true;
  }
  else if(fileName=="QCD800"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_800to1000.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);
    //tr->Add("/eos/home-l/ltsai//public/QCD4JetsMadgraph_800to1200.root"); // indeed this is 800to1000

    fout = new TFile("outfile_QCD_800To1000.root","RECREATE");
    normWgt = 1.0*lumi*1000*3083/totGenW;
    //normWgt = 1.0*lumi*1000*3083/2.4123477e+12;
    isQCD = true;
  }
  else if(fileName=="QCD1000"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_1000to1200.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_1000To1200.root","RECREATE");
    normWgt = 1.0*lumi*1000*877.2/totGenW;
    //normWgt = 1.0*lumi*1000*877.2/7.9361433e+11;
    isQCD = true;
  }
  else if(fileName=="QCD1200"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_1200to1500.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_1200To1500.root","RECREATE");
    normWgt = 1.0*lumi*1000*377.6/totGenW;
    //normWgt = 1.0*lumi*1000*377.6/3.4833910e+11;
    isQCD = true;
  }
  else if(fileName=="QCD1500"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_1500to2000.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_1500To2000.root","RECREATE");
    normWgt = 1.0*lumi*1000*125.2/totGenW;
    //normWgt = 1.0*lumi*1000*125.2/1.0634461e+11;
    isQCD = true;
  }
  else if(fileName=="QCD2000"){
    const char* inFILE = "/eos/home-l/ltsai//public/QCD4JetsMadgraph_2000toinf.root";
    tr->Add(inFILE);
    double totGenW = TotalGenWeight(inFILE);

    fout = new TFile("outfile_QCD_2000.root","RECREATE");
    normWgt = lumi*1000*26.32/totGenW;
    //normWgt = lumi*1000*26.32/2.2450631e+10;
    isQCD = true;
  }
  else if(fileName=="WtoLNu1Jet"){
    path = "Other_MC/WtoLNu1Jet/";
    tr->Add((path+"outFile_WtoLNu_1Jet.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WtoLNu_1Jet.root","RECREATE");
    normWgt = 1.0*lumi*1000*9084/1.2750897e+12;
    isOther = true;
  }
  else if(fileName=="WtoLNu2Jet"){
    path = "Other_MC/WtoLNu2Jet/";
    tr->Add((path+"outFile_WtoLNu_2Jets.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WtoLNu_2Jet.root","RECREATE");
    normWgt = 1.0*lumi*1000*2925/6.3699918e+11;
    isOther = true;
  }
  else if(fileName=="WtoLNu3Jet"){
    path = "Other_MC/WtoLNu3Jet/";
    tr->Add((path+"outFile_WtoLNu_3Jets.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WtoLNu_3Jet.root","RECREATE");
    normWgt = 1.0*lumi*1000*2925/3.2069025e+11;
    isOther = true;
  }
  else if(fileName=="WtoLNu4Jet"){
    path = "Other_MC/WtoLNu4Jet/";
    tr->Add((path+"outFile_WtoLNu_4Jets.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WtoLNu_4Jet.root","RECREATE");
    normWgt = 1.0*lumi*1000*2925/3.5458119e+10;
    isOther = true;
  }
  else if(fileName=="WGto2QG"){
    path = "Other_MC/WGto2QG_PTG200/";
    tr->Add((path+"outFile_WGto2QG_PTG200.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WGto2QG_PTG200.root","RECREATE");
    normWgt = 1.0*lumi*1000*0.6326/3033535.9;
    isOther = true;
  }
  else if(fileName=="WGtoLNuG200"){
    path = "Other_MC/WGtoLNuG_PTG200to400/";
    tr->Add((path+"outFile_WGtoLNuG_PTG200to400.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WGtoLNuG_PTG200to400.root","RECREATE");
    normWgt = 1.0*lumi*1000*0.2908/1441224.4;
    isOther = true;
  }
  else if(fileName=="WGtoLNuG400"){
    path = "Other_MC/WGtoLNuG_PTG400to600/";
    tr->Add((path+"outFile_WGtoLNuG_PTG400to600.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WGtoLNuG_PTG400to600.root","RECREATE");
    normWgt = 1.0*lumi*1000*0.02231/72278.417;
    isOther = true;
  }
  else if(fileName=="WGtoLNuG600"){
    path = "Other_MC/WGtoLNuG_PTG600/";
    tr->Add((path+"outFile_WGtoLNuG_PTG600.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_WGtoLNuG_PTG600.root","RECREATE");
    normWgt = 1.0*lumi*1000*0.004907/8294.4405;
    isOther = true;
  }
  else if(fileName=="DYJets"){
    path = "Other_MC/DYJets/";
    tr->Add((path+"outFile_DYJets.root").c_str());

    //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
    fout = new TFile("outfile_DYJets.root","RECREATE");
    normWgt = 1.0*lumi*1000*5558/94589416;
    isOther = true;
  }
  else if(fileName=="GJetsFlatPt"){
    path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJet_PT-15to6000_Flat/";
    tr->Add((path+"outFile_GmJets_DoubleEMEnriched_PT20_MGG40To80_Final4.root").c_str());
    //tr->Add((path+"outFile_GmJets_DoubleEMEnriched_PT20_MGG40To80_Final3.root").c_str());

    fout = new TFile("outFile_GJetsFlatPt_forCorrMatrix.root","RECREATE");
    normWgt = 1.0*lumi*1000*295100.0/27275.228;
    isSignal = true;
  }
  else if(fileName=="GJetsFlatPt_forVal"){
    path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJet_PT-15to6000_Flat/";
    tr->Add((path+"outFile_GmJets_DoubleEMEnriched_PT20_MGG40To80_Final3.root").c_str());

    fout = new TFile("outFile_GJetsFlatPt_forSomeCheck.root","RECREATE");
    normWgt = 1.0*lumi*1000*295100.0/27275.228;
    isSignal = true;
  }
  else if (fileName=="test1") {
    tr->Add("/afs/cern.ch/user/l/ltsai/eos_storage/condor_storage/G4JetsMadgraph_600toinf/outFile_G4JetsMadgraph_600toinf_0.root");

    fout = new TFile("mytesting_gjetmadgraph.root", "RECREATE");
    normWgt = 1.0;
    isSignal = true;
  }
  else if (fileName=="test2") {
    tr->Add("/afs/cern.ch/user/l/ltsai/eos_storage/condor_storage/QCD4JetsMadgraph_400to600/outFile_QCD4JetsMadgraph_400to600_0.root");

    fout = new TFile("mytesting_qcdmadgraph.root", "RECREATE");
    normWgt = 1.0;
    isQCD = true;
  }
  else if (fileName=="test3") {
    tr->Add("/afs/cern.ch/user/l/ltsai/eos_storage/condor_storage/Run2022E/outFile_Run2022E_0.root");

    fout = new TFile("mytesting_data.root", "RECREATE");
    isData = true; 
    jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
    jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
    jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
  }
  else{
    cout<<"No such sample"<<endl;
    abort();
  }

  // const char* inFILEname = "a.root";
  // tr->Add(inFILEname);
  // 
  // const char* oFILEname = "out.root";
  // fout = new TFile(oFILEname, "RECREATE");
  // normWgt = 1.0;
  // isSignal = false;

#define MAX_PHO 100
#define MAX_JET 130
#define MAX_GENPHO 100
  // Declaration of leaf types
  UInt_t          run;
  UInt_t          luminosityBlock;
  ULong64_t       event;
  UInt_t          bunchCrossing;
  Float_t         PuppiMET_pt;
  Int_t           nPhoton;
  Char_t          Photon_seediEtaOriX[MAX_PHO];   //[nPhoton]
  UChar_t         Photon_cutBased[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_electronVeto[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_hasConversionTracks[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_isScEtaEB[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_isScEtaEE[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_mvaID_WP80[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_mvaID_WP90[MAX_PHO];   //[nPhoton]
  Bool_t          Photon_pixelSeed[MAX_PHO];   //[nPhoton]
  UChar_t         Photon_seedGain[MAX_PHO];   //[nPhoton]
  Short_t         Photon_electronIdx[MAX_PHO];   //[nPhoton]
  Short_t         Photon_jetIdx[MAX_PHO];   //[nPhoton]
  Int_t           Photon_seediPhiOriY[MAX_PHO];   //[nPhoton]
  Int_t           Photon_vidNestedWPBitmap[MAX_PHO];   //[nPhoton]
  Float_t         Photon_ecalPFClusterIso[MAX_PHO];   //[nPhoton]
  Float_t         Photon_energyErr[MAX_PHO];   //[nPhoton]
  Float_t         Photon_energyRaw[MAX_PHO];   //[nPhoton]
  Float_t         Photon_esEffSigmaRR[MAX_PHO];   //[nPhoton]
  Float_t         Photon_esEnergyOverRawE[MAX_PHO];   //[nPhoton]
  Float_t         Photon_eta[MAX_PHO];   //[nPhoton]
  Float_t         Photon_etaWidth[MAX_PHO];   //[nPhoton]
  Float_t         Photon_haloTaggerMVAVal[MAX_PHO];   //[nPhoton]
  Float_t         Photon_hcalPFClusterIso[MAX_PHO];   //[nPhoton]
  Float_t         Photon_hoe[MAX_PHO];   //[nPhoton]
  Float_t         Photon_hoe_PUcorr[MAX_PHO];   //[nPhoton]
  Float_t         Photon_mvaID[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pfChargedIso[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pfChargedIsoPFPV[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pfChargedIsoWorstVtx[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pfPhoIso03[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pfRelIso03_all_quadratic[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pfRelIso03_chg_quadratic[MAX_PHO];   //[nPhoton]
  Float_t         Photon_phi[MAX_PHO];   //[nPhoton]
  Float_t         Photon_phiWidth[MAX_PHO];   //[nPhoton]
  Float_t         Photon_pt[MAX_PHO];   //[nPhoton]
  Float_t         Photon_r9[MAX_PHO];   //[nPhoton]
  Float_t         Photon_s4[MAX_PHO];   //[nPhoton]
  Float_t         Photon_sieie[MAX_PHO];   //[nPhoton]
  Float_t         Photon_sieip[MAX_PHO];   //[nPhoton]
  Float_t         Photon_sipip[MAX_PHO];   //[nPhoton]
  Float_t         Photon_trkSumPtHollowConeDR03[MAX_PHO];   //[nPhoton]
  Float_t         Photon_trkSumPtSolidConeDR04[MAX_PHO];   //[nPhoton]
  Float_t         Photon_x_calo[MAX_PHO];   //[nPhoton]
  Float_t         Photon_y_calo[MAX_PHO];   //[nPhoton]
  Float_t         Photon_z_calo[MAX_PHO];   //[nPhoton]
  Float_t         Photon_MyMVA[MAX_PHO]; 
  Float_t         Rho_fixedGridRhoFastjetAll;
  Bool_t          HLT_Photon200;
  Int_t           nGenIsolatedPhoton;
  Float_t         GenIsolatedPhoton_eta[MAX_GENPHO];   //[nGenIsolatedPhoton]
  Float_t         GenIsolatedPhoton_mass[MAX_GENPHO];   //[nGenIsolatedPhoton]
  Float_t         GenIsolatedPhoton_phi[MAX_GENPHO];   //[nGenIsolatedPhoton]
  Float_t         GenIsolatedPhoton_pt[MAX_GENPHO];   //[nGenIsolatedPhoton]
  Float_t	    genWeight;
  Int_t 	    Pileup_nPU;
  Int_t           nJet;
  UChar_t         Jet_nSVs[MAX_JET];   //[nJet]
  UChar_t         Jet_jetId[MAX_JET];   //[nJet]
  Float_t         Jet_eta[MAX_JET];   //[nJet]
  Float_t         Jet_mass[MAX_JET];   //[nJet]
  Float_t         Jet_phi[MAX_JET];   //[nJet]
  Float_t         Jet_pt[MAX_JET];   //[nJet]
  Float_t         Jet_rawFactor[MAX_JET];   //[nJet]

  // new part
  Short_t         Jet_genJetIdx[MAX_JET];   //[nJet]
  Float_t         Jet_btagPNetB[MAX_JET];   //[nJet]
  Float_t         Jet_btagPNetCvB[MAX_JET];   //[nJet]
  Float_t         Jet_btagPNetCvL[MAX_JET];   //[nJet]
  Float_t         Jet_btagPNetQvG[MAX_JET];   //[nJet]
  Float_t         Jet_btagRobustParTAK4B[MAX_JET];   //[nJet]
  Float_t         Jet_btagRobustParTAK4CvB[MAX_JET];   //[nJet]
  Float_t         Jet_btagRobustParTAK4CvL[MAX_JET];   //[nJet]
  Float_t         Jet_btagRobustParTAK4QG[MAX_JET];   //[nJet]
  Float_t         Jet_btagDeepFlavB[MAX_JET];   //[nJet]
  Float_t         Jet_btagDeepFlavCvB[MAX_JET];   //[nJet]
  Float_t         Jet_btagDeepFlavCvL[MAX_JET];   //[nJet]
  Float_t         Jet_btagDeepFlavQG[MAX_JET];   //[nJet]
                                                 //
  Short_t         Photon_genPartIdx[MAX_PHO];
#define MAX_GENJET 80
  Short_t         GenJet_partonFlavour[MAX_GENJET];   //[nGenJet]
  UChar_t         GenJet_hadronFlavour[MAX_GENJET];   //[nGenJet]
  TBranch        *b_Photon_genPartIdx;
  TBranch        *b_Jet_genJetIdx;   //!


  TBranch        *b_run;   //!
  TBranch        *b_luminosityBlock;   //!
  TBranch        *b_event;   //!
  TBranch        *b_PuppiMET_pt;
  TBranch        *b_bunchCrossing;   //!
  TBranch        *b_nPhoton;   //!
  TBranch        *b_Photon_seediEtaOriX;   //!
  TBranch        *b_Photon_cutBased;   //!
  TBranch        *b_Photon_electronVeto;   //!
  TBranch        *b_Photon_hasConversionTracks;   //!
  TBranch        *b_Photon_isScEtaEB;   //!
  TBranch        *b_Photon_isScEtaEE;   //!
  TBranch        *b_Photon_mvaID_WP80;   //!
  TBranch        *b_Photon_mvaID_WP90;   //!
  TBranch        *b_Photon_pixelSeed;   //!
  TBranch        *b_Photon_seedGain;   //!
  TBranch        *b_Photon_electronIdx;   //!
  TBranch        *b_Photon_jetIdx;   //!
  TBranch        *b_Photon_seediPhiOriY;   //!
  TBranch        *b_Photon_vidNestedWPBitmap;   //!
  TBranch        *b_Photon_ecalPFClusterIso;   //!
  TBranch        *b_Photon_energyErr;   //!
  TBranch        *b_Photon_energyRaw;   //!
  TBranch        *b_Photon_esEffSigmaRR;   //!
  TBranch        *b_Photon_esEnergyOverRawE;   //!
  TBranch        *b_Photon_eta;   //!
  TBranch        *b_Photon_etaWidth;   //!
  TBranch        *b_Photon_haloTaggerMVAVal;   //!
  TBranch        *b_Photon_hcalPFClusterIso;   //!
  TBranch        *b_Photon_hoe;   //!
  TBranch        *b_Photon_hoe_PUcorr;   //!
  TBranch        *b_Photon_mvaID;   //!
  TBranch        *b_Photon_pfChargedIso;   //!
  TBranch        *b_Photon_pfChargedIsoPFPV;   //!
  TBranch        *b_Photon_pfChargedIsoWorstVtx;   //!
  TBranch        *b_Photon_pfPhoIso03;   //!
  TBranch        *b_Photon_pfRelIso03_all_quadratic;   //!
  TBranch        *b_Photon_pfRelIso03_chg_quadratic;   //!
  TBranch        *b_Photon_phi;   //!
  TBranch        *b_Photon_phiWidth;   //!
  TBranch        *b_Photon_pt;   //!
  TBranch        *b_Photon_r9;   //!
  TBranch        *b_Photon_s4;   //!
  TBranch        *b_Photon_sieie;   //!
  TBranch        *b_Photon_sieip;   //!
  TBranch        *b_Photon_sipip;   //!
  TBranch        *b_Photon_trkSumPtHollowConeDR03;   //!
  TBranch        *b_Photon_trkSumPtSolidConeDR04;   //!
  TBranch        *b_Photon_x_calo;   //!
  TBranch        *b_Photon_y_calo;   //!
  TBranch        *b_Photon_z_calo;   //!  
  TBranch        *b_Rho_fixedGridRhoFastjetAll; //!
  TBranch        *b_HLT_Photon200;   //!
  TBranch        *b_nGenIsolatedPhoton;   //!
  TBranch        *b_GenIsolatedPhoton_eta;   //!
  TBranch        *b_GenIsolatedPhoton_mass;   //!
  TBranch        *b_GenIsolatedPhoton_phi;   //!
  TBranch        *b_GenIsolatedPhoton_pt;   //!



  TBranch        *b_Jet_nSVs;   //!
  TBranch        *b_Jet_btagPNetB;   //!
  TBranch        *b_Jet_btagPNetCvB;   //!
  TBranch        *b_Jet_btagPNetCvL;   //!
  TBranch        *b_Jet_btagPNetQvG;   //!
  TBranch        *b_Jet_btagRobustParTAK4B;   //!
  TBranch        *b_Jet_btagRobustParTAK4CvB;   //!
  TBranch        *b_Jet_btagRobustParTAK4CvL;   //!
  TBranch        *b_Jet_btagRobustParTAK4QG;   //!
  TBranch        *b_Jet_btagDeepFlavB;   //!
  TBranch        *b_Jet_btagDeepFlavCvB;   //!
  TBranch        *b_Jet_btagDeepFlavCvL;   //!
  TBranch        *b_Jet_btagDeepFlavQG;   //!
  TBranch        *b_GenJet_partonFlavour;   //!
  TBranch        *b_GenJet_hadronFlavour;   //!



  TBranch        *b_Photon_MyMVA;   //!
  TBranch        *b_genWeight;  //!
  TBranch	  *b_Pileup_nPU; //!
  TBranch        *b_nJet;   //!
  TBranch        *b_Jet_jetId;   //!
  TBranch        *b_Jet_mass;   //!
  TBranch        *b_Jet_eta;   //!
  TBranch        *b_Jet_phi;   //!
  TBranch        *b_Jet_pt;   //!
  TBranch	  *b_Jet_rawFactor;

  tr->SetBranchAddress("run", &run, &b_run);
  tr->SetBranchAddress("luminosityBlock", &luminosityBlock, &b_luminosityBlock);
  tr->SetBranchAddress("event", &event, &b_event);
  tr->SetBranchAddress("bunchCrossing", &bunchCrossing, &b_bunchCrossing); 
  tr->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt, &b_PuppiMET_pt);
  tr->SetBranchAddress("nPhoton", &nPhoton, &b_nPhoton);
  tr->SetBranchAddress("Photon_seediEtaOriX", Photon_seediEtaOriX, &b_Photon_seediEtaOriX);
  tr->SetBranchAddress("Photon_cutBased", Photon_cutBased, &b_Photon_cutBased);
  //tr->SetBranchAddress("Photon_electronVeto", Photon_electronVeto, &b_Photon_electronVeto);
  //tr->SetBranchAddress("Photon_hasConversionTracks", Photon_hasConversionTracks, &b_Photon_hasConversionTracks);
  tr->SetBranchAddress("Photon_isScEtaEB", Photon_isScEtaEB, &b_Photon_isScEtaEB);
  tr->SetBranchAddress("Photon_isScEtaEE", Photon_isScEtaEE, &b_Photon_isScEtaEE);
  tr->SetBranchAddress("Photon_mvaID_WP80", Photon_mvaID_WP80, &b_Photon_mvaID_WP80);
  tr->SetBranchAddress("Photon_mvaID_WP90", Photon_mvaID_WP90, &b_Photon_mvaID_WP90);
  tr->SetBranchAddress("Photon_pixelSeed", Photon_pixelSeed, &b_Photon_pixelSeed);
  tr->SetBranchAddress("Photon_seedGain", Photon_seedGain, &b_Photon_seedGain);
  tr->SetBranchAddress("Photon_electronIdx", Photon_electronIdx, &b_Photon_electronIdx);
  //tr->SetBranchAddress("Photon_jetIdx", Photon_jetIdx, &b_Photon_jetIdx);
  tr->SetBranchAddress("Photon_seediPhiOriY", Photon_seediPhiOriY, &b_Photon_seediPhiOriY);
  tr->SetBranchAddress("Photon_vidNestedWPBitmap", Photon_vidNestedWPBitmap, &b_Photon_vidNestedWPBitmap);
  //tr->SetBranchAddress("Photon_ecalPFClusterIso", Photon_ecalPFClusterIso, &b_Photon_ecalPFClusterIso);
  tr->SetBranchAddress("Photon_energyErr", Photon_energyErr, &b_Photon_energyErr);
  tr->SetBranchAddress("Photon_energyRaw", Photon_energyRaw, &b_Photon_energyRaw);
  tr->SetBranchAddress("Photon_esEffSigmaRR", Photon_esEffSigmaRR, &b_Photon_esEffSigmaRR);
  tr->SetBranchAddress("Photon_esEnergyOverRawE", Photon_esEnergyOverRawE, &b_Photon_esEnergyOverRawE);
  tr->SetBranchAddress("Photon_eta", Photon_eta, &b_Photon_eta);
  tr->SetBranchAddress("Photon_etaWidth", Photon_etaWidth, &b_Photon_etaWidth);
  tr->SetBranchAddress("Photon_haloTaggerMVAVal", Photon_haloTaggerMVAVal, &b_Photon_haloTaggerMVAVal);
  //tr->SetBranchAddress("Photon_hcalPFClusterIso", Photon_hcalPFClusterIso, &b_Photon_hcalPFClusterIso);
  tr->SetBranchAddress("Photon_hoe", Photon_hoe, &b_Photon_hoe);
  tr->SetBranchAddress("Photon_hoe_PUcorr", Photon_hoe_PUcorr, &b_Photon_hoe_PUcorr);
  tr->SetBranchAddress("Photon_mvaID", Photon_mvaID, &b_Photon_mvaID);
  tr->SetBranchAddress("Photon_pfChargedIso", Photon_pfChargedIso, &b_Photon_pfChargedIso);
  tr->SetBranchAddress("Photon_pfChargedIsoPFPV", Photon_pfChargedIsoPFPV, &b_Photon_pfChargedIsoPFPV);
  tr->SetBranchAddress("Photon_pfChargedIsoWorstVtx", Photon_pfChargedIsoWorstVtx, &b_Photon_pfChargedIsoWorstVtx);
  tr->SetBranchAddress("Photon_pfPhoIso03", Photon_pfPhoIso03, &b_Photon_pfPhoIso03);
  tr->SetBranchAddress("Photon_pfRelIso03_all_quadratic", Photon_pfRelIso03_all_quadratic, &b_Photon_pfRelIso03_all_quadratic);
  tr->SetBranchAddress("Photon_pfRelIso03_chg_quadratic", Photon_pfRelIso03_chg_quadratic, &b_Photon_pfRelIso03_chg_quadratic);
  tr->SetBranchAddress("Photon_phi", Photon_phi, &b_Photon_phi);
  tr->SetBranchAddress("Photon_phiWidth", Photon_phiWidth, &b_Photon_phiWidth);
  tr->SetBranchAddress("Photon_pt", Photon_pt, &b_Photon_pt);
  tr->SetBranchAddress("Photon_r9", Photon_r9, &b_Photon_r9);
  tr->SetBranchAddress("Photon_s4", Photon_s4, &b_Photon_s4);
  tr->SetBranchAddress("Photon_sieie", Photon_sieie, &b_Photon_sieie);
  tr->SetBranchAddress("Photon_sieip", Photon_sieip, &b_Photon_sieip);
  tr->SetBranchAddress("Photon_sipip", Photon_sipip, &b_Photon_sipip);
  tr->SetBranchAddress("Photon_trkSumPtHollowConeDR03", Photon_trkSumPtHollowConeDR03, &b_Photon_trkSumPtHollowConeDR03);
  tr->SetBranchAddress("Photon_trkSumPtSolidConeDR04", Photon_trkSumPtSolidConeDR04, &b_Photon_trkSumPtSolidConeDR04);
  tr->SetBranchAddress("Photon_x_calo", Photon_x_calo, &b_Photon_x_calo);
  tr->SetBranchAddress("Photon_y_calo", Photon_y_calo, &b_Photon_y_calo);
  tr->SetBranchAddress("Photon_z_calo", Photon_z_calo, &b_Photon_z_calo);
  tr->SetBranchAddress("Rho_fixedGridRhoFastjetAll", &Rho_fixedGridRhoFastjetAll, &b_Rho_fixedGridRhoFastjetAll);
  tr->SetBranchAddress("nJet", &nJet, &b_nJet);
  tr->SetBranchAddress("Jet_jetId", Jet_jetId, &b_Jet_jetId);
  tr->SetBranchAddress("Jet_mass", Jet_mass, &b_Jet_mass);
  tr->SetBranchAddress("Jet_eta", Jet_eta, &b_Jet_eta);
  tr->SetBranchAddress("Jet_phi", Jet_phi, &b_Jet_phi);
  tr->SetBranchAddress("Jet_pt", Jet_pt, &b_Jet_pt);
  tr->SetBranchAddress("Jet_rawFactor", Jet_rawFactor, &b_Jet_rawFactor);
  tr->SetBranchAddress("HLT_Photon200", &HLT_Photon200, &b_HLT_Photon200);
  if(isData==false){
    tr->SetBranchAddress("nGenIsolatedPhoton", &nGenIsolatedPhoton, &b_nGenIsolatedPhoton);
    tr->SetBranchAddress("GenIsolatedPhoton_eta", GenIsolatedPhoton_eta, &b_GenIsolatedPhoton_eta);
    tr->SetBranchAddress("GenIsolatedPhoton_mass", GenIsolatedPhoton_mass, &b_GenIsolatedPhoton_mass);
    tr->SetBranchAddress("GenIsolatedPhoton_phi", GenIsolatedPhoton_phi, &b_GenIsolatedPhoton_phi);
    tr->SetBranchAddress("GenIsolatedPhoton_pt", GenIsolatedPhoton_pt, &b_GenIsolatedPhoton_pt);
    tr->SetBranchAddress("genWeight", &genWeight, &b_genWeight);
    tr->SetBranchAddress("Pileup_nPU", &Pileup_nPU, &b_Pileup_nPU);
    tr->SetBranchAddress("Photon_genPartIdx", &Photon_genPartIdx, &b_Photon_genPartIdx);
    //tr->SetBranchAddress("Photon_MyMVA", Photon_MyMVA, &b_Photon_MyMVA);

    tr->SetBranchAddress("Jet_genJetIdx", Jet_genJetIdx, &b_Jet_genJetIdx);
    tr->SetBranchAddress("GenJet_partonFlavour", GenJet_partonFlavour, &b_GenJet_partonFlavour);
    tr->SetBranchAddress("GenJet_hadronFlavour", GenJet_hadronFlavour, &b_GenJet_hadronFlavour);
  }
  tr->SetBranchAddress("Jet_btagPNetB", Jet_btagPNetB, &b_Jet_btagPNetB);
  tr->SetBranchAddress("Jet_btagPNetCvB", Jet_btagPNetCvB, &b_Jet_btagPNetCvB);
  tr->SetBranchAddress("Jet_btagPNetCvL", Jet_btagPNetCvL, &b_Jet_btagPNetCvL);
  tr->SetBranchAddress("Jet_btagPNetQvG", Jet_btagPNetQvG, &b_Jet_btagPNetQvG);
  tr->SetBranchAddress("Jet_btagRobustParTAK4B", Jet_btagRobustParTAK4B, &b_Jet_btagRobustParTAK4B);
  tr->SetBranchAddress("Jet_btagRobustParTAK4CvB", Jet_btagRobustParTAK4CvB, &b_Jet_btagRobustParTAK4CvB);
  tr->SetBranchAddress("Jet_btagRobustParTAK4CvL", Jet_btagRobustParTAK4CvL, &b_Jet_btagRobustParTAK4CvL);
  tr->SetBranchAddress("Jet_btagRobustParTAK4QG", Jet_btagRobustParTAK4QG, &b_Jet_btagRobustParTAK4QG);
  tr->SetBranchAddress("Jet_btagDeepFlavB", Jet_btagDeepFlavB, &b_Jet_btagDeepFlavB);
  tr->SetBranchAddress("Jet_btagDeepFlavCvB", Jet_btagDeepFlavCvB, &b_Jet_btagDeepFlavCvB);
  tr->SetBranchAddress("Jet_btagDeepFlavCvL", Jet_btagDeepFlavCvL, &b_Jet_btagDeepFlavCvL);
  tr->SetBranchAddress("Jet_btagDeepFlavQG", Jet_btagDeepFlavQG, &b_Jet_btagDeepFlavQG);


  //Getting the CDFs for Shower shape corrections
  TGraphErrors *grMC_b[10], *grDataInv_b[10];
  TGraphErrors *grMC_e[10], *grDataInv_e[10];

  grMC_b[0] = (TGraphErrors*)fss_barrel->Get("mc_hoe");
  grMC_b[1] = (TGraphErrors*)fss_barrel->Get("mc_sieie");
  grDataInv_b[0] = (TGraphErrors*)fss_barrel->Get("dataInv_hoe");
  grDataInv_b[1] = (TGraphErrors*)fss_barrel->Get("dataInv_sieie");

  grMC_e[0] = (TGraphErrors*)fss_endcap->Get("mc_esEffSigmaRR");
  grMC_e[1] = (TGraphErrors*)fss_endcap->Get("mc_energyRaw");
  grMC_e[2] = (TGraphErrors*)fss_endcap->Get("mc_esEnergyOverRawE");
  grMC_e[3] = (TGraphErrors*)fss_endcap->Get("mc_etaWidth");
  grMC_e[4] = (TGraphErrors*)fss_endcap->Get("mc_hoe");
  grMC_e[5] = (TGraphErrors*)fss_endcap->Get("mc_phiWidth");
  grMC_e[6] = (TGraphErrors*)fss_endcap->Get("mc_r9");
  grMC_e[7] = (TGraphErrors*)fss_endcap->Get("mc_s4");
  grMC_e[8] = (TGraphErrors*)fss_endcap->Get("mc_sieie");
  grMC_e[9] = (TGraphErrors*)fss_endcap->Get("mc_sieip");

  grDataInv_e[0] = (TGraphErrors*)fss_endcap->Get("dataInv_esEffSigmaRR");
  grDataInv_e[1] = (TGraphErrors*)fss_endcap->Get("dataInv_energyRaw");
  grDataInv_e[2] = (TGraphErrors*)fss_endcap->Get("dataInv_esEnergyOverRawE");
  grDataInv_e[3] = (TGraphErrors*)fss_endcap->Get("dataInv_etaWidth");
  grDataInv_e[4] = (TGraphErrors*)fss_endcap->Get("dataInv_hoe");
  grDataInv_e[5] = (TGraphErrors*)fss_endcap->Get("dataInv_phiWidth");
  grDataInv_e[6] = (TGraphErrors*)fss_endcap->Get("dataInv_r9");
  grDataInv_e[7] = (TGraphErrors*)fss_endcap->Get("dataInv_s4");
  grDataInv_e[8] = (TGraphErrors*)fss_endcap->Get("dataInv_sieie");
  grDataInv_e[9] = (TGraphErrors*)fss_endcap->Get("dataInv_sieip");


  //TBranch *b_Photon_MyMVA = tr->Branch("Photon_MyMVA",Photon_MyMVA, "Photon_MyMVA[nPhoton]/F");
  //TBranch *b_passingMVAwp80 = tr->Branch("passingMVAwp80",&passingMVAwp80, "passingMVAwp80/I");
  TH1D *b_PhoPt            = new TH1D( "bALL_Pho_pt","Pho_pt", 75,210,1710);
  TH1D *b_PNetB            = new TH1D( "bALL_PNetB"          ,"PNetB"           , 100, 0.,1.);
  TH1D *b_PNetCvsB         = new TH1D( "bALL_PNetCvsB"       ,"PNetCvsB"        , 100, 0.,1.);
  TH1D *b_PNetCvsL         = new TH1D( "bALL_PNetCvsL"       ,"PNetCvsL"        , 100, 0.,1.);
  TH1D *b_PNetQvsG         = new TH1D( "bALL_PNetQvsG"       ,"PNetQvsG"        , 100, 0.,1.);
  TH1D *b_ParTB            = new TH1D( "bALL_ParTB"          ,"ParTB"           , 100, 0.,1.);
  TH1D *b_ParTCvsB         = new TH1D( "bALL_ParTCvsB"       ,"ParTCvsB"        , 100, 0.,1.);
  TH1D *b_ParTCvsL         = new TH1D( "bALL_ParTCvsL"       ,"ParTCvsL"        , 100, 0.,1.);
  TH1D *b_ParTQvsG         = new TH1D( "bALL_ParTQvsG"       ,"ParTQvsG"        , 100, 0.,1.);
  TH1D *b_DeepFlavourB     = new TH1D( "bALL_DeepFlavourB"   ,"DeepFlavourB"    , 100, 0.,1.);
  TH1D *b_DeepFlavourCvsB  = new TH1D( "bALL_DeepFlavourCvsB","DeepFlavourCvsB" , 100, 0.,1.);
  TH1D *b_DeepFlavourCvsL  = new TH1D( "bALL_DeepFlavourCvsL","DeepFlavourCvsL" , 100, 0.,1.);
  TH1D *b_DeepFlavourQvsG  = new TH1D( "bALL_DeepFlavourQvsG","DeepFlavourQvsG" , 100, 0.,1.);
  TH1D *b_PhoEta           = new TH1D( "bALL_PhoEta","", 100, -4., 4.);
  TH1D *b_PhoPhi           = new TH1D( "bALL_PhoPhi","", 100, -4., 4.);
  TH1D *b_mva              = new TH1D( "b_MyMVA","MyMVA",100, -1,1);
  TH1D *b_HoverE           = new TH1D( "b_HoverE","", 100, 0., 0.05);
  TH1D *b_sieie            = new TH1D( "b_sieie","", 100, 0., 0.05);
  TH1D *b_sieip            = new TH1D( "b_sieip","", 100, -0.001, 0.001);
  TH1D *b_pfChIso          = new TH1D( "b_pfChIso","", 100, 0., 20.);
  TH1D *b_pfChIsoWorstVtx  = new TH1D( "b_pfChIsoWorstVtx","", 100, 0., 20.);
  TH1D *b_r9               = new TH1D( "b_r9","", 100, 0., 5.);
  TH1D *b_s4               = new TH1D( "b_s4","", 100, 0., 2.);
  TH1D *b_phiWidth         = new TH1D( "b_phiWidth","", 100, 0., 0.4);
  TH1D *b_etaWidth         = new TH1D( "b_etaWidth","", 100, 0., 0.15);
  TH1D *b_esEnergyOverRawE = new TH1D( "b_esEnergyOverRawE","", 100, 0., 1.);
  TH1D *b_energyRaw        = new TH1D( "b_energyRaw","", 100, 0., 6000.);
  TH1D *b_esEffSigmaRR     = new TH1D( "b_esEffSigmaRR","", 100, 0., 15.);

  // only used in signal MC, records SS variable without corrections
  TH1D* borig_mva             = new TH1D( "borig_MyMVA","", 100, -1., 1.);
  TH1D* borig_HoverE          = new TH1D( "borig_HoverE","", 100, 0., 0.05);
  TH1D* borig_sieie           = new TH1D( "borig_sieie","", 100, 0., 0.05);
  TH1D* borig_sieip           = new TH1D( "borig_sieip","", 100, -0.001, 0.001);

  TH1D* borig_r9              = new TH1D( "borig_r9","", 100, 0., 5.);
  TH1D* borig_s4              = new TH1D( "borig_s4","", 100, 0., 2.);
  TH1D* borig_phiWidth        = new TH1D( "borig_phiWidth","", 100, 0., 0.4);
  TH1D* borig_etaWidth        = new TH1D( "borig_etaWidth","", 100, 0., 0.15);
  TH1D* borig_esEnergyOverRawE= new TH1D( "borig_esEnergyOverRawE","", 100, 0., 1.);
  TH1D* borig_energyRaw       = new TH1D( "borig_energyRaw","", 100, 0., 6000.);
  TH1D* borig_esEffSigmaRR    = new TH1D( "borig_esEffSigmaRR","", 100, 0., 15.);

  TH1D *e_PhoPt            = new TH1D( "eALL_Pho_pt","Pho_pt", 75,210,1710);
  TH1D *e_PNetB            = new TH1D( "eALL_PNetB"          ,"PNetB"           , 100, 0.,1.);
  TH1D *e_PNetCvsB         = new TH1D( "eALL_PNetCvsB"       ,"PNetCvsB"        , 100, 0.,1.);
  TH1D *e_PNetCvsL         = new TH1D( "eALL_PNetCvsL"       ,"PNetCvsL"        , 100, 0.,1.);
  TH1D *e_PNetQvsG         = new TH1D( "eALL_PNetQvsG"       ,"PNetQvsG"        , 100, 0.,1.);
  TH1D *e_ParTB            = new TH1D( "eALL_ParTB"          ,"ParTB"           , 100, 0.,1.);
  TH1D *e_ParTCvsB         = new TH1D( "eALL_ParTCvsB"       ,"ParTCvsB"        , 100, 0.,1.);
  TH1D *e_ParTCvsL         = new TH1D( "eALL_ParTCvsL"       ,"ParTCvsL"        , 100, 0.,1.);
  TH1D *e_ParTQvsG         = new TH1D( "eALL_ParTQvsG"       ,"ParTQvsG"        , 100, 0.,1.);
  TH1D *e_DeepFlavourB     = new TH1D( "eALL_DeepFlavourB"   ,"DeepFlavourB"    , 100, 0.,1.);
  TH1D *e_DeepFlavourCvsB  = new TH1D( "eALL_DeepFlavourCvsB","DeepFlavourCvsB" , 100, 0.,1.);
  TH1D *e_DeepFlavourCvsL  = new TH1D( "eALL_DeepFlavourCvsL","DeepFlavourCvsL" , 100, 0.,1.);
  TH1D *e_DeepFlavourQvsG  = new TH1D( "eALL_DeepFlavourQvsG","DeepFlavourQvsG" , 100, 0.,1.);
  TH1D *e_PhoEta           = new TH1D( "eALL_PhoEta","", 100, -4., 4.);
  TH1D *e_PhoPhi           = new TH1D( "eALL_PhoPhi","", 100, -4., 4.);

  TH1D *e_mva              = new TH1D( "e_MyMVA","MyMVA",100, -1,1);
  TH1D *e_HoverE           = new TH1D( "e_HoverE","", 100, 0., 0.05);
  TH1D *e_sieie            = new TH1D( "e_sieie","", 100, 0., 0.05);
  TH1D *e_sieip            = new TH1D( "e_sieip","", 100, -0.001, 0.001);
  TH1D *e_pfChIso          = new TH1D( "e_pfChIso","", 100, 0., 20.);
  TH1D *e_pfChIsoWorstVtx  = new TH1D( "e_pfChIsoWorstVtx","", 100, 0., 20.);
  TH1D *e_r9               = new TH1D( "e_r9","", 100, 0., 5.);
  TH1D *e_s4               = new TH1D( "e_s4","", 100, 0., 2.);
  TH1D *e_phiWidth         = new TH1D( "e_phiWidth","", 100, 0., 0.4);
  TH1D *e_etaWidth         = new TH1D( "e_etaWidth","", 100, 0., 0.3);
  TH1D *e_esEnergyOverRawE = new TH1D( "e_esEnergyOverRawE","", 100, 0., 1.);
  TH1D *e_energyRaw        = new TH1D( "e_energyRaw","", 100, 0., 6000.);
  TH1D *e_esEffSigmaRR     = new TH1D( "e_esEffSigmaRR","", 100, 0., 15.);

  TH1D* eorig_mva             = new TH1D( "eorig_MyMVA","", 100, -1., 1.);
  TH1D* eorig_HoverE          = new TH1D( "eorig_HoverE","", 100, 0., 0.05);
  TH1D* eorig_sieie           = new TH1D( "eorig_sieie","", 100, 0., 0.05);
  TH1D* eorig_sieip           = new TH1D( "eorig_sieip","", 100, -0.001, 0.001);

  TH1D* eorig_r9              = new TH1D( "eorig_r9","", 100, 0., 5.);
  TH1D* eorig_s4              = new TH1D( "eorig_s4","", 100, 0., 2.);
  TH1D* eorig_phiWidth        = new TH1D( "eorig_phiWidth","", 100, 0., 0.4);
  TH1D* eorig_etaWidth        = new TH1D( "eorig_etaWidth","", 100, 0., 0.3);
  TH1D* eorig_esEnergyOverRawE= new TH1D( "eorig_esEnergyOverRawE","", 100, 0., 1.);
  TH1D* eorig_energyRaw       = new TH1D( "eorig_energyRaw","", 100, 0., 6000.);
  TH1D* eorig_esEffSigmaRR    = new TH1D( "eorig_esEffSigmaRR","", 100, 0., 15.);

  double photonPt, photonEta, photonPhi, photonMVA, wgt;
  double jetPt, jetEta;
  int jet_nSV;
  double photonPfChargedIsoWorstVtx, photonPfChargedIsoPFPV, photonSieie, photonHoE;
  double genPhotonPt, genPhotonEta, genPhotonPhi;
  double photonMVAorig;
  bool isHadFlvr_C, isHadFlvr_B, isHadFlvr_L;
  double PNetB, PNetCvsB , PNetCvsL , PNetQvsG;
  double ParTB, ParTCvsB , ParTCvsL , ParTQvsG;
  double DeepFlavourB , DeepFlavourCvsB, DeepFlavourCvsL, DeepFlavourQvsG;

  double gjetZmass; // four momentum sum from gamma+jet. Following Z->di-jet but one jet faked into photon.
  double MET;


  TTree *tree = new TTree("tree","tree");
  tree->Branch("photon_pt", &photonPt);
  tree->Branch("photon_eta", &photonEta);
  tree->Branch("photon_phi", &photonPhi);
  tree->Branch("photon_mva", &photonMVA);
  tree->Branch("photon_sieie", &photonSieie);
  tree->Branch("photon_hoe", &photonHoE);
  tree->Branch("photon_pfChargedIsoWorstVtx", &photonPfChargedIsoWorstVtx);
  tree->Branch("photon_pfChargedIsoPFPV", &photonPfChargedIsoPFPV);
  tree->Branch("jet_pt", &jetPt);
  tree->Branch("jet_eta", &jetEta);
  tree->Branch("jet_nSV", &jet_nSV);

  tree->Branch("gjetZmass", &gjetZmass);
  tree->Branch("MET", &MET);
  if (!isData )
  {
    tree->Branch("GenPhoton_pt",&genPhotonPt);
    tree->Branch("GenPhoton_eta",&genPhotonEta);
    tree->Branch("GenPhoton_phi",&genPhotonPhi);
    tree->Branch("wgt", &wgt);
    if ( isSignal)
      tree->Branch("photon_mva_orig", &photonMVAorig);

    tree->Branch("isHadFlvr_C", &isHadFlvr_C);
    tree->Branch("isHadFlvr_B", &isHadFlvr_B);
    tree->Branch("isHadFlvr_L", &isHadFlvr_L);
  }

  tree->Branch("PNetB"           , &PNetB             );
  tree->Branch("PNetCvsB"        , &PNetCvsB          );
  tree->Branch("PNetCvsL"        , &PNetCvsL          );
  tree->Branch("PNetQvsG"        , &PNetQvsG          );
  tree->Branch("ParTB"           , &ParTB             );
  tree->Branch("ParTCvsB"        , &ParTCvsB          );
  tree->Branch("ParTCvsL"        , &ParTCvsL          );
  tree->Branch("ParTQvsG"        , &ParTQvsG          );
  tree->Branch("DeepFlavourB"    , &DeepFlavourB      );
  tree->Branch("DeepFlavourCvsB" , &DeepFlavourCvsB   );
  tree->Branch("DeepFlavourCvsL" , &DeepFlavourCvsL   );
  tree->Branch("DeepFlavourQvsG" , &DeepFlavourQvsG   );


  //Retrieving the BDT score
  TMVA::Reader *reader_barrel = new TMVA::Reader();
  TMVA::Reader *reader_endcap = new TMVA::Reader();
  Float_t photon_esEffSigmaRR;
  Float_t photon_energyRaw;
  Float_t photon_esEnergyOverRawE;
  Float_t photon_etaWidth;
  Float_t photon_hoe;
  Float_t photon_phiWidth;
  Float_t photon_r9;
  Float_t photon_s4;
  Float_t photon_sieie;
  Float_t photon_sieip;
  Float_t photon_rho;
  Float_t photon_eta;
  reader_barrel->AddVariable("photon_esEffSigmaRR", &photon_esEffSigmaRR);
  reader_barrel->AddVariable("photon_energyRaw", &photon_energyRaw);
  reader_barrel->AddVariable("photon_esEnergyOverRawE", &photon_esEnergyOverRawE);
  reader_barrel->AddVariable("photon_etaWidth", &photon_etaWidth);
  reader_barrel->AddVariable("photon_hoe", &photon_hoe);
  reader_barrel->AddVariable("photon_phiWidth", &photon_phiWidth);
  reader_barrel->AddVariable("photon_r9", &photon_r9);
  reader_barrel->AddVariable("photon_s4", &photon_s4);
  reader_barrel->AddVariable("photon_sieie", &photon_sieie);
  reader_barrel->AddVariable("photon_sieip", &photon_sieip);
  reader_barrel->AddVariable("photon_rho", &photon_rho);
  reader_barrel->AddSpectator("photon_eta", &photon_eta);

  reader_endcap->AddVariable("photon_esEffSigmaRR", &photon_esEffSigmaRR);
  reader_endcap->AddVariable("photon_energyRaw", &photon_energyRaw);
  reader_endcap->AddVariable("photon_esEnergyOverRawE", &photon_esEnergyOverRawE);
  reader_endcap->AddVariable("photon_etaWidth", &photon_etaWidth);
  reader_endcap->AddVariable("photon_hoe", &photon_hoe);
  reader_endcap->AddVariable("photon_phiWidth", &photon_phiWidth);
  reader_endcap->AddVariable("photon_r9", &photon_r9);
  reader_endcap->AddVariable("photon_s4", &photon_s4);
  reader_endcap->AddVariable("photon_sieie", &photon_sieie);
  reader_endcap->AddVariable("photon_sieip", &photon_sieip);
  reader_endcap->AddVariable("photon_rho", &photon_rho);
  reader_endcap->AddSpectator("photon_eta", &photon_eta);

  // book the MVA of your choice (prior training of these methods, ie,
  // existence of the weight files is required)
  reader_barrel->BookMVA( "BDT",  "data/TMVAClassification_BDTG.weights_Barrel_original.xml");
  reader_endcap->BookMVA( "BDT",  "data/TMVAClassification_BDTG.weights_Endcap_original.xml");

  //Booking Histograms for Pt and Correlation matrix
  const int NBINSX = 10, NBINSY = 2;
  const int NBINSX_gen = 10, NBINSY_gen = 2;
  float binsX[NBINSX+1] = {210,230,250,300,400,500,600,800,1000,1500,2000};
  float binsY[NBINSY+1] = {0.,1.5,2.5};
  float binsX_gen[NBINSX_gen+1] = {150,210,230,250,300,400,500,600,800,1000,1500};
  float binsY_gen[NBINSY_gen+1] = {0.,1.5,2.5};
  const int NBINSX_corr = 10;
  const int NBINSY_corr = 9;
  float binsX_corr[NBINSX_corr+1] = {210,230,250,300,400,500,600,800,1000,1500,2000};
  float binsY_corr[NBINSY_corr+1] = {210,230,250,300,400,500,600,800,1000,1500};
  TH1D *h_reco_pt[40];
  TH1D *h_gen_pt[40];
  TH2D *h_corrMatrix[4];
  TH1D *h_pt_reco[4];
  TH1D *h_pt_gen[4];
  for(int i=0; i<40; ++i){
    h_reco_pt[i] = new TH1D(Form("recoPt%i",i), Form("recoPt%i",i), NBINSX, binsX);
    h_gen_pt[i] = new TH1D(Form("genPt%i",i), Form("genPt%i",i), NBINSX_gen, binsX_gen);
    //h_corrMatrix[i] = new TH2D(Form("corrMatrix%i",i), Form("corrMatrix%i",i), NBINSX,binsX,NBINSX_gen, binsX_gen);
  }
  for(int i=0; i<4; ++i){
    h_pt_reco[i] = new TH1D(Form("reco_pt%i",i), Form("reco_pt%i",i), NBINSX, binsX);
    h_pt_gen[i] = new TH1D(Form("gen_pt%i",i), Form("gen_pt%i",i), NBINSX_gen, binsX_gen);
    h_corrMatrix[i] = new TH2D(Form("corrMatrix%i",i), Form("corrMatrix%i",i), NBINSX_corr,binsX_corr,NBINSY_corr, binsY_corr);
  }


  //std::cout<<"start looping\n";
  auto nEntries = tr->GetEntries();
  auto iEvent = nEntries;
  iEvent = 0;
  std::cout << "n entries : " << nEntries << std::endl;
  for(iEvent = 0; iEvent< nEntries; ++iEvent){
    tr->GetEntry(iEvent);


    if(iEvent%100000==0){cout<<"Events completed: "<<iEvent<<endl;}
    TLorentzVector recoPho;
    TLorentzVector genPho;
    vector<TLorentzVector> SelPhoton;
    vector<int> SelPhotonIdx;
    vector<TLorentzVector> GenPhoton;
    vector<TLorentzVector> SelJet;
    vector<int> SelJetIdx;
    vector<double> MyPhotonMVA;
    vector<double> SelPhoton_pfChargedIsoPFPV;
    vector<double> SelPhoton_sieie;
    vector<double> SelPhoton_hoe;
    vector<double> SelPhoton_pfChargedIsoWorstVtx;


    vector<TLorentzVector> SelPhotonALL;
    vector<int> SelPhotonIdxALL;
    vector<double> SS_var_photon_esEffSigmaRR;
    vector<double> SS_var_photon_energyRaw;
    vector<double> SS_var_photon_esEnergyOverRawE;
    vector<double> SS_var_photon_etaWidth;
    vector<double> SS_var_photon_hoe;
    vector<double> SS_var_photon_phiWidth;
    vector<double> SS_var_photon_r9;
    vector<double> SS_var_photon_s4;
    vector<double> SS_var_photon_sieie;
    vector<double> SS_var_photon_sieip;
    vector<double> SS_var_photon_rho;
    vector<double> SS_var_photon_eta;

    vector<double> MyPhotonMVA_MC_no_calib;
    for(int ij=0; ij< nPhoton; ++ij)
    {
      if (!isSignal ) if ( HLT_Photon200 == 0 ) continue;

      if(isSignal == true && nGenIsolatedPhoton < 1) continue;
      if(abs(Photon_eta[ij])>2.5) continue;
      if(Photon_pixelSeed[ij]==1)continue;
      if(abs(Photon_eta[ij])>1.4442 && abs(Photon_eta[ij])<1.566) continue;


      if(Photon_pfChargedIsoWorstVtx[ij]>20) continue;
      if(Photon_pfChargedIsoPFPV[ij]>20) continue;
      if(Photon_hoe[ij]>0.05) continue;
      if(abs(Photon_eta[ij])<1.5&&Photon_sieie[ij]>0.015) continue;
      if(abs(Photon_eta[ij])>1.5&&Photon_sieie[ij]>0.04 ) continue;

      bool reco_photon_in_signalregion_or_datasideband = false;
      if (!isDataSideband ) // is signal region
      {
        if(abs(Photon_eta[ij])<1.5 && Photon_pfChargedIsoPFPV[ij]<1.7 && Photon_pfChargedIsoWorstVtx[ij]<10) reco_photon_in_signalregion_or_datasideband = true;
        if(abs(Photon_eta[ij])>1.5 && Photon_pfChargedIsoPFPV[ij]<1.5 && Photon_pfChargedIsoWorstVtx[ij]<10) reco_photon_in_signalregion_or_datasideband = true;
      }
      else  // is data sideband
      {
        if(abs(Photon_eta[ij])<1.5 && Photon_pfChargedIsoPFPV[ij]>7.0) reco_photon_in_signalregion_or_datasideband = true;
        if(abs(Photon_eta[ij])>1.5 && Photon_pfChargedIsoPFPV[ij]>7.0) reco_photon_in_signalregion_or_datasideband = true;
      }


      if(Photon_pt[ij]>700 && Photon_pt[ij]<900 && Photon_seediEtaOriX[ij]+0==-21 && Photon_seediPhiOriY[ij]==260 && isEraG==true) continue; //Only for Era G
                                                                                                                                             //Applying the photon scales and smearing
      Float_t Photon_pt_nom=0;
      if(isData==false){
        //Photon smering is applied on MC
        Float_t rho    = cset_smearing->evaluate({"rho",Photon_eta[ij], Photon_r9[ij]});
        Float_t smearing = gRandom->Gaus(1,rho);
        Photon_pt_nom = Photon_pt[ij]*smearing;
      }
      else{
        //Photon scale is applied on Data
        Float_t Run = run;
        Float_t scale = 1.0*cset_scale->evaluate({"total_correction",Photon_seedGain[ij],Run,Photon_eta[ij],Photon_r9[ij],Photon_pt[ij]});
        Photon_pt_nom = Photon_pt[ij]*scale;
      }
      recoPho.SetPtEtaPhiM(Photon_pt_nom, Photon_eta[ij], Photon_phi[ij],0.);
      if(recoPho.Pt()<210) continue;
      //      std::cout<<"pass all pho selections\n";
      //cout<<Photon_pt_nom<<"	"<<Photon_pt[ij]<<endl;
      //recoPho.SetPtEtaPhiM(Photon_pt[ij], Photon_eta[ij], Photon_phi[ij], 0.);

      photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
      photon_energyRaw = Photon_energyRaw[ij];
      photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
      photon_etaWidth = Photon_etaWidth[ij];
      photon_hoe = Photon_hoe[ij];
      photon_phiWidth = Photon_phiWidth[ij];
      photon_r9 = Photon_r9[ij];
      photon_s4 = Photon_s4[ij];
      photon_sieie = Photon_sieie[ij];
      photon_sieip = Photon_sieip[ij];
      photon_rho = Rho_fixedGridRhoFastjetAll;
      photon_eta = Photon_eta[ij];

      // only reco_photon passing gen requirement would be recorded.
      // data: pass, gjet: pass if reco photon is gen-matched
      // QCD: if event exists gen-photon, pass it if reco photon is gen-matched
      // QCD: if no gen-photon in event, pass it
      bool reco_photon_is_gen_required = false;
      // this block selects source and apply SS corr
      if(isData==true || isOther==true){
        reco_photon_is_gen_required = true;
      }

      if(isSignal == true){

        for(int ik=0; ik< nGenIsolatedPhoton; ++ik){
          genPho.SetPtEtaPhiM(GenIsolatedPhoton_pt[ik], GenIsolatedPhoton_eta[ik], GenIsolatedPhoton_phi[ik], GenIsolatedPhoton_mass[ik]);
          if(recoPho.DeltaR(genPho)> 0.1) continue;
          reco_photon_is_gen_required = true;
          if ( reco_photon_in_signalregion_or_datasideband )
            GenPhoton.push_back(genPho);

          if ( reco_photon_in_signalregion_or_datasideband )
          {
            if(abs(Photon_eta[ij])<1.5)
            {MyPhotonMVA_MC_no_calib.push_back(reader_barrel->EvaluateMVA("BDT"));}
            else
            {MyPhotonMVA_MC_no_calib.push_back(reader_endcap->EvaluateMVA("BDT"));}
            // not calibrated MVA calculation end

            if(abs(Photon_eta[ij])<1.5){ // barrel SS corr
              photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
              photon_energyRaw = Photon_energyRaw[ij];
              photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
              photon_etaWidth = Photon_etaWidth[ij];
              if ( is_problematic_SS_corr_ )
                photon_hoe = Photon_hoe[ij];
              else
                photon_hoe = grDataInv_b[0]->Eval(grMC_b[0]->Eval(Photon_hoe[ij]));
              photon_phiWidth = Photon_phiWidth[ij];
              photon_r9 = Photon_r9[ij];
              photon_s4 = Photon_s4[ij];
              photon_sieie = grDataInv_b[1]->Eval(grMC_b[1]->Eval(Photon_sieie[ij]));
              photon_sieip = Photon_sieip[ij];
              photon_rho = Rho_fixedGridRhoFastjetAll;
              photon_eta = Photon_eta[ij];
            } // end of barrel SS corr
            else{ // endcap SS corr
              photon_esEnergyOverRawE = grDataInv_e[2]->Eval(grMC_e[2]->Eval(Photon_esEnergyOverRawE[ij]));
              photon_etaWidth         = grDataInv_e[3]->Eval(grMC_e[3]->Eval(Photon_etaWidth[ij]));
              if ( is_problematic_SS_corr_ )
              {
                photon_hoe = Photon_hoe[ij];
                photon_esEffSigmaRR     = Photon_esEffSigmaRR[ij];
                photon_energyRaw        = Photon_energyRaw[ij];
                photon_phiWidth         = Photon_phiWidth[ij];
              }
              else
              {
                photon_hoe              = grDataInv_e[4]->Eval(grMC_e[4]->Eval(Photon_hoe[ij]));
                photon_esEffSigmaRR     = grDataInv_e[0]->Eval(grMC_e[0]->Eval(Photon_esEffSigmaRR[ij]));
                photon_energyRaw        = grDataInv_e[1]->Eval(grMC_e[1]->Eval(Photon_energyRaw[ij]));
                photon_phiWidth         = grDataInv_e[5]->Eval(grMC_e[5]->Eval(Photon_phiWidth[ij]));
              }
              photon_r9               = grDataInv_e[6]->Eval(grMC_e[6]->Eval(Photon_r9[ij]));
              photon_s4               = grDataInv_e[7]->Eval(grMC_e[7]->Eval(Photon_s4[ij]));
              photon_sieie            = grDataInv_e[8]->Eval(grMC_e[8]->Eval(Photon_sieie[ij]));
              photon_sieip            = grDataInv_e[9]->Eval(grMC_e[9]->Eval(Photon_sieip[ij]));
              photon_rho              = Rho_fixedGridRhoFastjetAll;
              photon_eta              = Photon_eta[ij];
            } // end of endcap SS corr
            /* orig block
            if(abs(Photon_eta[ij])<1.5){ // barrel SS corr
              photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
              photon_energyRaw = Photon_energyRaw[ij];
              photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
              photon_etaWidth = Photon_etaWidth[ij];
              photon_hoe = grDataInv_b[0]->Eval(grMC_b[0]->Eval(Photon_hoe[ij]));
              photon_phiWidth = Photon_phiWidth[ij];
              photon_r9 = Photon_r9[ij];
              photon_s4 = Photon_s4[ij];
              photon_sieie = grDataInv_b[1]->Eval(grMC_b[1]->Eval(Photon_sieie[ij]));
              photon_sieip = Photon_sieip[ij];
              photon_rho = Rho_fixedGridRhoFastjetAll;
              photon_eta = Photon_eta[ij];
            } // end of barrel SS corr
            else{ // endcap SS corr
              photon_esEffSigmaRR     = grDataInv_e[0]->Eval(grMC_e[0]->Eval(Photon_esEffSigmaRR[ij]));
              photon_energyRaw        = grDataInv_e[1]->Eval(grMC_e[1]->Eval(Photon_energyRaw[ij]));
              photon_esEnergyOverRawE = grDataInv_e[2]->Eval(grMC_e[2]->Eval(Photon_esEnergyOverRawE[ij]));
              photon_etaWidth         = grDataInv_e[3]->Eval(grMC_e[3]->Eval(Photon_etaWidth[ij]));
              photon_hoe              = grDataInv_e[4]->Eval(grMC_e[4]->Eval(Photon_hoe[ij]));
              photon_phiWidth         = grDataInv_e[5]->Eval(grMC_e[5]->Eval(Photon_phiWidth[ij]));
              photon_r9               = grDataInv_e[6]->Eval(grMC_e[6]->Eval(Photon_r9[ij]));
              photon_s4               = grDataInv_e[7]->Eval(grMC_e[7]->Eval(Photon_s4[ij]));
              photon_sieie            = grDataInv_e[8]->Eval(grMC_e[8]->Eval(Photon_sieie[ij]));
              photon_sieip            = grDataInv_e[9]->Eval(grMC_e[9]->Eval(Photon_sieip[ij]));
              photon_rho              = Rho_fixedGridRhoFastjetAll;
              photon_eta              = Photon_eta[ij];
            } // end of endcap SS corr
            orig block */
          }

          break;
        } // end of nGenIsolatedPhoton
      } // end of isSignal

      if ( isQCD ) // Record di-jet event in QCD sample.
        if ( Photon_genPartIdx[ij] < 0 ) reco_photon_is_gen_required = true;

      if ( reco_photon_is_gen_required )
      {
        SelPhotonALL.push_back(recoPho);
        SelPhotonIdxALL.push_back(ij);

        if ( reco_photon_in_signalregion_or_datasideband )
        {
          if(abs(Photon_eta[ij])<1.44)
          {MyPhotonMVA.push_back(reader_barrel->EvaluateMVA("BDT"));}
          else
          {MyPhotonMVA.push_back(reader_endcap->EvaluateMVA("BDT"));}
          if (!isSignal ) MyPhotonMVA_MC_no_calib.push_back(0);

          SelPhoton.push_back(recoPho);
          SelPhotonIdx.push_back(ij);
          SelPhoton_pfChargedIsoPFPV.push_back(Photon_pfChargedIsoPFPV[ij]);
          SelPhoton_sieie.push_back(Photon_sieie[ij]);
          SelPhoton_hoe.push_back(Photon_hoe[ij]);
          SelPhoton_pfChargedIsoWorstVtx.push_back(Photon_pfChargedIsoWorstVtx[ij]);

          SS_var_photon_esEffSigmaRR    .push_back(photon_esEffSigmaRR    );
          SS_var_photon_energyRaw       .push_back(photon_energyRaw       );
          SS_var_photon_esEnergyOverRawE.push_back(photon_esEnergyOverRawE);
          SS_var_photon_etaWidth        .push_back(photon_etaWidth        );
          SS_var_photon_hoe             .push_back(photon_hoe             );
          SS_var_photon_phiWidth        .push_back(photon_phiWidth        );
          SS_var_photon_r9              .push_back(photon_r9              );
          SS_var_photon_s4              .push_back(photon_s4              );
          SS_var_photon_sieie           .push_back(photon_sieie           );
          SS_var_photon_sieip           .push_back(photon_sieip           );
          SS_var_photon_rho             .push_back(photon_rho             );
          SS_var_photon_eta             .push_back(photon_eta             );
        }
      } // end of reco_photon_is_gen_required
    } // loop for ij ( index of isolated photon )
      //    std::cout<<"Passing SelPhoton size\n";

    TLorentzVector jet_raw4v;
    TLorentzVector jet_corr4v;

    int selected_jet_idx_all = -1;
    for(int ij=0; ij<nJet; ++ij){
      //Applying the JEC
      Float_t jet_pt_raw = (1-Jet_rawFactor[ij])*Jet_pt[ij];
      Float_t jet_mass_raw = (1-Jet_rawFactor[ij])*Jet_mass[ij];
      Float_t jet_eta_raw = Jet_eta[ij];
      Float_t jet_phi_raw = Jet_phi[ij];

      Float_t jet_raw_jec_sf_L2 = jec_sf_L2->evaluate({jet_eta_raw,jet_pt_raw});
      Float_t jet_raw_jec_sf_L3 = jec_sf_L3->evaluate({jet_eta_raw,jet_pt_raw*jet_raw_jec_sf_L2});	   
      Float_t jet_raw_sf_L23   = jec_sf_L23->evaluate({jet_eta_raw,jet_pt_raw*jet_raw_jec_sf_L2*jet_raw_jec_sf_L3});

      jet_raw4v.SetPtEtaPhiM(jet_pt_raw, jet_eta_raw, jet_phi_raw, jet_mass_raw);
      jet_corr4v = jet_raw4v*(jet_raw_jec_sf_L2*jet_raw_jec_sf_L3*jet_raw_sf_L23);

      if ( jet_corr4v.Pt()<25 ) continue;
      if ( abs(jet_corr4v.Eta())>2.5 ) continue;
      if ( Jet_jetId[ij]!=6 ) continue;

      if ( SelPhoton.size()>0 )
        if ( jet_corr4v.DeltaR(SelPhoton[0])>0.4 )
        { SelJet.push_back(jet_corr4v); SelJetIdx.push_back(ij); }

      // find a good photon and a good jet matching. (Only first matching jet selected)
      if ( SelPhotonALL.size()>0 )
        if ( jet_corr4v.DeltaR(SelPhotonALL[0])>0.4 && selected_jet_idx_all < 0 )
          selected_jet_idx_all = ij;

    } // end of ij < nJet
      //  std::cout<<"Passing SelJet size\n";

    bool fill_histo = selected_jet_idx_all < 0 ? false : true;

    if ( fill_histo )
    {
      double evt_weight = 1;
      if ( isData==false )
      {
        double pileup_weight = h_pu_nom->GetBinContent(h_pu_nom->FindBin(Pileup_nPU));
        evt_weight = genWeight*normWgt*pileup_weight*GetPhotonSF(SelPhotonALL[0].Pt(), SelPhotonALL[0].Eta(), "nom")*GetTriggerSF(SelPhotonALL[0].Pt(), SelPhotonALL[0].Eta(), "nom");
      }
      // start filling histogram without signal region cut
      float abseta = fabs(Photon_eta[ SelPhotonIdxALL[0] ]);
      float _PNetB               = Jet_btagPNetB[ selected_jet_idx_all ];
      float _PNetCvsB            = Jet_btagPNetCvB[ selected_jet_idx_all ];
      float _PNetCvsL            = Jet_btagPNetCvL[ selected_jet_idx_all ];
      float _PNetQvsG            = Jet_btagPNetQvG[ selected_jet_idx_all ];
      float _ParTB               = Jet_btagRobustParTAK4B[ selected_jet_idx_all ];
      float _ParTCvsB            = Jet_btagRobustParTAK4CvB[ selected_jet_idx_all ];
      float _ParTCvsL            = Jet_btagRobustParTAK4CvL[ selected_jet_idx_all ];
      float _ParTQvsG            = Jet_btagRobustParTAK4QG[ selected_jet_idx_all ];
      float _DeepFlavourB        = Jet_btagDeepFlavB[ selected_jet_idx_all ];
      float _DeepFlavourCvsB     = Jet_btagDeepFlavCvB[ selected_jet_idx_all ];
      float _DeepFlavourCvsL     = Jet_btagDeepFlavCvL[ selected_jet_idx_all ];
      float _DeepFlavourQvsG     = Jet_btagDeepFlavQG[ selected_jet_idx_all ];
      if ( abseta < 1.5 ) // barrel
      {
        b_PhoPt->Fill(SelPhotonALL[0].Pt() , evt_weight);
        b_PNetB            ->Fill( _PNetB          , evt_weight);
        b_PNetCvsB         ->Fill( _PNetCvsB       , evt_weight);
        b_PNetCvsL         ->Fill( _PNetCvsL       , evt_weight);
        b_PNetQvsG         ->Fill( _PNetQvsG       , evt_weight);
        b_ParTB            ->Fill( _ParTB          , evt_weight);
        b_ParTCvsB         ->Fill( _ParTCvsB       , evt_weight);
        b_ParTCvsL         ->Fill( _ParTCvsL       , evt_weight);
        b_ParTQvsG         ->Fill( _ParTQvsG       , evt_weight);
        b_DeepFlavourB     ->Fill( _DeepFlavourB   , evt_weight);
        b_DeepFlavourCvsB  ->Fill( _DeepFlavourCvsB, evt_weight);
        b_DeepFlavourCvsL  ->Fill( _DeepFlavourCvsL, evt_weight);
        b_DeepFlavourQvsG  ->Fill( _DeepFlavourQvsG, evt_weight);
        b_PhoEta           ->Fill( Photon_eta[ SelPhotonIdxALL[0] ], evt_weight); 
        b_PhoPhi           ->Fill( Photon_phi[ SelPhotonIdxALL[0] ], evt_weight); 
        b_pfChIso          ->Fill( Photon_pfChargedIsoPFPV[ SelPhotonIdxALL[0] ], evt_weight); 
        b_pfChIsoWorstVtx  ->Fill( Photon_pfChargedIsoWorstVtx[ SelPhotonIdxALL[0] ], evt_weight); 
      }
      else // endcap
      {
        e_PhoPt->Fill(SelPhotonALL[0].Pt() , evt_weight);
        e_PNetB            ->Fill( _PNetB          , evt_weight);
        e_PNetCvsB         ->Fill( _PNetCvsB       , evt_weight);
        e_PNetCvsL         ->Fill( _PNetCvsL       , evt_weight);
        e_PNetQvsG         ->Fill( _PNetQvsG       , evt_weight);
        e_ParTB            ->Fill( _ParTB          , evt_weight);
        e_ParTCvsB         ->Fill( _ParTCvsB       , evt_weight);
        e_ParTCvsL         ->Fill( _ParTCvsL       , evt_weight);
        e_ParTQvsG         ->Fill( _ParTQvsG       , evt_weight);
        e_DeepFlavourB     ->Fill( _DeepFlavourB   , evt_weight);
        e_DeepFlavourCvsB  ->Fill( _DeepFlavourCvsB, evt_weight);
        e_DeepFlavourCvsL  ->Fill( _DeepFlavourCvsL, evt_weight);
        e_DeepFlavourQvsG  ->Fill( _DeepFlavourQvsG, evt_weight);
        e_PhoEta           ->Fill( Photon_eta[ SelPhotonIdxALL[0] ], evt_weight); 
        e_PhoPhi           ->Fill( Photon_phi[ SelPhotonIdxALL[0] ], evt_weight); 
        e_pfChIso          ->Fill( Photon_pfChargedIsoPFPV[ SelPhotonIdxALL[0] ], evt_weight); 
        e_pfChIsoWorstVtx  ->Fill( Photon_pfChargedIsoWorstVtx[ SelPhotonIdxALL[0] ], evt_weight); 
      }
    } // end of fill_histo


    // sel photon is filtered by reco_photon_in_signalregion_or_datasideband
    if(SelPhoton.size() == 0) continue;
    if(SelJet.size() == 0) continue;

    double wgt_gen = 1;
    if ( isData )
      wgt = 1;
    else
    {
      double puWgt = h_pu_nom->GetBinContent(h_pu_nom->FindBin(Pileup_nPU));
      double phoSF = GetPhotonSF(SelPhoton[0].Pt(), SelPhoton[0].Eta(), "nom");
      double trigSF = GetTriggerSF(SelPhoton[0].Pt(), SelPhoton[0].Eta(), "nom");
      wgt = genWeight*normWgt*puWgt*phoSF*trigSF;
      wgt_gen = genWeight * normWgt;
    }


    photonPt = SelPhoton[0].Pt();
    photonEta = SelPhoton[0].Eta();
    photonPhi = SelPhoton[0].Phi();
    photonMVA = MyPhotonMVA[0];

    photonMVAorig = isSignal ? MyPhotonMVA_MC_no_calib[0] : 0.;

    photonPfChargedIsoWorstVtx = SelPhoton_pfChargedIsoWorstVtx[0];
    photonPfChargedIsoPFPV = SelPhoton_pfChargedIsoPFPV[0];
    photonSieie = SelPhoton_sieie[0];
    photonHoE = SelPhoton_hoe[0];
    jetPt = SelJet[0].Pt();
    jetEta = SelJet[0].Eta();
    jet_nSV = Jet_nSVs[ SelJetIdx[0] ];
    gjetZmass = (SelJet[0]+SelPhoton[0]).M();
    MET = PuppiMET_pt;
    genPhotonPt  = GenPhoton.size()>0 ? GenPhoton[0].Pt()  : -999;
    genPhotonEta = GenPhoton.size()>0 ? GenPhoton[0].Eta() : -999;
    genPhotonPhi = GenPhoton.size()>0 ? GenPhoton[0].Phi() : -999;

    isHadFlvr_C = isData ? false : GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ]==4;
    isHadFlvr_B = isData ? false : GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ]==5;
    isHadFlvr_L = isData ? false : GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ]==0;

    PNetB               = Jet_btagPNetB[ SelJetIdx[0] ];
    PNetCvsB            = Jet_btagPNetCvB[ SelJetIdx[0] ];
    PNetCvsL            = Jet_btagPNetCvL[ SelJetIdx[0] ];
    PNetQvsG            = Jet_btagPNetQvG[ SelJetIdx[0] ];
    ParTB               = Jet_btagRobustParTAK4B[ SelJetIdx[0] ];
    ParTCvsB            = Jet_btagRobustParTAK4CvB[ SelJetIdx[0] ];
    ParTCvsL            = Jet_btagRobustParTAK4CvL[ SelJetIdx[0] ];
    ParTQvsG            = Jet_btagRobustParTAK4QG[ SelJetIdx[0] ];
    DeepFlavourB        = Jet_btagDeepFlavB[ SelJetIdx[0] ];
    DeepFlavourCvsB     = Jet_btagDeepFlavCvB[ SelJetIdx[0] ];
    DeepFlavourCvsL     = Jet_btagDeepFlavCvL[ SelJetIdx[0] ];
    DeepFlavourQvsG     = Jet_btagDeepFlavQG[ SelJetIdx[0] ];

    tree->Fill();

    // fill shower shape distribution, only in signal region or data sideband
    if ( abs(SelPhoton[0].Eta()) < 1.5 )
    {
      b_mva              ->Fill( MyPhotonMVA[0], wgt);
      b_HoverE           ->Fill( SS_var_photon_hoe[0],  wgt); 
      b_sieie            ->Fill( SS_var_photon_sieie[0], wgt); 
      b_sieip            ->Fill( SS_var_photon_sieip[0], wgt); 
      b_r9               ->Fill( SS_var_photon_r9[0], wgt); 
      b_s4               ->Fill( SS_var_photon_s4[0], wgt); 
      b_phiWidth         ->Fill( SS_var_photon_phiWidth[0], wgt); 
      b_etaWidth         ->Fill( SS_var_photon_etaWidth[0], wgt); 
      b_esEnergyOverRawE ->Fill( SS_var_photon_esEnergyOverRawE[0], wgt); 
      b_energyRaw        ->Fill( SS_var_photon_energyRaw[0], wgt); 
      b_esEffSigmaRR     ->Fill( SS_var_photon_esEffSigmaRR[0], wgt); 

      if ( isSignal)
      {
        borig_mva              ->Fill( MyPhotonMVA_MC_no_calib[0], wgt); 
        borig_HoverE           ->Fill( Photon_hoe             [ SelPhotonIdx[0] ], wgt); 
        borig_sieie            ->Fill( Photon_sieie           [ SelPhotonIdx[0] ], wgt); 
        borig_sieip            ->Fill( Photon_sieip           [ SelPhotonIdx[0] ], wgt); 
        borig_r9               ->Fill( Photon_r9              [ SelPhotonIdx[0] ], wgt); 
        borig_s4               ->Fill( Photon_s4              [ SelPhotonIdx[0] ], wgt); 
        borig_phiWidth         ->Fill( Photon_phiWidth        [ SelPhotonIdx[0] ], wgt); 
        borig_etaWidth         ->Fill( Photon_etaWidth        [ SelPhotonIdx[0] ], wgt); 
        borig_esEnergyOverRawE ->Fill( Photon_esEnergyOverRawE[ SelPhotonIdx[0] ], wgt); 
        borig_energyRaw        ->Fill( Photon_energyRaw       [ SelPhotonIdx[0] ], wgt); 
        borig_esEffSigmaRR     ->Fill( Photon_esEffSigmaRR    [ SelPhotonIdx[0] ], wgt); 
      }
    } else {
      e_mva              ->Fill( MyPhotonMVA[0], wgt);
      e_HoverE           ->Fill( SS_var_photon_hoe[0],  wgt); 
      e_sieie            ->Fill( SS_var_photon_sieie[0], wgt); 
      e_sieip            ->Fill( SS_var_photon_sieip[0], wgt); 
      e_r9               ->Fill( SS_var_photon_r9[0], wgt); 
      e_s4               ->Fill( SS_var_photon_s4[0], wgt); 
      e_phiWidth         ->Fill( SS_var_photon_phiWidth[0], wgt); 
      e_etaWidth         ->Fill( SS_var_photon_etaWidth[0], wgt); 
      e_esEnergyOverRawE ->Fill( SS_var_photon_esEnergyOverRawE[0], wgt); 
      e_energyRaw        ->Fill( SS_var_photon_energyRaw[0], wgt); 
      e_esEffSigmaRR     ->Fill( SS_var_photon_esEffSigmaRR[0], wgt); 

      if ( isSignal)
      {
        eorig_mva              ->Fill( MyPhotonMVA_MC_no_calib[0], wgt); 
        eorig_HoverE           ->Fill( Photon_hoe             [ SelPhotonIdx[0] ], wgt); 
        eorig_sieie            ->Fill( Photon_sieie           [ SelPhotonIdx[0] ], wgt); 
        eorig_sieip            ->Fill( Photon_sieip           [ SelPhotonIdx[0] ], wgt); 
        eorig_r9               ->Fill( Photon_r9              [ SelPhotonIdx[0] ], wgt); 
        eorig_s4               ->Fill( Photon_s4              [ SelPhotonIdx[0] ], wgt); 
        eorig_phiWidth         ->Fill( Photon_phiWidth        [ SelPhotonIdx[0] ], wgt); 
        eorig_etaWidth         ->Fill( Photon_etaWidth        [ SelPhotonIdx[0] ], wgt); 
        eorig_esEnergyOverRawE ->Fill( Photon_esEnergyOverRawE[ SelPhotonIdx[0] ], wgt); 
        eorig_energyRaw        ->Fill( Photon_energyRaw       [ SelPhotonIdx[0] ], wgt); 
        eorig_esEffSigmaRR     ->Fill( Photon_esEffSigmaRR    [ SelPhotonIdx[0] ], wgt); 
      }
    }
    // fill shower shape distribution, only in signal region or data sideband end





    if ( GenPhoton.size() > 0 ) {
      if(abs(SelPhoton[0].Eta())<=1.5 && abs(SelJet[0].Eta())<1.5){
        if(GenPhoton[0].Pt()>=210){
          //cout<<SelPhoton[0].Pt()<<endl;
          h_pt_reco[0]->Fill(SelPhoton[0].Pt(),wgt);
          h_pt_gen[0]->Fill(GenPhoton[0].Pt(),wgt_gen);
        }
        if(GenPhoton[0].Pt()<210){h_reco_pt[0]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[0]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[1]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[1]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[2]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[2]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[3]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[3]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[4]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[4]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[5]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[5]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[6]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[6]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[7]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[7]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[8]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[8]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[9]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[9]->Fill(GenPhoton[0].Pt(),wgt);}
      }
      if(abs(SelPhoton[0].Eta())<=1.5 && abs(SelJet[0].Eta())>1.5 && abs(SelJet[0].Eta())<2.5){
        if(GenPhoton[0].Pt()>=210){
          h_pt_reco[1]->Fill(SelPhoton[0].Pt(),wgt);
          h_pt_gen[1]->Fill(GenPhoton[0].Pt(),wgt_gen);
        }
        if(GenPhoton[0].Pt()<210){h_reco_pt[10]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[10]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[11]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[11]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[12]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[12]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[13]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[13]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[14]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[14]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[15]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[15]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[16]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[16]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[17]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[17]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[18]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[18]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[19]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[19]->Fill(GenPhoton[0].Pt(),wgt);}
      }
      if(abs(SelPhoton[0].Eta())>1.5 && abs(SelPhoton[0].Eta())<=2.5 && abs(SelJet[0].Eta())<1.5){
        if(GenPhoton[0].Pt()>=210){
          h_pt_reco[2]->Fill(SelPhoton[0].Pt(),wgt);
          h_pt_gen[2]->Fill(GenPhoton[0].Pt(),wgt_gen);
        }
        if(GenPhoton[0].Pt()<210){h_reco_pt[20]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[20]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[21]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[21]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[22]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[22]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[23]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[23]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[24]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[24]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[25]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[25]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[26]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[26]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[27]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[27]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[28]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[28]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[29]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[29]->Fill(GenPhoton[0].Pt(),wgt);}
      }
      if(abs(SelPhoton[0].Eta())>1.5 && abs(SelPhoton[0].Eta())<=2.5 && abs(SelJet[0].Eta())>1.5 && abs(SelJet[0].Eta())<=2.5){
        if(GenPhoton[0].Pt()>=210){
          h_pt_reco[3]->Fill(SelPhoton[0].Pt(),wgt);
          h_pt_gen[3]->Fill(GenPhoton[0].Pt(),wgt_gen);
        }
        if(GenPhoton[0].Pt()<210){h_reco_pt[30]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[30]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[31]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[31]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[32]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[32]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[33]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[33]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[34]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[34]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[35]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[35]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[36]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[36]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[37]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[37]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[38]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[38]->Fill(GenPhoton[0].Pt(),wgt);}
        if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[39]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[39]->Fill(GenPhoton[0].Pt(),wgt);}
      }
    } // if gen photon size > 0

  }

  for(int j=0;j<NBINSX_gen;++j){
    for(int i=0;i<NBINSX;++i){
      h_corrMatrix[0]->SetBinContent(i+1,j,h_reco_pt[j]->GetBinContent(i+1)/h_gen_pt[j]->Integral());
      h_corrMatrix[0]->SetBinError(i+1,j,h_reco_pt[j]->GetBinError(i+1)/h_gen_pt[j]->Integral());

      h_corrMatrix[1]->SetBinContent(i+1,j,h_reco_pt[j+NBINSX_gen]->GetBinContent(i+1)/h_gen_pt[j+NBINSX_gen]->Integral());
      h_corrMatrix[1]->SetBinError(i+1,j,h_reco_pt[j+NBINSX_gen]->GetBinError(i+1)/h_gen_pt[j+NBINSX_gen]->Integral());

      h_corrMatrix[2]->SetBinContent(i+1,j,h_reco_pt[j+2*NBINSX_gen]->GetBinContent(i+1)/h_gen_pt[j+2*NBINSX_gen]->Integral());
      h_corrMatrix[2]->SetBinError(i+1,j,h_reco_pt[j+2*NBINSX_gen]->GetBinError(i+1)/h_gen_pt[j+2*NBINSX_gen]->Integral());

      h_corrMatrix[3]->SetBinContent(i+1,j,h_reco_pt[j+3*NBINSX_gen]->GetBinContent(i+1)/h_gen_pt[j+3*NBINSX_gen]->Integral());
      h_corrMatrix[3]->SetBinError(i+1,j,h_reco_pt[j+3*NBINSX_gen]->GetBinError(i+1)/h_gen_pt[j+3*NBINSX_gen]->Integral());
    }
  }
  for(int i=1;i<NBINSX+1;++i){
    h_corrMatrix[0]->SetBinContent(i,0,0);
    h_corrMatrix[0]->SetBinError(i,0,0);
    h_corrMatrix[1]->SetBinContent(i,0,0);
    h_corrMatrix[1]->SetBinError(i,0,0);
    h_corrMatrix[2]->SetBinContent(i,0,0);
    h_corrMatrix[2]->SetBinError(i,0,0);
    h_corrMatrix[3]->SetBinContent(i,0,0);
    h_corrMatrix[3]->SetBinError(i,0,0);
  }
  fout->cd();
  for(int i=0; i<4; ++i){
    h_pt_reco[i]->Write();
    h_pt_gen[i]->Write();
    h_corrMatrix[i]->Write();
  }
  for(int i=0; i<40; ++i){
    h_reco_pt[i]->Write();
    h_gen_pt[i]->Write();
  }

  b_mva->Write();
  b_PhoPt->Write();
  b_PNetB           ->Write();
  b_PNetCvsB        ->Write();
  b_PNetCvsL        ->Write();
  b_PNetQvsG        ->Write();
  b_ParTB           ->Write();
  b_ParTCvsB        ->Write();
  b_ParTCvsL        ->Write();
  b_ParTQvsG        ->Write();
  b_DeepFlavourB    ->Write();
  b_DeepFlavourCvsB ->Write();
  b_DeepFlavourCvsL ->Write();
  b_DeepFlavourQvsG ->Write();
  b_PhoEta          ->Write();
  b_PhoPhi          ->Write();
  b_HoverE          ->Write();
  b_sieie           ->Write();
  b_sieip           ->Write();
  b_pfChIso         ->Write();
  b_pfChIsoWorstVtx ->Write();
  b_r9              ->Write();
  b_s4              ->Write();
  b_phiWidth        ->Write();
  b_etaWidth        ->Write();
  b_esEnergyOverRawE->Write();
  b_energyRaw       ->Write();
  b_esEffSigmaRR    ->Write();

  if ( isSignal)
  {
    borig_mva              ->Write();
    borig_HoverE           ->Write();
    borig_sieie            ->Write();
    borig_sieip            ->Write();
    borig_r9               ->Write();
    borig_s4               ->Write();
    borig_phiWidth         ->Write();
    borig_etaWidth         ->Write();
    borig_esEnergyOverRawE ->Write();
    borig_energyRaw        ->Write();
    borig_esEffSigmaRR     ->Write();
  }

  e_mva->Write();
  e_PhoPt->Write();
  e_PNetB           ->Write();
  e_PNetCvsB        ->Write();
  e_PNetCvsL        ->Write();
  e_PNetQvsG        ->Write();
  e_ParTB           ->Write();
  e_ParTCvsB        ->Write();
  e_ParTCvsL        ->Write();
  e_ParTQvsG        ->Write();
  e_DeepFlavourB    ->Write();
  e_DeepFlavourCvsB ->Write();
  e_DeepFlavourCvsL ->Write();
  e_DeepFlavourQvsG ->Write();
  e_PhoEta          ->Write();
  e_PhoPhi          ->Write();
  e_HoverE          ->Write();
  e_sieie           ->Write();
  e_sieip           ->Write();
  e_pfChIso         ->Write();
  e_pfChIsoWorstVtx ->Write();
  e_r9              ->Write();
  e_s4              ->Write();
  e_phiWidth        ->Write();
  e_etaWidth        ->Write();
  e_esEnergyOverRawE->Write();
  e_energyRaw       ->Write();
  e_esEffSigmaRR    ->Write();
  if ( isSignal)
  {
    eorig_mva              ->Write();
    eorig_HoverE           ->Write();
    eorig_sieie            ->Write();
    eorig_sieip            ->Write();
    eorig_r9               ->Write();
    eorig_s4               ->Write();
    eorig_phiWidth         ->Write();
    eorig_etaWidth         ->Write();
    eorig_esEnergyOverRawE ->Write();
    eorig_energyRaw        ->Write();
    eorig_esEffSigmaRR     ->Write();
  }

  tree->Write();
  delete fout;
}
