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
//#include "TMVA/"
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
//#include "/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/py3-correctionlib/2.1.0-d2a3f7d7a03ec004ef7327ef5e29e333/lib/python3.9/site-packages/correctionlib/include/correction.h"
//#include "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GetPhotonSF.h"
#include "extlib/correction.h"

using correction::CorrectionSet;
using namespace std;

//Photon scale and smearing files
auto cset_photon_scale_smearing_file = CorrectionSet::from_file("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/EGmSFs/SS.json");
auto cset_scale = cset_photon_scale_smearing_file->at("Prompt2022FG_ScaleJSON");
auto cset_smearing = cset_photon_scale_smearing_file->at("Prompt2022FG_SmearingJSON");

//Jet JEC-JER files
auto cset_jet_jerc_file = CorrectionSet::from_file("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/EGmSFs/jet_jerc.json");
correction::Correction::Ref jec_sf_L2;
correction::Correction::Ref jec_sf_L3;
correction::Correction::Ref jec_sf_L23;
//For MC 
//jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2Relative_AK4PFPuppi");
//jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L3Absolute_AK4PFPuppi");
//jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2L3Residual_AK4PFPuppi");

int main(int argc, char** argv){
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
TFile *fpu;
//string path_PU = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/Pileup_files/";
//Getting the Pileup SF histos
   fpu = new TFile("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/Pileup_files/PileupSF_DYJets_EraEFG.root");
   TH1D *h_pu_nom, *h_pu_up, *h_pu_down;
   if(isData==false){
    h_pu_nom = (TH1D*)fpu->Get("pileupSF_nom");
    //h_pu_up = (TH1D*)fpu->Get("pileupSF_up");
    //h_pu_down = (TH1D*)fpu->Get("pileupSF_down");
   }
//Getting the CDFs for Shower shape corrections
   TFile *fss_barrel = new TFile("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/TagAndProbe/output_ShowerShapeCorrection_barrel_1000Bins.root");
   TFile *fss_endcap = new TFile("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/TagAndProbe/output_ShowerShapeCorrection_endcap_1000Bins.root");

if(fileName=="DataE"){
  path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/Data/";
  tr->Add((path+"outFile_EGamma2022E.root").c_str());
  fout = new TFile("qcdEstimate/outfile_dataQCD_G.root","RECREATE");
  isData = true;
  jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
  jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
  jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
}
else if(fileName=="DataF"){
  path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/Data/";
  tr->Add((path+"outFile_EGamma2022F_merged_1.root").c_str());
  tr->Add((path+"outFile_EGamma2022F_merged_2.root").c_str());
  tr->Add((path+"outFile_EGamma2022F_merged_3.root").c_str());
  tr->Add((path+"outFile_EGamma2022F_merged_4.root").c_str());
  tr->Add((path+"outFile_EGamma2022F_merged_5.root").c_str());
  fout = new TFile("qcdEstimate/outfile_dataQCD_G.root","RECREATE");
  isData = true; 
  jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi");
  jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi");
  jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
}
if(fileName=="DataG"){
  path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/Data/";
  tr->Add((path+"outFile_EGamma2022G.root").c_str());
  fout = new TFile("qcdEstimate/outfile_dataQCD_G.root","RECREATE");
  isData = true;
  isEraG = true;
  jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi");
  jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi");
  jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
}

else if(fileName=="GJets200"){
  path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJets200/";
  tr->Add((path+"output_GmJets_200To400.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("outfile_GmJets_200To400.root","RECREATE");
  normWgt = 1.0*lumi*1000*1548*1.42/4.0377335e+11;
  isSignal = true;
}
else if(fileName=="GJets400"){
  path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJets400/";
  tr->Add((path+"output_GmJets_400To600_1.root").c_str());
  tr->Add((path+"output_GmJets_400To600_2.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets400To600.root").c_str());
  fout = new TFile("outfile_GmJets_400To600.root","RECREATE");
  normWgt = 1.0*lumi*1000*166.1*1.56/4.8090040e+10;
  isSignal = true;
}
else if(fileName=="GJets600"){
  path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJets600/";
  //tr->Add((path+"output_GmJets_600_1.root").c_str());
  //tr->Add((path+"output_GmJets_600_2.root").c_str());
  //tr->Add((path+"output_GmJets_600_3.root").c_str());
  //tr->Add((path+"output_GmJets_600_4.root").c_str());
  tr->Add((path+"output_GmJets_600_5.root").c_str());
  tr->Add((path+"output_GmJets_600_6.root").c_str());
  tr->Add((path+"output_GmJets_600_7.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets600.root").c_str());
  fout = new TFile("outfile_GmJets_600_1.root","RECREATE");
  normWgt = 1.0*lumi*1000*53.91*1.56/2.4486741e+10;
  isSignal = true;
}
else if(fileName=="QCD400"){
  tr->Add("QCD_MC/QCD400/output_QCD400To600_1_copy.root");
  tr->Add("QCD_MC/QCD400/output_QCD400To600_2_copy.root");

  //fpu = new TFile((path_PU+"PileupSF_QCD400To600.root").c_str());
  fout = new TFile("qcdEstimate/outfile_QCD_400To600.root","RECREATE");
  normWgt = 1.0*lumi*1000*96000/6.7668799e+13;
  isQCD = true;
}
else if(fileName=="QCD600"){
  tr->Add("QCD_MC/QCD600/output_QCD600To800_1.root");
  tr->Add("QCD_MC/QCD600/output_QCD600To800_2.root");
  tr->Add("QCD_MC/QCD600/output_QCD600To800_3.root");
  tr->Add("QCD_MC/QCD600/output_QCD600To800_4.root");
  tr->Add("QCD_MC/QCD600/output_QCD600To800_5.root");
  tr->Add("QCD_MC/QCD600/output_QCD600To800_6.root");

  //fpu = new TFile((path_PU+"PileupSF_QCD600To800.root").c_str());
  fout = new TFile("qcdEstimate/outfile_QCD_600To800.root","RECREATE");
  normWgt = 1.0*lumi*1000*13380/9.8935244e+12;
  isQCD = true;
}
else if(fileName=="QCD800"){
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_1.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_2.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_3.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_4.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_5.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_6.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_7.root");
  tr->Add("QCD_MC/QCD800/output_QCD800To1000_8.root");
 
  //fpu = new TFile((path_PU+"PileupSF_QCD800To1000.root").c_str()); 
  fout = new TFile("qcdEstimate/outfile_QCD_800To1000.root","RECREATE");
  normWgt = 1.0*lumi*1000*3083/2.4123477e+12;
  isQCD = true;
}
else if(fileName=="QCD1000"){
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_1.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_2.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_3.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_4.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_5.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_6.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_7.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_8.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_9.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_10.root");
  tr->Add("QCD_MC/QCD1000/output_QCD1000To1200_11.root");

  //fpu = new TFile((path_PU+"PileupSF_QCD1000To1200.root").c_str());
  fout = new TFile("qcdEstimate/outfile_QCD_1000To1200.root","RECREATE");
  normWgt = 1.0*lumi*1000*877.2/7.9361433e+11;
  isQCD = true;
}
else if(fileName=="QCD1200"){
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_1.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_2.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_3.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_4.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_5.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_6.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_7.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_8.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_9.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_10.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_11.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_12.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_13.root");
  tr->Add("QCD_MC/QCD1200/output_QCD1200To1500_14.root");

  //fpu = new TFile((path_PU+"PileupSF_QCD1200To1500.root").c_str());
  fout = new TFile("qcdEstimate/outfile_QCD_1200To1500.root","RECREATE");
  normWgt = 1.0*lumi*1000*377.6/3.4833910e+11;
  isQCD = true;
}
else if(fileName=="QCD1500"){
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_1.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_2.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_3.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_4.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_5.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_6.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_7.root");
  tr->Add("QCD_MC/QCD1500/output_QCD1500To2000_8.root");

  //fpu = new TFile((path_PU+"PileupSF_QCD1500To2000.root").c_str());
  fout = new TFile("qcdEstimate/outfile_QCD_1500To2000.root","RECREATE");
  normWgt = 1.0*lumi*1000*125.2/1.0634461e+11;
  isQCD = true;
}
else if(fileName=="QCD2000"){
  tr->Add("QCD_MC/QCD2000/output_QCD2000_1.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_2.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_3.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_4.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_5.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_6.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_7.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_8.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_9.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_10.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_11.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_12.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_13.root");
  tr->Add("QCD_MC/QCD2000/output_QCD2000_14.root");

  //fpu = new TFile((path_PU+"PileupSF_QCD2000.root").c_str());
  fout = new TFile("qcdEstimate/outfile_QCD_2000.root","RECREATE");
  normWgt = lumi*1000*26.32/2.2450631e+10;
  isQCD = true;
}
else if(fileName=="WtoLNu1Jet"){
  path = "Other_MC/WtoLNu1Jet/";
  tr->Add((path+"outFile_WtoLNu_1Jet.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WtoLNu_1Jet.root","RECREATE");
  normWgt = 1.0*lumi*1000*9084/1.2750897e+12;
  isOther = true;
}
else if(fileName=="WtoLNu2Jet"){
  path = "Other_MC/WtoLNu2Jet/";
  tr->Add((path+"outFile_WtoLNu_2Jets.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WtoLNu_2Jet.root","RECREATE");
  normWgt = 1.0*lumi*1000*2925/6.3699918e+11;
  isOther = true;
}
else if(fileName=="WtoLNu3Jet"){
  path = "Other_MC/WtoLNu3Jet/";
  tr->Add((path+"outFile_WtoLNu_3Jets.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WtoLNu_3Jet.root","RECREATE");
  normWgt = 1.0*lumi*1000*2925/3.2069025e+11;
  isOther = true;
}
else if(fileName=="WtoLNu4Jet"){
  path = "Other_MC/WtoLNu4Jet/";
  tr->Add((path+"outFile_WtoLNu_4Jets.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WtoLNu_4Jet.root","RECREATE");
  normWgt = 1.0*lumi*1000*2925/3.5458119e+10;
  isOther = true;
}
else if(fileName=="WGto2QG"){
  path = "Other_MC/WGto2QG_PTG200/";
  tr->Add((path+"outFile_WGto2QG_PTG200.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WGto2QG_PTG200.root","RECREATE");
  normWgt = 1.0*lumi*1000*0.6326/3033535.9;
  isOther = true;
}
else if(fileName=="WGtoLNuG200"){
  path = "Other_MC/WGtoLNuG_PTG200to400/";
  tr->Add((path+"outFile_WGtoLNuG_PTG200to400.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WGtoLNuG_PTG200to400.root","RECREATE");
  normWgt = 1.0*lumi*1000*0.2908/1441224.4;
  isOther = true;
}
else if(fileName=="WGtoLNuG400"){
  path = "Other_MC/WGtoLNuG_PTG400to600/";
  tr->Add((path+"outFile_WGtoLNuG_PTG400to600.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WGtoLNuG_PTG400to600.root","RECREATE");
  normWgt = 1.0*lumi*1000*0.02231/72278.417;
  isOther = true;
}
else if(fileName=="WGtoLNuG600"){
  path = "Other_MC/WGtoLNuG_PTG600/";
  tr->Add((path+"outFile_WGtoLNuG_PTG600.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_WGtoLNuG_PTG600.root","RECREATE");
  normWgt = 1.0*lumi*1000*0.004907/8294.4405;
  isOther = true;
}
else if(fileName=="DYJets"){
  path = "Other_MC/DYJets/";
  tr->Add((path+"outFile_DYJets.root").c_str());

  //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
  fout = new TFile("qcdEstimate/outfile_DYJets.root","RECREATE");
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
else{
  cout<<"No such sample"<<endl;
  abort();
}

// Declaration of leaf types
   UInt_t          run;
   UInt_t          luminosityBlock;
   ULong64_t       event;
   UInt_t          bunchCrossing;
   Int_t           nPhoton;
   Char_t          Photon_seediEtaOriX[20];   //[nPhoton]
   UChar_t         Photon_cutBased[20];   //[nPhoton]
   Bool_t          Photon_electronVeto[20];   //[nPhoton]
   Bool_t          Photon_hasConversionTracks[20];   //[nPhoton]
   Bool_t          Photon_isScEtaEB[20];   //[nPhoton]
   Bool_t          Photon_isScEtaEE[20];   //[nPhoton]
   Bool_t          Photon_mvaID_WP80[20];   //[nPhoton]
   Bool_t          Photon_mvaID_WP90[20];   //[nPhoton]
   Bool_t          Photon_pixelSeed[20];   //[nPhoton]
   UChar_t         Photon_seedGain[20];   //[nPhoton]
   Short_t         Photon_electronIdx[20];   //[nPhoton]
   Short_t         Photon_jetIdx[20];   //[nPhoton]
   Int_t           Photon_seediPhiOriY[20];   //[nPhoton]
   Int_t           Photon_vidNestedWPBitmap[20];   //[nPhoton]
   Float_t         Photon_ecalPFClusterIso[20];   //[nPhoton]
   Float_t         Photon_energyErr[20];   //[nPhoton]
   Float_t         Photon_energyRaw[20];   //[nPhoton]
   Float_t         Photon_esEffSigmaRR[20];   //[nPhoton]
   Float_t         Photon_esEnergyOverRawE[20];   //[nPhoton]
   Float_t         Photon_eta[20];   //[nPhoton]
   Float_t         Photon_etaWidth[20];   //[nPhoton]
   Float_t         Photon_haloTaggerMVAVal[20];   //[nPhoton]
   Float_t         Photon_hcalPFClusterIso[20];   //[nPhoton]
   Float_t         Photon_hoe[20];   //[nPhoton]
   Float_t         Photon_hoe_PUcorr[20];   //[nPhoton]
   Float_t         Photon_mvaID[20];   //[nPhoton]
   Float_t         Photon_pfChargedIso[20];   //[nPhoton]
   Float_t         Photon_pfChargedIsoPFPV[20];   //[nPhoton]
   Float_t         Photon_pfChargedIsoWorstVtx[20];   //[nPhoton]
   Float_t         Photon_pfPhoIso03[20];   //[nPhoton]
   Float_t         Photon_pfRelIso03_all_quadratic[20];   //[nPhoton]
   Float_t         Photon_pfRelIso03_chg_quadratic[20];   //[nPhoton]
   Float_t         Photon_phi[20];   //[nPhoton]
   Float_t         Photon_phiWidth[20];   //[nPhoton]
   Float_t         Photon_pt[20];   //[nPhoton]
   Float_t         Photon_r9[20];   //[nPhoton]
   Float_t         Photon_s4[20];   //[nPhoton]
   Float_t         Photon_sieie[20];   //[nPhoton]
   Float_t         Photon_sieip[20];   //[nPhoton]
   Float_t         Photon_sipip[20];   //[nPhoton]
   Float_t         Photon_trkSumPtHollowConeDR03[20];   //[nPhoton]
   Float_t         Photon_trkSumPtSolidConeDR04[20];   //[nPhoton]
   Float_t         Photon_x_calo[20];   //[nPhoton]
   Float_t         Photon_y_calo[20];   //[nPhoton]
   Float_t         Photon_z_calo[20];   //[nPhoton]
   Float_t         Photon_MyMVA[12]; 
   Float_t         Rho_fixedGridRhoFastjetAll;
   Bool_t          HLT_Photon200;
   Int_t           nGenIsolatedPhoton;
   Float_t         GenIsolatedPhoton_eta[10];   //[nGenIsolatedPhoton]
   Float_t         GenIsolatedPhoton_mass[10];   //[nGenIsolatedPhoton]
   Float_t         GenIsolatedPhoton_phi[10];   //[nGenIsolatedPhoton]
   Float_t         GenIsolatedPhoton_pt[10];   //[nGenIsolatedPhoton]
   Float_t	    genWeight;
   Int_t 	    Pileup_nPU;
   Int_t           nJet;
   UChar_t         Jet_jetId[91];   //[nJet]
   Float_t         Jet_eta[91];   //[nJet]
   Float_t         Jet_mass[91];   //[nJet]
   Float_t         Jet_phi[91];   //[nJet]
   Float_t         Jet_pt[91];   //[nJet]
   Float_t         Jet_rawFactor[91];   //[nJet]

   
   TBranch        *b_run;   //!
   TBranch        *b_luminosityBlock;   //!
   TBranch        *b_event;   //!
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
   tr->SetBranchAddress("nPhoton", &nPhoton, &b_nPhoton);
   tr->SetBranchAddress("Photon_seediEtaOriX", Photon_seediEtaOriX, &b_Photon_seediEtaOriX);
   tr->SetBranchAddress("Photon_cutBased", Photon_cutBased, &b_Photon_cutBased);
   tr->SetBranchAddress("Photon_electronVeto", Photon_electronVeto, &b_Photon_electronVeto);
   tr->SetBranchAddress("Photon_hasConversionTracks", Photon_hasConversionTracks, &b_Photon_hasConversionTracks);
   tr->SetBranchAddress("Photon_isScEtaEB", Photon_isScEtaEB, &b_Photon_isScEtaEB);
   tr->SetBranchAddress("Photon_isScEtaEE", Photon_isScEtaEE, &b_Photon_isScEtaEE);
   tr->SetBranchAddress("Photon_mvaID_WP80", Photon_mvaID_WP80, &b_Photon_mvaID_WP80);
   tr->SetBranchAddress("Photon_mvaID_WP90", Photon_mvaID_WP90, &b_Photon_mvaID_WP90);
   tr->SetBranchAddress("Photon_pixelSeed", Photon_pixelSeed, &b_Photon_pixelSeed);
   tr->SetBranchAddress("Photon_seedGain", Photon_seedGain, &b_Photon_seedGain);
   tr->SetBranchAddress("Photon_electronIdx", Photon_electronIdx, &b_Photon_electronIdx);
   tr->SetBranchAddress("Photon_jetIdx", Photon_jetIdx, &b_Photon_jetIdx);
   tr->SetBranchAddress("Photon_seediPhiOriY", Photon_seediPhiOriY, &b_Photon_seediPhiOriY);
   tr->SetBranchAddress("Photon_vidNestedWPBitmap", Photon_vidNestedWPBitmap, &b_Photon_vidNestedWPBitmap);
   tr->SetBranchAddress("Photon_ecalPFClusterIso", Photon_ecalPFClusterIso, &b_Photon_ecalPFClusterIso);
   tr->SetBranchAddress("Photon_energyErr", Photon_energyErr, &b_Photon_energyErr);
   tr->SetBranchAddress("Photon_energyRaw", Photon_energyRaw, &b_Photon_energyRaw);
   tr->SetBranchAddress("Photon_esEffSigmaRR", Photon_esEffSigmaRR, &b_Photon_esEffSigmaRR);
   tr->SetBranchAddress("Photon_esEnergyOverRawE", Photon_esEnergyOverRawE, &b_Photon_esEnergyOverRawE);
   tr->SetBranchAddress("Photon_eta", Photon_eta, &b_Photon_eta);
   tr->SetBranchAddress("Photon_etaWidth", Photon_etaWidth, &b_Photon_etaWidth);
   tr->SetBranchAddress("Photon_haloTaggerMVAVal", Photon_haloTaggerMVAVal, &b_Photon_haloTaggerMVAVal);
   tr->SetBranchAddress("Photon_hcalPFClusterIso", Photon_hcalPFClusterIso, &b_Photon_hcalPFClusterIso);
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
    tr->SetBranchAddress("Photon_MyMVA", Photon_MyMVA, &b_Photon_MyMVA);
   }

//JEC for MC
   if(isData==false){
	jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2Relative_AK4PFPuppi");
	jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L3Absolute_AK4PFPuppi");
	jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2L3Residual_AK4PFPuppi");
   }

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


   Float_t Photon_MyMVA1;
   //TBranch *b_Photon_MyMVA = tr->Branch("Photon_MyMVA",Photon_MyMVA, "Photon_MyMVA[nPhoton]/F");
   //TBranch *b_passingMVAwp80 = tr->Branch("passingMVAwp80",&passingMVAwp80, "passingMVAwp80/I");

   TH1D *h_mva = new TH1D("MyMVA","MyMVA",100, -1,1);
   TH1D *h_PhoPt = new TH1D("Pho_pt","Pho_pt", 75,210,1710);

   double photonPt, photonEta, photonPhi, photonMVA, wgt;
   double jetPt, jetEta;
   double photonPfChargedIsoWorstVtx, photonPfChargedIsoPFPV, photonSieie, photonHoE;
   double genPhotonPt, genPhotonEta, genPhotonPhi;
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
   tree->Branch("GenPhoton_pt",&genPhotonPt);
   tree->Branch("GenPhoton_eta",&genPhotonEta);
   tree->Branch("GenPhoton_phi",&genPhotonPhi);
   tree->Branch("wgt", &wgt);
   
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
      reader_barrel->BookMVA( "BDT",  "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/TMVAClassification_BDTG.weights_Barrel.xml");
      reader_endcap->BookMVA( "BDT",  "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/TMVAClassification_BDTG.weights_Endcap.xml");

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


  int nEntries = tr->GetEntries();
  for(int iEvent = 0; iEvent< nEntries; ++iEvent){
    tr->GetEntry(iEvent);
    if(iEvent%100000==0){cout<<"Events completed: "<<iEvent<<endl;}
    TLorentzVector recoPho;
    TLorentzVector genPho;
    vector<TLorentzVector> SelPhoton;
    vector<TLorentzVector> GenPhoton;
    vector<TLorentzVector> SelJet;
    vector<double> MyPhotonMVA;
    vector<double> SelPhoton_pfChargedIsoPFPV;
    vector<double> SelPhoton_sieie;
    vector<double> SelPhoton_hoe;
    vector<double> SelPhoton_pfChargedIsoWorstVtx;
    for(int ij=0; ij< nPhoton; ++ij){
      if(HLT_Photon200==0) continue;
      if(isSignal == true && nGenIsolatedPhoton < 1) continue;
      if(abs(Photon_eta[ij])>2.5 || Photon_pixelSeed[ij]==1)continue;
      if(abs(Photon_eta[ij])>1.44 && abs(Photon_eta[ij])<1.566) continue;
      if(abs(Photon_eta[ij])<1.44 && (Photon_pfChargedIsoPFPV[ij]>1.7 || Photon_sieie[ij]>0.015 || Photon_hoe[ij]>0.05 || Photon_pfChargedIsoWorstVtx[ij]>10)) continue;
      if(abs(Photon_eta[ij])>1.566 && (Photon_pfChargedIsoPFPV[ij]>1.5 || Photon_sieie[ij]>0.04 || Photon_hoe[ij]>0.05 || Photon_pfChargedIsoWorstVtx[ij]>10)) continue;
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
	//cout<<Photon_pt_nom<<"	"<<Photon_pt[ij]<<endl;
      //recoPho.SetPtEtaPhiM(Photon_pt[ij], Photon_eta[ij], Photon_phi[ij], 0.);
      
      if(isData==true || isOther==true){
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

          if(abs(Photon_eta[ij])<1.44){MyPhotonMVA.push_back(reader_barrel->EvaluateMVA("BDT"));}
          else{MyPhotonMVA.push_back(reader_endcap->EvaluateMVA("BDT"));}

          SelPhoton.push_back(recoPho);
          SelPhoton_pfChargedIsoPFPV.push_back(Photon_pfChargedIsoPFPV[ij]);
          SelPhoton_sieie.push_back(Photon_sieie[ij]);
          SelPhoton_hoe.push_back(Photon_hoe[ij]);
          SelPhoton_pfChargedIsoWorstVtx.push_back(Photon_pfChargedIsoWorstVtx[ij]);

    }
 
      if(isSignal == true){
        for(int ik=0; ik< nGenIsolatedPhoton; ++ik){
          genPho.SetPtEtaPhiM(GenIsolatedPhoton_pt[ik], GenIsolatedPhoton_eta[ik], GenIsolatedPhoton_phi[ik], GenIsolatedPhoton_mass[ik]);
	  if(recoPho.DeltaR(genPho)> 0.1) continue;
	  if(abs(Photon_eta[ij])<1.44){
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

            MyPhotonMVA.push_back(reader_barrel->EvaluateMVA("BDT"));
		SelPhoton_sieie.push_back(photon_sieie);
          	SelPhoton_hoe.push_back(photon_hoe);
	  }
	  
          else{
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

	    	MyPhotonMVA.push_back(reader_endcap->EvaluateMVA("BDT"));
		SelPhoton_sieie.push_back(photon_sieie);
                SelPhoton_hoe.push_back(photon_hoe);
	  }

	  SelPhoton.push_back(recoPho);
	  SelPhoton_pfChargedIsoPFPV.push_back(Photon_pfChargedIsoPFPV[ij]);
	  SelPhoton_pfChargedIsoWorstVtx.push_back(Photon_pfChargedIsoWorstVtx[ij]);
	  GenPhoton.push_back(genPho);
      }
    } // isSignal end

    if(isQCD == true && nGenIsolatedPhoton <1){
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

          if(abs(Photon_eta[ij])<1.44){MyPhotonMVA.push_back(reader_barrel->EvaluateMVA("BDT"));}
          else{MyPhotonMVA.push_back(reader_endcap->EvaluateMVA("BDT"));}

          SelPhoton.push_back(recoPho);
	  SelPhoton_pfChargedIsoPFPV.push_back(Photon_pfChargedIsoPFPV[ij]);
          SelPhoton_sieie.push_back(Photon_sieie[ij]);
          SelPhoton_hoe.push_back(Photon_hoe[ij]);
          SelPhoton_pfChargedIsoWorstVtx.push_back(Photon_pfChargedIsoWorstVtx[ij]);
    }
    
   if(isQCD == true && nGenIsolatedPhoton>0){
        for(int ik=0; ik< nGenIsolatedPhoton; ++ik){
          genPho.SetPtEtaPhiM(GenIsolatedPhoton_pt[ik], GenIsolatedPhoton_eta[ik], GenIsolatedPhoton_phi[ik], GenIsolatedPhoton_mass[ik]);
          if(recoPho.DeltaR(genPho)<= 0.1) continue;
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

          if(abs(Photon_eta[ij])<1.44){MyPhotonMVA.push_back(reader_barrel->EvaluateMVA("BDT"));}
          else{MyPhotonMVA.push_back(reader_endcap->EvaluateMVA("BDT"));}

          SelPhoton.push_back(recoPho);
	  SelPhoton_pfChargedIsoPFPV.push_back(Photon_pfChargedIsoPFPV[ij]);
          SelPhoton_sieie.push_back(Photon_sieie[ij]);
          SelPhoton_hoe.push_back(Photon_hoe[ij]);
          SelPhoton_pfChargedIsoWorstVtx.push_back(Photon_pfChargedIsoWorstVtx[ij]);
      }
    }
  } // loop for ij ( index of isolated photon )
  if(SelPhoton.size()<1) continue;
 
  TLorentzVector jet_raw4v;
  TLorentzVector jet_corr4v;
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

           if(jet_corr4v.Pt()>25 && abs(jet_corr4v.Eta())<2.5 && jet_corr4v.DeltaR(SelPhoton[0])>0.4 && Jet_jetId[ij]==6){
           	SelJet.push_back(jet_corr4v);
      	   }
     }
  if(SelJet.size()<1) continue;
  double wgt_gen;
  if(isData==false){
   double puWgt = h_pu_nom->GetBinContent(h_pu_nom->FindBin(Pileup_nPU));
   wgt = genWeight*normWgt;//*puWgt*GetPhotonSF(SelPhoton[0].Pt(), SelPhoton[0].Eta(),"nom")*GetTriggerSF(SelPhoton[0].Pt(), SelPhoton[0].Eta(),"nom");
   wgt_gen = genWeight*normWgt;
  }
  else{
   wgt = 1;
  }
  photonPt = SelPhoton[0].Pt();
  photonEta = SelPhoton[0].Eta();
  photonPhi = SelPhoton[0].Phi();
  photonMVA = MyPhotonMVA[0];
  photonPfChargedIsoWorstVtx = SelPhoton_pfChargedIsoWorstVtx[0];
  photonPfChargedIsoPFPV = SelPhoton_pfChargedIsoPFPV[0];
  photonSieie = SelPhoton_sieie[0];
  photonHoE = SelPhoton_hoe[0];
  jetPt = SelJet[0].Pt();
  jetEta = SelJet[0].Eta();
  genPhotonPt = GenPhoton[0].Pt();
  genPhotonEta = GenPhoton[0].Eta();
  genPhotonPhi = GenPhoton[0].Phi();
  //tree->Fill();
  h_mva->Fill(MyPhotonMVA[0] , wgt);
  h_PhoPt->Fill(SelPhoton[0].Pt() , wgt);

  //  Filling histograms {{{
  // barrel photon - barrel jet
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
  } // end of barrel photon - barrel jet
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
  } // end of barrel photon - endcap jet
  if(abs(SelPhoton[0].Eta())>1.5 && abs(SelPhoton[0].Eta())<=2.5 && abs(SelJet[0].Eta())<1.5){
	if(GenPhoton[0].Pt()>=210){
		h_pt_reco[2]->Fill(SelPhoton[0].Pt(),wgt);
		h_pt_gen[2]->Fill(GenPhoton[0].Pt(),wgt_gen);
	}
	if(GenPhoton[0].Pt() <210){h_reco_pt[20]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[20]->Fill(GenPhoton[0].Pt(),wgt);}
	if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230 ){h_reco_pt[21]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[21]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250 ){h_reco_pt[22]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[22]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300 ){h_reco_pt[23]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[23]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400 ){h_reco_pt[24]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[24]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500 ){h_reco_pt[25]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[25]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600 ){h_reco_pt[26]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[26]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800 ){h_reco_pt[27]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[27]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[28]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[28]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=1000&& GenPhoton[0].Pt()<1500){h_reco_pt[29]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[29]->Fill(GenPhoton[0].Pt(),wgt);}
  } // end of endcap photon - barrel jet
  if(abs(SelPhoton[0].Eta())>1.5 && abs(SelPhoton[0].Eta())<=2.5 && abs(SelJet[0].Eta())>1.5 && abs(SelJet[0].Eta())<=2.5){
	if(GenPhoton[0].Pt()>=210){
		h_pt_reco[3]->Fill(SelPhoton[0].Pt(),wgt);
		h_pt_gen[3]->Fill(GenPhoton[0].Pt(),wgt_gen);
	}
	if(GenPhoton[0].Pt() <210){h_reco_pt[30]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[30]->Fill(GenPhoton[0].Pt(),wgt);}
	if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230 ){h_reco_pt[31]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[31]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250 ){h_reco_pt[32]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[32]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300 ){h_reco_pt[33]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[33]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400 ){h_reco_pt[34]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[34]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500 ){h_reco_pt[35]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[35]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600 ){h_reco_pt[36]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[36]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800 ){h_reco_pt[37]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[37]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[38]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[38]->Fill(GenPhoton[0].Pt(),wgt);}
  if(GenPhoton[0].Pt()>=1000&& GenPhoton[0].Pt()<1500){h_reco_pt[39]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[39]->Fill(GenPhoton[0].Pt(),wgt);}
  } // end of endcap photon - endcap jet
  //  Filling histograms end }}}
  tree->Fill();
} // end of event looping

// write gen-reco photon pt matrix
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
  h_mva->Write();
  h_PhoPt->Write();
  tree->Write();
  delete fout;
}
