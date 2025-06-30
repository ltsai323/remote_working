#ifndef __GeneralFuncs_h__
#define __GeneralFuncs_h__
#include <ROOT/RDataFrame.hxx>
#include <TLorentzVector.h>
#include <ROOT/RVec.hxx>
#include <TFile.h>
#include <TTree.h>
#include <iostream>

using namespace ROOT;
using namespace ROOT::VecOps;
// Function to construct jetP4 vector
#define NO_MATCHING -1
namespace GeneralFuncs {
  RVec<TLorentzVector> ConstructJetP4(const RVec<float> &Jet_pt, 
                                      const RVec<float> &Jet_eta, 
                                      const RVec<float> &Jet_phi, 
                                      const RVec<float> &Jet_mass,
                                      const Int_t nJet);
  // -1 means no any matching
  Int_t GetIndex_firstPassing(const RVec<Int_t>& selectionCRITERIA);
  Short_t GetLeadingJetIdx_ignore2indices(const RVec<Float_t>& selectionCRITERIA, Short_t idx1, Short_t idx2); // ignore 2 idx from mu+ and mu- of Muon_jetIdx
 
  class PileupWgtMgr {
    public:
      PileupWgtMgr(const char* pileupROOTfile);
      Double_t GetWeight(Int_t pileup_NPU);


    private:
      TFile* fpu;
      TH1D* h_pu_nom;
  };
template <typename T>
  RVec<T> access_array_by_idxarray(const RVec<T>& theARRAY, RVec<Short_t> idxARRAY);
};



// detail inside the same file
#define __GeneralFuncs_C__
#ifdef  __GeneralFuncs_C__
RVec<TLorentzVector> GeneralFuncs::ConstructJetP4(const RVec<float> &Jet_pt, 
                                    const RVec<float> &Jet_eta, 
                                    const RVec<float> &Jet_phi, 
                                    const RVec<float> &Jet_mass,
                                    const Int_t nJet) {
    RVec<TLorentzVector> jetP4;
    for (size_t i = 0; i < nJet; ++i) {
        TLorentzVector jet;
        jet.SetPtEtaPhiM(Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
        jetP4.push_back(jet);
    }
    return jetP4;
}

Int_t GeneralFuncs::GetIndex_firstPassing(const RVec<Int_t>& selectionCRITERIA) {
  for ( size_t idx = 0; idx < selectionCRITERIA.size(); ++idx ) {
    if ( selectionCRITERIA[idx] == 0 ) continue;
    return idx;
  }
  return NO_MATCHING;
}
Short_t GeneralFuncs::GetLeadingJetIdx_ignore2indices(const RVec<Float_t>& jetPT, Short_t idx1, Short_t idx2) {
  Float_t jet_pt = 0;
  size_t selected_jet_index = NO_MATCHING;

  for ( size_t idx = 0; idx < jetPT.size(); ++idx ) {
    if ( idx == idx1 ) continue;
    if ( idx == idx2 ) continue;
    if ( jetPT[idx] == 0 ) continue;
    if ( jetPT[idx] > jet_pt )
    { jet_pt = jetPT[idx]; selected_jet_index = idx; }
  }
  return selected_jet_index;
}


GeneralFuncs::PileupWgtMgr::PileupWgtMgr(const char* pileupROOTfile) : fpu( TFile::Open(pileupROOTfile) )
{ this->h_pu_nom = (TH1D*) this->fpu->Get("pileupSF_nom"); }
Double_t GeneralFuncs::PileupWgtMgr::GetWeight(Int_t pileup_NPU) { return this->h_pu_nom->GetBinContent(this->h_pu_nom->FindBin(pileup_NPU)); }

template <typename T>
RVec<T> GeneralFuncs::access_array_by_idxarray(const RVec<T>& theARRAY, RVec<Short_t> idxARRAY)
{
  RVec<T> out;
  for ( Short_t idx : idxARRAY ) {
    try {
      // not to raise error if -1 put. (means nothing)
      if ( idx<0 ) { out.push_back(-1); continue; }
      if (idx >= theARRAY.size()) {
        throw std::out_of_range(
            Form("[OutOfRange] Accessing array(size %zu) with index(%d) is out of bounds!", theARRAY.size(), idx)
            );
      }
      out.push_back(theARRAY[idx]);  // Safe access
    }
    catch (const std::out_of_range &e) {
      std::cerr << "Error: " << e.what() << std::endl;
      exit(EXIT_FAILURE);
    }
  }
  return out;
}
#endif // __GeneralFuncs_C__
#endif // __GeneralFuncs_h__
