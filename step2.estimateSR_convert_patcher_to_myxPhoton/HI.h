//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Dec 24 17:36:44 2024 by ROOT version 6.30/07
// from TTree Events/Events
// found on file: G4JetsMadgraph_100to200.root
//////////////////////////////////////////////////////////

#ifndef HI_h
#define HI_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "ROOT/RVec.hxx"

class HI {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   ULong_t         selectedPhoIdx;
   ULong_t         selectedGJetIdx;
   Bool_t          PassJetHLT;
   Bool_t          PassPhoHLT;
   UInt_t          run;
   UInt_t          luminosityBlock;
   ULong64_t       event;
   UInt_t          bunchCrossing;
   Int_t           nPhoton;
   Char_t          Photon_seediEtaOriX[6];   //[nPhoton]
   UChar_t         Photon_cutBased[6];   //[nPhoton]
   Bool_t          Photon_isScEtaEB[6];   //[nPhoton]
   Bool_t          Photon_isScEtaEE[6];   //[nPhoton]
   Bool_t          Photon_mvaID_WP80[6];   //[nPhoton]
   Bool_t          Photon_mvaID_WP90[6];   //[nPhoton]
   Bool_t          Photon_pixelSeed[6];   //[nPhoton]
   UChar_t         Photon_seedGain[6];   //[nPhoton]
   Short_t         Photon_electronIdx[6];   //[nPhoton]
   Int_t           Photon_seediPhiOriY[6];   //[nPhoton]
   Int_t           Photon_vidNestedWPBitmap[6];   //[nPhoton]
   Float_t         Photon_energyErr[6];   //[nPhoton]
   Float_t         Photon_energyRaw[6];   //[nPhoton]
   Float_t         Photon_esEffSigmaRR[6];   //[nPhoton]
   Float_t         Photon_esEnergyOverRawE[6];   //[nPhoton]
   Float_t         Photon_eta[6];   //[nPhoton]
   Float_t         Photon_etaWidth[6];   //[nPhoton]
   Float_t         Photon_haloTaggerMVAVal[6];   //[nPhoton]
   Float_t         Photon_hoe[6];   //[nPhoton]
   Float_t         Photon_hoe_PUcorr[6];   //[nPhoton]
   Float_t         Photon_mvaID[6];   //[nPhoton]
   Float_t         Photon_pfChargedIso[6];   //[nPhoton]
   Float_t         Photon_pfChargedIsoPFPV[6];   //[nPhoton]
   Float_t         Photon_pfChargedIsoWorstVtx[6];   //[nPhoton]
   Float_t         Photon_pfPhoIso03[6];   //[nPhoton]
   Float_t         Photon_pfRelIso03_all_quadratic[6];   //[nPhoton]
   Float_t         Photon_pfRelIso03_chg_quadratic[6];   //[nPhoton]
   Float_t         Photon_phi[6];   //[nPhoton]
   Float_t         Photon_phiWidth[6];   //[nPhoton]
   Float_t         Photon_pt[6];   //[nPhoton]
   Float_t         Photon_r9[6];   //[nPhoton]
   Float_t         Photon_s4[6];   //[nPhoton]
   Float_t         Photon_sieie[6];   //[nPhoton]
   Float_t         Photon_sieip[6];   //[nPhoton]
   Float_t         Photon_sipip[6];   //[nPhoton]
   Float_t         Photon_trkSumPtHollowConeDR03[6];   //[nPhoton]
   Float_t         Photon_trkSumPtSolidConeDR04[6];   //[nPhoton]
   Float_t         Photon_x_calo[6];   //[nPhoton]
   Float_t         Photon_y_calo[6];   //[nPhoton]
   Float_t         Photon_z_calo[6];   //[nPhoton]
   Float_t         mva;
   Float_t         Rho_fixedGridRhoFastjetAll;
   Int_t           nJet;
   UChar_t         Jet_jetId[14];   //[nJet]
   UChar_t         Jet_nConstituents[14];   //[nJet]
   UChar_t         Jet_nElectrons[14];   //[nJet]
   UChar_t         Jet_nMuons[14];   //[nJet]
   UChar_t         Jet_nSVs[14];   //[nJet]
   Int_t           Jet_hfadjacentEtaStripsSize[14];   //[nJet]
   Int_t           Jet_hfcentralEtaStripSize[14];   //[nJet]
   Float_t         Jet_PNetRegPtRawCorr[14];   //[nJet]
   Float_t         Jet_PNetRegPtRawCorrNeutrino[14];   //[nJet]
   Float_t         Jet_PNetRegPtRawRes[14];   //[nJet]
   Float_t         Jet_area[14];   //[nJet]
   Float_t         Jet_chEmEF[14];   //[nJet]
   Float_t         Jet_chHEF[14];   //[nJet]
   Float_t         Jet_eta[14];   //[nJet]
   Float_t         Jet_hfsigmaEtaEta[14];   //[nJet]
   Float_t         Jet_hfsigmaPhiPhi[14];   //[nJet]
   Float_t         Jet_mass[14];   //[nJet]
   Float_t         Jet_muEF[14];   //[nJet]
   Float_t         Jet_muonSubtrFactor[14];   //[nJet]
   Float_t         Jet_neEmEF[14];   //[nJet]
   Float_t         Jet_neHEF[14];   //[nJet]
   Float_t         Jet_phi[14];   //[nJet]
   Float_t         Jet_pt[14];   //[nJet]
   Float_t         Jet_rawFactor[14];   //[nJet]
   UChar_t         PV_npvs;
   UChar_t         PV_npvsGood;
   Float_t         PuppiMET_phi;
   Float_t         PuppiMET_pt;
   Bool_t          Flag_METFilters;
   Bool_t          HLT_Photon200;
   Bool_t          HLT_Photon175;
   Bool_t          HLT_Photon150;
   Int_t           nSV;
   Float_t         SV_dxySig[20];   //[nSV]
   Float_t         SV_dlenSig[20];   //[nSV]
   UChar_t         SV_ntracks[20];   //[nSV]
   Float_t         SV_chi2[20];   //[nSV]
   Float_t         SV_eta[20];   //[nSV]
   Float_t         SV_mass[20];   //[nSV]
   Float_t         SV_ndof[20];   //[nSV]
   Float_t         SV_phi[20];   //[nSV]
   Float_t         SV_pt[20];   //[nSV]
   Float_t         SV_x[20];   //[nSV]
   Float_t         SV_y[20];   //[nSV]
   Float_t         SV_z[20];   //[nSV]
   Float_t         Jet_btagPNetB[14];   //[nJet]
   Float_t         Jet_btagPNetCvB[14];   //[nJet]
   Float_t         Jet_btagPNetCvL[14];   //[nJet]
   Float_t         Jet_btagPNetQvG[14];   //[nJet]
   Float_t         Jet_btagRobustParTAK4B[14];   //[nJet]
   Float_t         Jet_btagRobustParTAK4CvB[14];   //[nJet]
   Float_t         Jet_btagRobustParTAK4CvL[14];   //[nJet]
   Float_t         Jet_btagRobustParTAK4QG[14];   //[nJet]
   Float_t         Jet_btagDeepFlavB[14];   //[nJet]
   Float_t         Jet_btagDeepFlavCvB[14];   //[nJet]
   Float_t         Jet_btagDeepFlavCvL[14];   //[nJet]
   Float_t         Jet_btagDeepFlavQG[14];   //[nJet]
   Short_t         Photon_genPartIdx[6];   //[nPhoton]
   Short_t         Jet_genJetIdx[14];   //[nJet]
   Int_t           nGenPart;
   Short_t         GenPart_genPartIdxMother[84];   //[nGenPart]
   UShort_t        GenPart_statusFlags[84];   //[nGenPart]
   Int_t           GenPart_pdgId[84];   //[nGenPart]
   Int_t           GenPart_status[84];   //[nGenPart]
   Float_t         GenPart_eta[84];   //[nGenPart]
   Float_t         GenPart_mass[84];   //[nGenPart]
   Float_t         GenPart_phi[84];   //[nGenPart]
   Float_t         GenPart_pt[84];   //[nGenPart]
   Int_t           nGenJet;
   Float_t         GenJet_eta[16];   //[nGenJet]
   Float_t         GenJet_pt[16];   //[nGenJet]
   Float_t         GenJet_phi[16];   //[nGenJet]
   Float_t         GenJet_mass[16];   //[nGenJet]
   Short_t         GenJet_partonFlavour[16];   //[nGenJet]
   UChar_t         GenJet_hadronFlavour[16];   //[nGenJet]
   Float_t         genWeight;
   Int_t           nGenIsolatedPhoton;
   Float_t         GenIsolatedPhoton_eta[3];   //[nGenIsolatedPhoton]
   Float_t         GenIsolatedPhoton_mass[3];   //[nGenIsolatedPhoton]
   Float_t         GenIsolatedPhoton_phi[3];   //[nGenIsolatedPhoton]
   Float_t         GenIsolatedPhoton_pt[3];   //[nGenIsolatedPhoton]
   Int_t           Generator_id1;
   Int_t           Generator_id2;
   Float_t         Generator_scalePDF;
   Float_t         Generator_weight;
   Float_t         Generator_x1;
   Float_t         Generator_x2;
   Int_t           Pileup_nPU;
   Short_t         Jet_partonFlavour[14];   //[nJet]
   UChar_t         Jet_hadronFlavour[14];   //[nJet]
   Int_t           nPSWeight;
   Float_t         PSWeight[4];   //[nPSWeight]
   ROOT::VecOps::RVec<float> *Photon_sieie_calib;
   ROOT::VecOps::RVec<float> *Photon_esEffSigmaRR_calib;
   ROOT::VecOps::RVec<float> *Photon_esEnergyOverRawE_calib;
   ROOT::VecOps::RVec<float> *Photon_energyRaw_calib;
   ROOT::VecOps::RVec<float> *Photon_phiWidth_calib;
   ROOT::VecOps::RVec<float> *Photon_etaWidth_calib;
   ROOT::VecOps::RVec<float> *Photon_r9_calib;
   ROOT::VecOps::RVec<float> *Photon_s4_calib;
   ROOT::VecOps::RVec<float> *Photon_sieip_calib;
   ROOT::VecOps::RVec<float> *Photon_hoe_calib;
   Float_t         mva_calib;

   // List of branches
   TBranch        *b_selectedPhoIdx;   //!
   TBranch        *b_selectedGJetIdx;   //!
   TBranch        *b_PassJetHLT;   //!
   TBranch        *b_PassPhoHLT;   //!
   TBranch        *b_run;   //!
   TBranch        *b_luminosityBlock;   //!
   TBranch        *b_event;   //!
   TBranch        *b_bunchCrossing;   //!
   TBranch        *b_nPhoton;   //!
   TBranch        *b_Photon_seediEtaOriX;   //!
   TBranch        *b_Photon_cutBased;   //!
   TBranch        *b_Photon_isScEtaEB;   //!
   TBranch        *b_Photon_isScEtaEE;   //!
   TBranch        *b_Photon_mvaID_WP80;   //!
   TBranch        *b_Photon_mvaID_WP90;   //!
   TBranch        *b_Photon_pixelSeed;   //!
   TBranch        *b_Photon_seedGain;   //!
   TBranch        *b_Photon_electronIdx;   //!
   TBranch        *b_Photon_seediPhiOriY;   //!
   TBranch        *b_Photon_vidNestedWPBitmap;   //!
   TBranch        *b_Photon_energyErr;   //!
   TBranch        *b_Photon_energyRaw;   //!
   TBranch        *b_Photon_esEffSigmaRR;   //!
   TBranch        *b_Photon_esEnergyOverRawE;   //!
   TBranch        *b_Photon_eta;   //!
   TBranch        *b_Photon_etaWidth;   //!
   TBranch        *b_Photon_haloTaggerMVAVal;   //!
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
   TBranch        *b_mva;   //!
   TBranch        *b_Rho_fixedGridRhoFastjetAll;   //!
   TBranch        *b_nJet;   //!
   TBranch        *b_Jet_jetId;   //!
   TBranch        *b_Jet_nConstituents;   //!
   TBranch        *b_Jet_nElectrons;   //!
   TBranch        *b_Jet_nMuons;   //!
   TBranch        *b_Jet_nSVs;   //!
   TBranch        *b_Jet_hfadjacentEtaStripsSize;   //!
   TBranch        *b_Jet_hfcentralEtaStripSize;   //!
   TBranch        *b_Jet_PNetRegPtRawCorr;   //!
   TBranch        *b_Jet_PNetRegPtRawCorrNeutrino;   //!
   TBranch        *b_Jet_PNetRegPtRawRes;   //!
   TBranch        *b_Jet_area;   //!
   TBranch        *b_Jet_chEmEF;   //!
   TBranch        *b_Jet_chHEF;   //!
   TBranch        *b_Jet_eta;   //!
   TBranch        *b_Jet_hfsigmaEtaEta;   //!
   TBranch        *b_Jet_hfsigmaPhiPhi;   //!
   TBranch        *b_Jet_mass;   //!
   TBranch        *b_Jet_muEF;   //!
   TBranch        *b_Jet_muonSubtrFactor;   //!
   TBranch        *b_Jet_neEmEF;   //!
   TBranch        *b_Jet_neHEF;   //!
   TBranch        *b_Jet_phi;   //!
   TBranch        *b_Jet_pt;   //!
   TBranch        *b_Jet_rawFactor;   //!
   TBranch        *b_PV_npvs;   //!
   TBranch        *b_PV_npvsGood;   //!
   TBranch        *b_PuppiMET_phi;   //!
   TBranch        *b_PuppiMET_pt;   //!
   TBranch        *b_Flag_METFilters;   //!
   TBranch        *b_HLT_Photon200;   //!
   TBranch        *b_HLT_Photon175;   //!
   TBranch        *b_HLT_Photon150;   //!
   TBranch        *b_nSV;   //!
   TBranch        *b_SV_dxySig;   //!
   TBranch        *b_SV_dlenSig;   //!
   TBranch        *b_SV_ntracks;   //!
   TBranch        *b_SV_chi2;   //!
   TBranch        *b_SV_eta;   //!
   TBranch        *b_SV_mass;   //!
   TBranch        *b_SV_ndof;   //!
   TBranch        *b_SV_phi;   //!
   TBranch        *b_SV_pt;   //!
   TBranch        *b_SV_x;   //!
   TBranch        *b_SV_y;   //!
   TBranch        *b_SV_z;   //!
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
   TBranch        *b_Photon_genPartIdx;   //!
   TBranch        *b_Jet_genJetIdx;   //!
   TBranch        *b_nGenPart;   //!
   TBranch        *b_GenPart_genPartIdxMother;   //!
   TBranch        *b_GenPart_statusFlags;   //!
   TBranch        *b_GenPart_pdgId;   //!
   TBranch        *b_GenPart_status;   //!
   TBranch        *b_GenPart_eta;   //!
   TBranch        *b_GenPart_mass;   //!
   TBranch        *b_GenPart_phi;   //!
   TBranch        *b_GenPart_pt;   //!
   TBranch        *b_nGenJet;   //!
   TBranch        *b_GenJet_eta;   //!
   TBranch        *b_GenJet_pt;   //!
   TBranch        *b_GenJet_phi;   //!
   TBranch        *b_GenJet_mass;   //!
   TBranch        *b_GenJet_partonFlavour;   //!
   TBranch        *b_GenJet_hadronFlavour;   //!
   TBranch        *b_genWeight;   //!
   TBranch        *b_nGenIsolatedPhoton;   //!
   TBranch        *b_GenIsolatedPhoton_eta;   //!
   TBranch        *b_GenIsolatedPhoton_mass;   //!
   TBranch        *b_GenIsolatedPhoton_phi;   //!
   TBranch        *b_GenIsolatedPhoton_pt;   //!
   TBranch        *b_Generator_id1;   //!
   TBranch        *b_Generator_id2;   //!
   TBranch        *b_Generator_scalePDF;   //!
   TBranch        *b_Generator_weight;   //!
   TBranch        *b_Generator_x1;   //!
   TBranch        *b_Generator_x2;   //!
   TBranch        *b_Pileup_nPU;   //!
   TBranch        *b_Jet_partonFlavour;   //!
   TBranch        *b_Jet_hadronFlavour;   //!
   TBranch        *b_nPSWeight;   //!
   TBranch        *b_PSWeight;   //!
   TBranch        *b_Photon_sieie_calib;   //!
   TBranch        *b_Photon_esEffSigmaRR_calib;   //!
   TBranch        *b_Photon_esEnergyOverRawE_calib;   //!
   TBranch        *b_Photon_energyRaw_calib;   //!
   TBranch        *b_Photon_phiWidth_calib;   //!
   TBranch        *b_Photon_etaWidth_calib;   //!
   TBranch        *b_Photon_r9_calib;   //!
   TBranch        *b_Photon_s4_calib;   //!
   TBranch        *b_Photon_sieip_calib;   //!
   TBranch        *b_Photon_hoe_calib;   //!
   TBranch        *b_mva_calib;   //!

   HI(TTree *tree=0);
   virtual ~HI();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef HI_cxx
HI::HI(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      //TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("G4JetsMadgraph_100to200.root");
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/QCD4JetsMadgraph_200to400.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/QCD4JetsMadgraph_200to400.root");
      }
      f->GetObject("Events",tree);

   }
   Init(tree);
}

HI::~HI()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t HI::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t HI::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void HI::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   Photon_sieie_calib = 0;
   Photon_esEffSigmaRR_calib = 0;
   Photon_esEnergyOverRawE_calib = 0;
   Photon_energyRaw_calib = 0;
   Photon_phiWidth_calib = 0;
   Photon_etaWidth_calib = 0;
   Photon_r9_calib = 0;
   Photon_s4_calib = 0;
   Photon_sieip_calib = 0;
   Photon_hoe_calib = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("selectedPhoIdx", &selectedPhoIdx, &b_selectedPhoIdx);
   fChain->SetBranchAddress("selectedGJetIdx", &selectedGJetIdx, &b_selectedGJetIdx);
   fChain->SetBranchAddress("PassJetHLT", &PassJetHLT, &b_PassJetHLT);
   fChain->SetBranchAddress("PassPhoHLT", &PassPhoHLT, &b_PassPhoHLT);
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("luminosityBlock", &luminosityBlock, &b_luminosityBlock);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("bunchCrossing", &bunchCrossing, &b_bunchCrossing);
   fChain->SetBranchAddress("nPhoton", &nPhoton, &b_nPhoton);
   fChain->SetBranchAddress("Photon_seediEtaOriX", Photon_seediEtaOriX, &b_Photon_seediEtaOriX);
   fChain->SetBranchAddress("Photon_cutBased", Photon_cutBased, &b_Photon_cutBased);
   fChain->SetBranchAddress("Photon_isScEtaEB", Photon_isScEtaEB, &b_Photon_isScEtaEB);
   fChain->SetBranchAddress("Photon_isScEtaEE", Photon_isScEtaEE, &b_Photon_isScEtaEE);
   fChain->SetBranchAddress("Photon_mvaID_WP80", Photon_mvaID_WP80, &b_Photon_mvaID_WP80);
   fChain->SetBranchAddress("Photon_mvaID_WP90", Photon_mvaID_WP90, &b_Photon_mvaID_WP90);
   fChain->SetBranchAddress("Photon_pixelSeed", Photon_pixelSeed, &b_Photon_pixelSeed);
   fChain->SetBranchAddress("Photon_seedGain", Photon_seedGain, &b_Photon_seedGain);
   fChain->SetBranchAddress("Photon_electronIdx", Photon_electronIdx, &b_Photon_electronIdx);
   fChain->SetBranchAddress("Photon_seediPhiOriY", Photon_seediPhiOriY, &b_Photon_seediPhiOriY);
   fChain->SetBranchAddress("Photon_vidNestedWPBitmap", Photon_vidNestedWPBitmap, &b_Photon_vidNestedWPBitmap);
   fChain->SetBranchAddress("Photon_energyErr", Photon_energyErr, &b_Photon_energyErr);
   fChain->SetBranchAddress("Photon_energyRaw", Photon_energyRaw, &b_Photon_energyRaw);
   fChain->SetBranchAddress("Photon_esEffSigmaRR", Photon_esEffSigmaRR, &b_Photon_esEffSigmaRR);
   fChain->SetBranchAddress("Photon_esEnergyOverRawE", Photon_esEnergyOverRawE, &b_Photon_esEnergyOverRawE);
   fChain->SetBranchAddress("Photon_eta", Photon_eta, &b_Photon_eta);
   fChain->SetBranchAddress("Photon_etaWidth", Photon_etaWidth, &b_Photon_etaWidth);
   fChain->SetBranchAddress("Photon_haloTaggerMVAVal", Photon_haloTaggerMVAVal, &b_Photon_haloTaggerMVAVal);
   fChain->SetBranchAddress("Photon_hoe", Photon_hoe, &b_Photon_hoe);
   fChain->SetBranchAddress("Photon_hoe_PUcorr", Photon_hoe_PUcorr, &b_Photon_hoe_PUcorr);
   fChain->SetBranchAddress("Photon_mvaID", Photon_mvaID, &b_Photon_mvaID);
   fChain->SetBranchAddress("Photon_pfChargedIso", Photon_pfChargedIso, &b_Photon_pfChargedIso);
   fChain->SetBranchAddress("Photon_pfChargedIsoPFPV", Photon_pfChargedIsoPFPV, &b_Photon_pfChargedIsoPFPV);
   fChain->SetBranchAddress("Photon_pfChargedIsoWorstVtx", Photon_pfChargedIsoWorstVtx, &b_Photon_pfChargedIsoWorstVtx);
   fChain->SetBranchAddress("Photon_pfPhoIso03", Photon_pfPhoIso03, &b_Photon_pfPhoIso03);
   fChain->SetBranchAddress("Photon_pfRelIso03_all_quadratic", Photon_pfRelIso03_all_quadratic, &b_Photon_pfRelIso03_all_quadratic);
   fChain->SetBranchAddress("Photon_pfRelIso03_chg_quadratic", Photon_pfRelIso03_chg_quadratic, &b_Photon_pfRelIso03_chg_quadratic);
   fChain->SetBranchAddress("Photon_phi", Photon_phi, &b_Photon_phi);
   fChain->SetBranchAddress("Photon_phiWidth", Photon_phiWidth, &b_Photon_phiWidth);
   fChain->SetBranchAddress("Photon_pt", Photon_pt, &b_Photon_pt);
   fChain->SetBranchAddress("Photon_r9", Photon_r9, &b_Photon_r9);
   fChain->SetBranchAddress("Photon_s4", Photon_s4, &b_Photon_s4);
   fChain->SetBranchAddress("Photon_sieie", Photon_sieie, &b_Photon_sieie);
   fChain->SetBranchAddress("Photon_sieip", Photon_sieip, &b_Photon_sieip);
   fChain->SetBranchAddress("Photon_sipip", Photon_sipip, &b_Photon_sipip);
   fChain->SetBranchAddress("Photon_trkSumPtHollowConeDR03", Photon_trkSumPtHollowConeDR03, &b_Photon_trkSumPtHollowConeDR03);
   fChain->SetBranchAddress("Photon_trkSumPtSolidConeDR04", Photon_trkSumPtSolidConeDR04, &b_Photon_trkSumPtSolidConeDR04);
   fChain->SetBranchAddress("Photon_x_calo", Photon_x_calo, &b_Photon_x_calo);
   fChain->SetBranchAddress("Photon_y_calo", Photon_y_calo, &b_Photon_y_calo);
   fChain->SetBranchAddress("Photon_z_calo", Photon_z_calo, &b_Photon_z_calo);
   fChain->SetBranchAddress("mva", &mva, &b_mva);
   fChain->SetBranchAddress("Rho_fixedGridRhoFastjetAll", &Rho_fixedGridRhoFastjetAll, &b_Rho_fixedGridRhoFastjetAll);
   fChain->SetBranchAddress("nJet", &nJet, &b_nJet);
   fChain->SetBranchAddress("Jet_jetId", Jet_jetId, &b_Jet_jetId);
   fChain->SetBranchAddress("Jet_nConstituents", Jet_nConstituents, &b_Jet_nConstituents);
   fChain->SetBranchAddress("Jet_nElectrons", Jet_nElectrons, &b_Jet_nElectrons);
   fChain->SetBranchAddress("Jet_nMuons", Jet_nMuons, &b_Jet_nMuons);
   fChain->SetBranchAddress("Jet_nSVs", Jet_nSVs, &b_Jet_nSVs);
   fChain->SetBranchAddress("Jet_hfadjacentEtaStripsSize", Jet_hfadjacentEtaStripsSize, &b_Jet_hfadjacentEtaStripsSize);
   fChain->SetBranchAddress("Jet_hfcentralEtaStripSize", Jet_hfcentralEtaStripSize, &b_Jet_hfcentralEtaStripSize);
   fChain->SetBranchAddress("Jet_PNetRegPtRawCorr", Jet_PNetRegPtRawCorr, &b_Jet_PNetRegPtRawCorr);
   fChain->SetBranchAddress("Jet_PNetRegPtRawCorrNeutrino", Jet_PNetRegPtRawCorrNeutrino, &b_Jet_PNetRegPtRawCorrNeutrino);
   fChain->SetBranchAddress("Jet_PNetRegPtRawRes", Jet_PNetRegPtRawRes, &b_Jet_PNetRegPtRawRes);
   fChain->SetBranchAddress("Jet_area", Jet_area, &b_Jet_area);
   fChain->SetBranchAddress("Jet_chEmEF", Jet_chEmEF, &b_Jet_chEmEF);
   fChain->SetBranchAddress("Jet_chHEF", Jet_chHEF, &b_Jet_chHEF);
   fChain->SetBranchAddress("Jet_eta", Jet_eta, &b_Jet_eta);
   fChain->SetBranchAddress("Jet_hfsigmaEtaEta", Jet_hfsigmaEtaEta, &b_Jet_hfsigmaEtaEta);
   fChain->SetBranchAddress("Jet_hfsigmaPhiPhi", Jet_hfsigmaPhiPhi, &b_Jet_hfsigmaPhiPhi);
   fChain->SetBranchAddress("Jet_mass", Jet_mass, &b_Jet_mass);
   fChain->SetBranchAddress("Jet_muEF", Jet_muEF, &b_Jet_muEF);
   fChain->SetBranchAddress("Jet_muonSubtrFactor", Jet_muonSubtrFactor, &b_Jet_muonSubtrFactor);
   fChain->SetBranchAddress("Jet_neEmEF", Jet_neEmEF, &b_Jet_neEmEF);
   fChain->SetBranchAddress("Jet_neHEF", Jet_neHEF, &b_Jet_neHEF);
   fChain->SetBranchAddress("Jet_phi", Jet_phi, &b_Jet_phi);
   fChain->SetBranchAddress("Jet_pt", Jet_pt, &b_Jet_pt);
   fChain->SetBranchAddress("Jet_rawFactor", Jet_rawFactor, &b_Jet_rawFactor);
   fChain->SetBranchAddress("PV_npvs", &PV_npvs, &b_PV_npvs);
   fChain->SetBranchAddress("PV_npvsGood", &PV_npvsGood, &b_PV_npvsGood);
   fChain->SetBranchAddress("PuppiMET_phi", &PuppiMET_phi, &b_PuppiMET_phi);
   fChain->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt, &b_PuppiMET_pt);
   fChain->SetBranchAddress("Flag_METFilters", &Flag_METFilters, &b_Flag_METFilters);
   fChain->SetBranchAddress("HLT_Photon200", &HLT_Photon200, &b_HLT_Photon200);
   fChain->SetBranchAddress("HLT_Photon175", &HLT_Photon175, &b_HLT_Photon175);
   fChain->SetBranchAddress("HLT_Photon150", &HLT_Photon150, &b_HLT_Photon150);
   fChain->SetBranchAddress("nSV", &nSV, &b_nSV);
   fChain->SetBranchAddress("SV_dxySig", SV_dxySig, &b_SV_dxySig);
   fChain->SetBranchAddress("SV_dlenSig", SV_dlenSig, &b_SV_dlenSig);
   fChain->SetBranchAddress("SV_ntracks", SV_ntracks, &b_SV_ntracks);
   fChain->SetBranchAddress("SV_chi2", SV_chi2, &b_SV_chi2);
   fChain->SetBranchAddress("SV_eta", SV_eta, &b_SV_eta);
   fChain->SetBranchAddress("SV_mass", SV_mass, &b_SV_mass);
   fChain->SetBranchAddress("SV_ndof", SV_ndof, &b_SV_ndof);
   fChain->SetBranchAddress("SV_phi", SV_phi, &b_SV_phi);
   fChain->SetBranchAddress("SV_pt", SV_pt, &b_SV_pt);
   fChain->SetBranchAddress("SV_x", SV_x, &b_SV_x);
   fChain->SetBranchAddress("SV_y", SV_y, &b_SV_y);
   fChain->SetBranchAddress("SV_z", SV_z, &b_SV_z);
   fChain->SetBranchAddress("Jet_btagPNetB", Jet_btagPNetB, &b_Jet_btagPNetB);
   fChain->SetBranchAddress("Jet_btagPNetCvB", Jet_btagPNetCvB, &b_Jet_btagPNetCvB);
   fChain->SetBranchAddress("Jet_btagPNetCvL", Jet_btagPNetCvL, &b_Jet_btagPNetCvL);
   fChain->SetBranchAddress("Jet_btagPNetQvG", Jet_btagPNetQvG, &b_Jet_btagPNetQvG);
   fChain->SetBranchAddress("Jet_btagRobustParTAK4B", Jet_btagRobustParTAK4B, &b_Jet_btagRobustParTAK4B);
   fChain->SetBranchAddress("Jet_btagRobustParTAK4CvB", Jet_btagRobustParTAK4CvB, &b_Jet_btagRobustParTAK4CvB);
   fChain->SetBranchAddress("Jet_btagRobustParTAK4CvL", Jet_btagRobustParTAK4CvL, &b_Jet_btagRobustParTAK4CvL);
   fChain->SetBranchAddress("Jet_btagRobustParTAK4QG", Jet_btagRobustParTAK4QG, &b_Jet_btagRobustParTAK4QG);
   fChain->SetBranchAddress("Jet_btagDeepFlavB", Jet_btagDeepFlavB, &b_Jet_btagDeepFlavB);
   fChain->SetBranchAddress("Jet_btagDeepFlavCvB", Jet_btagDeepFlavCvB, &b_Jet_btagDeepFlavCvB);
   fChain->SetBranchAddress("Jet_btagDeepFlavCvL", Jet_btagDeepFlavCvL, &b_Jet_btagDeepFlavCvL);
   fChain->SetBranchAddress("Jet_btagDeepFlavQG", Jet_btagDeepFlavQG, &b_Jet_btagDeepFlavQG);
   fChain->SetBranchAddress("Photon_genPartIdx", Photon_genPartIdx, &b_Photon_genPartIdx);
   fChain->SetBranchAddress("Jet_genJetIdx", Jet_genJetIdx, &b_Jet_genJetIdx);
   fChain->SetBranchAddress("nGenPart", &nGenPart, &b_nGenPart);
   fChain->SetBranchAddress("GenPart_genPartIdxMother", GenPart_genPartIdxMother, &b_GenPart_genPartIdxMother);
   fChain->SetBranchAddress("GenPart_statusFlags", GenPart_statusFlags, &b_GenPart_statusFlags);
   fChain->SetBranchAddress("GenPart_pdgId", GenPart_pdgId, &b_GenPart_pdgId);
   fChain->SetBranchAddress("GenPart_status", GenPart_status, &b_GenPart_status);
   fChain->SetBranchAddress("GenPart_eta", GenPart_eta, &b_GenPart_eta);
   fChain->SetBranchAddress("GenPart_mass", GenPart_mass, &b_GenPart_mass);
   fChain->SetBranchAddress("GenPart_phi", GenPart_phi, &b_GenPart_phi);
   fChain->SetBranchAddress("GenPart_pt", GenPart_pt, &b_GenPart_pt);
   fChain->SetBranchAddress("nGenJet", &nGenJet, &b_nGenJet);
   fChain->SetBranchAddress("GenJet_eta", GenJet_eta, &b_GenJet_eta);
   fChain->SetBranchAddress("GenJet_pt", GenJet_pt, &b_GenJet_pt);
   fChain->SetBranchAddress("GenJet_phi", GenJet_phi, &b_GenJet_phi);
   fChain->SetBranchAddress("GenJet_mass", GenJet_mass, &b_GenJet_mass);
   fChain->SetBranchAddress("GenJet_partonFlavour", GenJet_partonFlavour, &b_GenJet_partonFlavour);
   fChain->SetBranchAddress("GenJet_hadronFlavour", GenJet_hadronFlavour, &b_GenJet_hadronFlavour);
   fChain->SetBranchAddress("genWeight", &genWeight, &b_genWeight);
   fChain->SetBranchAddress("nGenIsolatedPhoton", &nGenIsolatedPhoton, &b_nGenIsolatedPhoton);
   fChain->SetBranchAddress("GenIsolatedPhoton_eta", GenIsolatedPhoton_eta, &b_GenIsolatedPhoton_eta);
   fChain->SetBranchAddress("GenIsolatedPhoton_mass", GenIsolatedPhoton_mass, &b_GenIsolatedPhoton_mass);
   fChain->SetBranchAddress("GenIsolatedPhoton_phi", GenIsolatedPhoton_phi, &b_GenIsolatedPhoton_phi);
   fChain->SetBranchAddress("GenIsolatedPhoton_pt", GenIsolatedPhoton_pt, &b_GenIsolatedPhoton_pt);
   fChain->SetBranchAddress("Generator_id1", &Generator_id1, &b_Generator_id1);
   fChain->SetBranchAddress("Generator_id2", &Generator_id2, &b_Generator_id2);
   fChain->SetBranchAddress("Generator_scalePDF", &Generator_scalePDF, &b_Generator_scalePDF);
   fChain->SetBranchAddress("Generator_weight", &Generator_weight, &b_Generator_weight);
   fChain->SetBranchAddress("Generator_x1", &Generator_x1, &b_Generator_x1);
   fChain->SetBranchAddress("Generator_x2", &Generator_x2, &b_Generator_x2);
   fChain->SetBranchAddress("Pileup_nPU", &Pileup_nPU, &b_Pileup_nPU);
   fChain->SetBranchAddress("Jet_partonFlavour", Jet_partonFlavour, &b_Jet_partonFlavour);
   fChain->SetBranchAddress("Jet_hadronFlavour", Jet_hadronFlavour, &b_Jet_hadronFlavour);
   fChain->SetBranchAddress("nPSWeight", &nPSWeight, &b_nPSWeight);
   fChain->SetBranchAddress("PSWeight", PSWeight, &b_PSWeight);
   fChain->SetBranchAddress("Photon_sieie_calib", &Photon_sieie_calib, &b_Photon_sieie_calib);
   fChain->SetBranchAddress("Photon_esEffSigmaRR_calib", &Photon_esEffSigmaRR_calib, &b_Photon_esEffSigmaRR_calib);
   fChain->SetBranchAddress("Photon_esEnergyOverRawE_calib", &Photon_esEnergyOverRawE_calib, &b_Photon_esEnergyOverRawE_calib);
   fChain->SetBranchAddress("Photon_energyRaw_calib", &Photon_energyRaw_calib, &b_Photon_energyRaw_calib);
   fChain->SetBranchAddress("Photon_phiWidth_calib", &Photon_phiWidth_calib, &b_Photon_phiWidth_calib);
   fChain->SetBranchAddress("Photon_etaWidth_calib", &Photon_etaWidth_calib, &b_Photon_etaWidth_calib);
   fChain->SetBranchAddress("Photon_r9_calib", &Photon_r9_calib, &b_Photon_r9_calib);
   fChain->SetBranchAddress("Photon_s4_calib", &Photon_s4_calib, &b_Photon_s4_calib);
   fChain->SetBranchAddress("Photon_sieip_calib", &Photon_sieip_calib, &b_Photon_sieip_calib);
   fChain->SetBranchAddress("Photon_hoe_calib", &Photon_hoe_calib, &b_Photon_hoe_calib);
   fChain->SetBranchAddress("mva_calib", &mva_calib, &b_mva_calib);
   Notify();
}

Bool_t HI::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void HI::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t HI::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef HI_cxx
