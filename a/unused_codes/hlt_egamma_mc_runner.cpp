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
#include <iostream>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include "TLorentzVector.h"
//#include "/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/py3-correctionlib/2.1.0-d2a3f7d7a03ec004ef7327ef5e29e333/lib/python3.9/site-packages/correctionlib/include/correction.h"
#include "correction.h"
using correction::CorrectionSet;
using namespace std;

auto cset_lead = CorrectionSet::from_file("/afs/cern.ch/work/m/mukherje/public/Hgg_2022_Trigger_jsons/PostEE/merged/TriggerSF_lead_2022_postEE.json");
auto cset_sf_lead = cset_lead->at("TriggerSF");

auto cset_sublead = CorrectionSet::from_file("/afs/cern.ch/work/m/mukherje/public/Hgg_2022_Trigger_jsons/PostEE/merged/TriggerSF_sublead_2022_postEE.json");
auto cset_sf_sublead = cset_sublead->at("TriggerSF");

//void hlt_egamma_mc_runner()
//{
int main(int argc, char** argv)
{
  //TString dir = "ntuples_from_MINIAOD_13_11_2023";
  TString dir = "";

  TString proc_name[] = {"DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8"};
  //TString proc_name[] = {"DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8","GluGluHToGG_M-125_TuneCP5_13p6TeV_powheg-pythia8","DYto2E_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8","GluGluHtoGG_M-125_TuneCP5_13p6TeV_amcatnloFXFX-pythia8"};
  const int nproc = sizeof(proc_name)/sizeof(proc_name[0])-1;
  for(int kk = 0; kk <= nproc ; kk++)
  {
   std::cout << proc_name[kk] << std::endl;
   TFile* final_file = TFile::Open("HIST_"+ proc_name[kk] +".root","RECREATE");
   //Definition of the HIstogram
   TH1F* CMS_hgg_mass = new TH1F("CMS_hgg_mass","",320,60.,140.); 
   TH1F* subleadPt = new TH1F("subleadPt","",80,0,200);
   TH1F* leadPt = new TH1F("leadPt","",80,0,200); 
   TH2F* ptSubVsLead = new TH2F("ptSubVsLead","",180,20,200,180,20,200);
   TH1F* R9_lead = new TH1F("R9_lead","",110,0,1.1);
   TH1F* R9_sublead = new TH1F("R9_sublead","",110,0,1.1);

   float eEta[] = {0.,0.1,0.2,0.3,0.4,0.6,0.8,1.0,1.2,1.4442,1.566,1.7,1.8,2.,2.2,2.3,2.5};
   const int nEta = sizeof(eEta)/sizeof(eEta[0])-1;
   TH1F* Eta_lead = new  TH1F("Eta_lead", "",nEta, eEta);
   TH1F* Eta_sublead = new  TH1F("Eta_sublead","", nEta, eEta);
  
   float x_2d[] = {0.,0.5,0.55,0.6,0.65,0.7,0.74,0.76,0.78,0.8,0.82,0.84,0.86,0.88,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.05,2.};
   const int nx_2d = sizeof(x_2d)/sizeof(x_2d[0])-1;
   float y_2d[] = {0.,0.8,1.,1.2,1.4442,1.566,2,2.5,3.};
   const int ny_2d = sizeof(y_2d)/sizeof(y_2d[0])-1;
   TH2F *R9VsEtaLead = new TH2F("R9VsEtaLead","",nx_2d,x_2d,ny_2d,y_2d);
   TH2F *R9VsEtaSubLead = new TH2F("R9VsEtaSubLead","",nx_2d,x_2d,ny_2d,y_2d);
  
   TH1F *h1 = new TH1F("h1", "", 100, 0.0, 1.0);
   TH1F *h2 = new TH1F("h2", "", 100, 0.0, 1.0);
   TH1F *h3 = new TH1F("h3", "", 100, 0.0, 1.0);
   TH1F *h4 = new TH1F("h4", "", 100, 0.0, 1.0); 
   TH1F *h5 = new TH1F("h5", "", 100, 0.0, 1.0);   
   TH1F *h6 = new TH1F("h6", "", 100, 0.0, 1.0);

   TFile *file = TFile::Open(proc_name[kk] + ".root");
   TTree *mtree = (TTree*)file->Get("mytuple/tree");

   // Declaration of leaf types
   Int_t           nPU;
   Float_t         weight;
   Int_t           nPV;
   Int_t           n_photons;
   vector<float>   *photon_pfPhotonIso;
   vector<float>   *photon_pfChargedHadIso;
   vector<float>   *photon_pfNeutralHadIso;
   vector<float>   *photon_full5x5_sigmaIetaIeta;
   vector<float>   *photon_full5x5_r9;
   vector<float>   *photon_HE;
   vector<float>   *photon_R9;
   vector<float>   *photon_see;
   vector<float>   *photon_sieie;
   vector<int>     *photon_is_gen_matched;
   vector<float>   *photon_mvaID;
   vector<float>   *photon_pt;
   vector<float>   *photon_et;
   vector<float>   *photon_eta;
   vector<float>   *photon_phi;
   vector<float>   *photon_energy;
   vector<float>   *photon_sc_eta;
   vector<float>   *photon_sc_phi;
   vector<float>   *photon_sc_energy;
   vector<float>   *photon_sc_et;
   Int_t           n_electrons;
   vector<float>   *electron_pfPhotonIso;
   vector<float>   *electron_pfChargedHadIso;
   vector<float>   *electron_pfNeutralHadIso;
   vector<float>   *electron_full5x5_sigmaIetaIeta;
   vector<float>   *electron_full5x5_r9;
   vector<float>   *electron_HE;
   vector<float>   *electron_R9;
   vector<float>   *electron_see;
   vector<float>   *electron_sieie;
   vector<int>     *electron_is_gen_matched;
   vector<float>   *electron_mvaID;
   vector<float>   *electron_mvaNoIsoID;
   vector<float>   *electron_pt;
   vector<float>   *electron_eta;
   vector<float>   *electron_phi;
   vector<float>   *electron_energy;
   vector<float>   *electron_pfiso_drcor;
   vector<float>   *electron_pfiso_eacor;
   vector<float>   *electron_pfiso04_eacor;
   vector<float>   *electron_sc_et;
   vector<float>   *electron_sc_energy;
   vector<float>   *electron_sc_eta;
   vector<float>   *electron_sc_phi;
   Int_t           nHLT_lead_egobj;
   vector<float>   *HLT_egobj_lead_pt;
   vector<float>   *HLT_egobj_lead_eta;
   vector<float>   *HLT_egobj_lead_phi;
   vector<float>   *HLT_egobj_lead_energy;
   Int_t           nHLT_subl_egobj;
   vector<float>   *HLT_egobj_subl_pt;
   vector<float>   *HLT_egobj_subl_eta;
   vector<float>   *HLT_egobj_subl_phi;
   vector<float>   *HLT_egobj_subl_energy;
   Bool_t          HLT_SingleEle_30;
   Bool_t          HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90;
   Bool_t          HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95;



   // List of branches
   TBranch        *b_nPU;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_nPV;   //!
   TBranch        *b_n_photons;   //!
   TBranch        *b_photon_pfPhotonIso;   //!
   TBranch        *b_photon_pfChargedHadIso;   //!
   TBranch        *b_photon_pfNeutralHadIso;   //!
   TBranch        *b_photon_full5x5_sigmaIetaIeta;   //!
   TBranch        *b_photon_full5x5_r9;   //!
   TBranch        *b_photon_HE;   //!
   TBranch        *b_photon_R9;   //!
   TBranch        *b_photon_see;   //!
   TBranch        *b_photon_sieie;   //!
   TBranch        *b_photon_is_gen_matched;   //!
   TBranch        *b_photon_mvaID;   //!
   TBranch        *b_photon_pt;   //!
   TBranch        *b_photon_et;   //!
   TBranch        *b_photon_eta;   //!
   TBranch        *b_photon_phi;   //!
   TBranch        *b_photon_energy;   //!
   TBranch        *b_photon_sc_eta;   //!
   TBranch        *b_photon_sc_phi;   //!
   TBranch        *b_photon_sc_energy;   //!
   TBranch        *b_photon_sc_et;   //!
   TBranch        *b_n_electrons;   //!
   TBranch        *b_electron_pfPhotonIso;   //!
   TBranch        *b_electron_pfChargedHadIso;   //!
   TBranch        *b_electron_pfNeutralHadIso;   //!
   TBranch        *b_electron_full5x5_sigmaIetaIeta;   //!
   TBranch        *b_electron_full5x5_r9;   //!
   TBranch        *b_electron_HE;   //!
   TBranch        *b_electron_R9;   //!
   TBranch        *b_electron_see;   //!
   TBranch        *b_electron_sieie;   //!
   TBranch        *b_electron_is_gen_matched;   //!
   TBranch        *b_electron_mvaID;   //!
   TBranch        *b_electron_mvaNoIsoID;   //!
   TBranch        *b_electron_pt;   //!
   TBranch        *b_electron_eta;   //!
   TBranch        *b_electron_phi;   //!
   TBranch        *b_electron_energy;   //!
   TBranch        *b_electron_pfiso_drcor;   //!
   TBranch        *b_electron_pfiso_eacor;   //!
   TBranch        *b_electron_pfiso04_eacor;   //!
   TBranch        *b_electron_sc_et;   //!
   TBranch        *b_electron_sc_energy;   //!
   TBranch        *b_electron_sc_eta;   //!
   TBranch        *b_electron_sc_phi;   //!
   TBranch        *b_nHLT_lead_egobj;   //!
   TBranch        *b_HLT_egobj_lead_pt;   //!
   TBranch        *b_HLT_egobj_lead_eta;   //!
   TBranch        *b_HLT_egobj_lead_phi;   //!
   TBranch        *b_HLT_egobj_lead_energy;   //!
   TBranch        *b_nHLT_subl_egobj;   //!
   TBranch        *b_HLT_egobj_subl_pt;   //!
   TBranch        *b_HLT_egobj_subl_eta;   //!
   TBranch        *b_HLT_egobj_subl_phi;   //!
   TBranch        *b_HLT_egobj_subl_energy;   //!
   TBranch        *b_HLT_SingleEle_30;   //!
   TBranch        *b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90;   //!
   TBranch        *b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95;   //!

   // Set object pointer
   photon_pfPhotonIso = 0;
   photon_pfChargedHadIso = 0;
   photon_pfNeutralHadIso = 0;
   photon_full5x5_sigmaIetaIeta = 0;
   photon_full5x5_r9 = 0;
   photon_HE = 0;
   photon_R9 = 0;
   photon_see = 0;
   photon_sieie = 0;
   photon_is_gen_matched = 0;
   photon_mvaID = 0;
   photon_pt = 0;
   photon_et = 0;
   photon_eta = 0;
   photon_phi = 0;
   photon_energy = 0;
   photon_sc_eta = 0;
   photon_sc_phi = 0;
   photon_sc_energy = 0;
   photon_sc_et = 0;
   electron_pfPhotonIso = 0;
   electron_pfChargedHadIso = 0;
   electron_pfNeutralHadIso = 0;
   electron_full5x5_sigmaIetaIeta = 0;
   electron_full5x5_r9 = 0;
   electron_HE = 0;
   electron_R9 = 0;
   electron_see = 0;
   electron_sieie = 0;
   electron_is_gen_matched = 0;
   electron_mvaID = 0;
   electron_mvaNoIsoID = 0;
   electron_pt = 0;
   electron_eta = 0;
   electron_phi = 0;
   electron_energy = 0;
   electron_pfiso_drcor = 0;
   electron_pfiso_eacor = 0;
   electron_pfiso04_eacor = 0;
   electron_sc_et = 0;
   electron_sc_energy = 0;
   electron_sc_eta = 0;
   electron_sc_phi = 0;
   HLT_egobj_lead_pt = 0;
   HLT_egobj_lead_eta = 0;
   HLT_egobj_lead_phi = 0;
   HLT_egobj_lead_energy = 0;
   HLT_egobj_subl_pt = 0;
   HLT_egobj_subl_eta = 0;
   HLT_egobj_subl_phi = 0;
   HLT_egobj_subl_energy = 0;


   mtree->SetBranchAddress("nPU", &nPU, &b_nPU);
   mtree->SetBranchAddress("weight", &weight, &b_weight);
   mtree->SetBranchAddress("nPV", &nPV, &b_nPV);
   mtree->SetBranchAddress("n_photons", &n_photons, &b_n_photons);
   mtree->SetBranchAddress("photon_pfPhotonIso", &photon_pfPhotonIso, &b_photon_pfPhotonIso);
   mtree->SetBranchAddress("photon_pfChargedHadIso", &photon_pfChargedHadIso, &b_photon_pfChargedHadIso);
   mtree->SetBranchAddress("photon_pfNeutralHadIso", &photon_pfNeutralHadIso, &b_photon_pfNeutralHadIso);
   mtree->SetBranchAddress("photon_full5x5_sigmaIetaIeta", &photon_full5x5_sigmaIetaIeta, &b_photon_full5x5_sigmaIetaIeta);
   mtree->SetBranchAddress("photon_full5x5_r9", &photon_full5x5_r9, &b_photon_full5x5_r9);
   mtree->SetBranchAddress("photon_HE", &photon_HE, &b_photon_HE);
   mtree->SetBranchAddress("photon_R9", &photon_R9, &b_photon_R9);
   mtree->SetBranchAddress("photon_see", &photon_see, &b_photon_see);
   mtree->SetBranchAddress("photon_sieie", &photon_sieie, &b_photon_sieie);
   mtree->SetBranchAddress("photon_is_gen_matched", &photon_is_gen_matched, &b_photon_is_gen_matched);
   mtree->SetBranchAddress("photon_mvaID", &photon_mvaID, &b_photon_mvaID);
   mtree->SetBranchAddress("photon_pt", &photon_pt, &b_photon_pt);
   mtree->SetBranchAddress("photon_et", &photon_et, &b_photon_et);
   mtree->SetBranchAddress("photon_eta", &photon_eta, &b_photon_eta);
   mtree->SetBranchAddress("photon_phi", &photon_phi, &b_photon_phi);
   mtree->SetBranchAddress("photon_energy", &photon_energy, &b_photon_energy);
   mtree->SetBranchAddress("photon_sc_eta", &photon_sc_eta, &b_photon_sc_eta);
   mtree->SetBranchAddress("photon_sc_phi", &photon_sc_phi, &b_photon_sc_phi);
   mtree->SetBranchAddress("photon_sc_energy", &photon_sc_energy, &b_photon_sc_energy);
   mtree->SetBranchAddress("photon_sc_et", &photon_sc_et, &b_photon_sc_et);
   mtree->SetBranchAddress("n_electrons", &n_electrons, &b_n_electrons);
   mtree->SetBranchAddress("electron_pfPhotonIso", &electron_pfPhotonIso, &b_electron_pfPhotonIso);
   mtree->SetBranchAddress("electron_pfChargedHadIso", &electron_pfChargedHadIso, &b_electron_pfChargedHadIso);
   mtree->SetBranchAddress("electron_pfNeutralHadIso", &electron_pfNeutralHadIso, &b_electron_pfNeutralHadIso);
   mtree->SetBranchAddress("electron_full5x5_sigmaIetaIeta", &electron_full5x5_sigmaIetaIeta, &b_electron_full5x5_sigmaIetaIeta);
   mtree->SetBranchAddress("electron_full5x5_r9", &electron_full5x5_r9, &b_electron_full5x5_r9);
   mtree->SetBranchAddress("electron_HE", &electron_HE, &b_electron_HE);
   mtree->SetBranchAddress("electron_R9", &electron_R9, &b_electron_R9);
   mtree->SetBranchAddress("electron_see", &electron_see, &b_electron_see);
   mtree->SetBranchAddress("electron_sieie", &electron_sieie, &b_electron_sieie);
   mtree->SetBranchAddress("electron_is_gen_matched", &electron_is_gen_matched, &b_electron_is_gen_matched);
   mtree->SetBranchAddress("electron_mvaID", &electron_mvaID, &b_electron_mvaID);
   mtree->SetBranchAddress("electron_mvaNoIsoID", &electron_mvaNoIsoID, &b_electron_mvaNoIsoID);
   mtree->SetBranchAddress("electron_pt", &electron_pt, &b_electron_pt);
   mtree->SetBranchAddress("electron_eta", &electron_eta, &b_electron_eta);
   mtree->SetBranchAddress("electron_phi", &electron_phi, &b_electron_phi);
   mtree->SetBranchAddress("electron_energy", &electron_energy, &b_electron_energy);
   mtree->SetBranchAddress("electron_pfiso_drcor", &electron_pfiso_drcor, &b_electron_pfiso_drcor);
   mtree->SetBranchAddress("electron_pfiso_eacor", &electron_pfiso_eacor, &b_electron_pfiso_eacor);
   mtree->SetBranchAddress("electron_pfiso04_eacor", &electron_pfiso04_eacor, &b_electron_pfiso04_eacor);
   mtree->SetBranchAddress("electron_sc_et", &electron_sc_et, &b_electron_sc_et);
   mtree->SetBranchAddress("electron_sc_energy", &electron_sc_energy, &b_electron_sc_energy);
   mtree->SetBranchAddress("electron_sc_eta", &electron_sc_eta, &b_electron_sc_eta);
   mtree->SetBranchAddress("electron_sc_phi", &electron_sc_phi, &b_electron_sc_phi);
   mtree->SetBranchAddress("nHLT_lead_egobj", &nHLT_lead_egobj, &b_nHLT_lead_egobj);
   mtree->SetBranchAddress("HLT_egobj_lead_pt", &HLT_egobj_lead_pt, &b_HLT_egobj_lead_pt);
   mtree->SetBranchAddress("HLT_egobj_lead_eta", &HLT_egobj_lead_eta, &b_HLT_egobj_lead_eta);
   mtree->SetBranchAddress("HLT_egobj_lead_phi", &HLT_egobj_lead_phi, &b_HLT_egobj_lead_phi);
   mtree->SetBranchAddress("HLT_egobj_lead_energy", &HLT_egobj_lead_energy, &b_HLT_egobj_lead_energy);
   mtree->SetBranchAddress("nHLT_subl_egobj", &nHLT_subl_egobj, &b_nHLT_subl_egobj);
   mtree->SetBranchAddress("HLT_egobj_subl_pt", &HLT_egobj_subl_pt, &b_HLT_egobj_subl_pt);
   mtree->SetBranchAddress("HLT_egobj_subl_eta", &HLT_egobj_subl_eta, &b_HLT_egobj_subl_eta);
   mtree->SetBranchAddress("HLT_egobj_subl_phi", &HLT_egobj_subl_phi, &b_HLT_egobj_subl_phi);
   mtree->SetBranchAddress("HLT_egobj_subl_energy", &HLT_egobj_subl_energy, &b_HLT_egobj_subl_energy);
   //mtree->SetBranchAddress("HLT_SingleEle_30", &HLT_SingleEle_30, &b_HLT_SingleEle_30);
   mtree->SetBranchAddress("HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90", &HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90, &b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90);
   mtree->SetBranchAddress("HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95", &HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95, &b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95);

   //starting the tree reader
   Long64_t nn = mtree->GetEntries();
   for(Long64_t j =0; j < nn ; j++)
          {
                mtree->GetEntry(j);
                if(j%10000 == 0) std::cout << j << " --> events processed" << std::endl;
                for(int ii= 0; ii < n_photons-1; ii++)
                {
                        // cut region
                        if(photon_full5x5_r9->at(ii) < 0.5 ) continue; 
                        if(  (fabs(photon_sc_eta->at(ii))>= 1.4442 && fabs(photon_sc_eta->at(ii)) <= 1.566) || fabs(photon_sc_eta->at(ii))>=2.5) continue; 
                        if(photon_pt->at(ii) < 30.0 ) continue;
                        if(photon_mvaID->at(ii) < -0.9) continue;
                        if(photon_full5x5_r9->at(ii) > 1.1) continue;
                        if(photon_HE->at(ii) > 0.08 ) continue;
                        if(photon_full5x5_r9->at(ii) < 0.8 && photon_pfChargedHadIso->at(ii) > 20 && photon_pfChargedHadIso->at(ii)/photon_pt->at(ii) > 0.3 ) continue;
                        for(int jj= ii+1; jj < n_photons; jj++)
                        {
                               if(photon_full5x5_r9->at(jj) < 0.5 ) continue; 
                               if(  (fabs(photon_sc_eta->at(jj))>= 1.4442 && fabs(photon_sc_eta->at(jj)) <= 1.566) || fabs(photon_sc_eta->at(jj))>=2.5) continue;
                               if(photon_pt->at(jj) < 20.0 ) continue;
                               if(photon_mvaID->at(jj) < -0.9) continue;
                               if(photon_HE->at(jj) > 0.08 ) continue;
                               if(photon_full5x5_r9->at(jj) > 1.1) continue;
                               if(photon_full5x5_r9->at(jj) < 0.8 && photon_pfChargedHadIso->at(jj) > 20 && photon_pfChargedHadIso->at(jj)/photon_pt->at(jj) > 0.3 ) continue;
                               TLorentzVector photon1, photon2;
                               photon1.SetPtEtaPhiM(photon_pt->at(ii),photon_eta->at(ii),photon_phi->at(ii),0.0);
                               photon2.SetPtEtaPhiM(photon_pt->at(jj),photon_eta->at(jj),photon_phi->at(jj),0.0); 
                               //Histogram filling
                               CMS_hgg_mass->Fill((photon1+photon2).M()); 
                               leadPt->Fill(photon_pt->at(ii)); subleadPt->Fill(photon_pt->at(jj));
                               R9_lead->Fill(photon_full5x5_r9->at(ii)); R9_sublead->Fill(photon_full5x5_r9->at(ii));
                               Eta_lead->Fill(fabs(photon_sc_eta->at(ii))); Eta_sublead->Fill(fabs(photon_sc_eta->at(jj)));
                               ptSubVsLead->Fill(photon_pt->at(ii),photon_pt->at(jj));
                               R9VsEtaLead->Fill(photon_full5x5_r9->at(ii),fabs(photon_sc_eta->at(ii)));
                               R9VsEtaSubLead->Fill(photon_full5x5_r9->at(jj),fabs(photon_sc_eta->at(jj)));
                               Float_t sf_lead    = cset_sf_lead->evaluate({"nominal",fabs(photon_sc_eta->at(ii)), photon_full5x5_r9->at(ii), photon_pt->at(ii)});
                               Float_t sf_lead_sublead = cset_sf_lead->evaluate({"nominal",fabs(photon_sc_eta->at(jj)), photon_full5x5_r9->at(jj), photon_pt->at(jj)});
                               Float_t sf_sublead = cset_sf_sublead->evaluate({"nominal",fabs(photon_sc_eta->at(jj)), photon_full5x5_r9->at(jj), photon_pt->at(jj)});
                               Float_t sf_sublead_lead = cset_sf_sublead->evaluate({"nominal",fabs(photon_sc_eta->at(ii)), photon_full5x5_r9->at(ii), photon_pt->at(ii)});
                               Float_t SF = sf_lead * sf_sublead + sf_lead_sublead * sf_sublead_lead - sf_lead * sf_lead_sublead;
                               //std::cout << sf_lead << "  - " << sf_sublead << " - " << sf_lead * sf_sublead << std::endl; 

                               h1->Fill(SF);
                               if(fabs(photon_sc_eta->at(ii)) > 1.5 && fabs(photon_sc_eta->at(jj)) > 1.5 ) h2->Fill(SF); 
                               if(photon_full5x5_r9->at(ii)   < 0.56 && photon_full5x5_r9->at(ii) < 0.85 ) h3->Fill(SF);
 			       if(photon_pt->at(ii) < 40 && photon_pt->at(jj) < 40 )                       h4->Fill(SF);//sf_lead * sf_sublead);
			       if(fabs(photon_sc_eta->at(ii)) < 1.5 && fabs(photon_sc_eta->at(jj)) < 1.5 ) h5->Fill(SF);//sf_lead * sf_sublead);
			       if(photon_full5x5_r9->at(ii)   > 0.85 && photon_full5x5_r9->at(ii) > 0.90 ) h6->Fill(SF);//sf_lead * sf_sublead);
                               if(SF > 1.0) std::cout << SF << std::endl;
                        }  // find second photon for higgs
                }
          }
        final_file->Write();
        final_file->cd();
	CMS_hgg_mass->Write();
	leadPt->Write();
	subleadPt->Write();
	R9_lead->Write();
	R9_sublead->Write();
	Eta_lead->Write();
	Eta_sublead->Write();
	ptSubVsLead->Write();
	R9VsEtaSubLead-> Write();
        h1->Write(); h2->Write(); h3->Write(); h4->Write(); h5->Write(); h6->Write(); 
  	final_file->Close();
  }
}

