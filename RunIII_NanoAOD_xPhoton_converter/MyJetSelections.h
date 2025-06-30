#ifndef __MyJetSelections_h__
#define __MyJetSelections_h__
#include "TMath.h"

typedef ROOT::VecOps::RVec<Float_t> RVecFloat;
typedef ROOT::VecOps::RVec<Bool_t> RVecBool;
typedef ROOT::VecOps::RVec<Short_t> RVecShort;

namespace JetSelections
{
  TString EventPassedAllJetHLT();
  // https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV
  // JetID = 2 : passed tight ID
  // JetID = 6 : Passed tight ID and lepton veto
  TString JetPreselection();
  template <typename T>
  auto Define_LooseVetoMap(T &df);


};


// add detail inside the same file
#define __MyJetSelections_C__

#ifdef __MyJetSelections_C__

//TString JetSelections::EventPassedAllJetHLT() // event based, not object based
//{ return "HLT_PFJet40==1 || HLT_PFJet60==1 || HLT_PFJet80==1 || HLT_PFJet110==1 || HLT_PFJet140==1 || HLT_PFJet200==1 || HLT_PFJet260==1 || HLT_PFJet320==1 || HLT_PFJet400==1 || HLT_PFJet450==1 || HLT_PFJet500==1 || HLT_PFJet550==1"; }

TString JetSelections::JetPreselection()
{ return "Jet_pt > 15. && abs(Jet_eta)<2.4 && Jet_jetId==6"; } // leave some jets for JEC JER pt > 25GeV

// see Run3 VetoMap section in https://cms-jerc.web.cern.ch/Recommendations/
template <typename T>
auto JetSelections::Define_LooseVetoMap(T &df)
{
  return df
    .Define("Jet_reject_pf_muon",
      [](const RVecShort& jetMUidx, const RVecBool& muISpf)
      {
        RVecBool jet_has_pf_muon;
        for ( auto&& muidx : jetMUidx ) { bool reject_pf_muon = true; if ( muidx != -1 && muidx < muISpf.size() ) reject_pf_muon = muISpf[muidx] == 1 ? false : true; jet_has_pf_muon.push_back(reject_pf_muon); }
        return jet_has_pf_muon;
      }, {"Jet_muonIdx1", "Muon_isPFcand"}
      )
    .Define("LooseVetoMap", "Jet_pt > 15. && Jet_jetId == 6 && (Jet_neEmEF+Jet_neEmEF) < 0.9 && Jet_reject_pf_muon");
}

#endif // __MyJetSelections_C__
#endif // __MyJetSelections_h__
