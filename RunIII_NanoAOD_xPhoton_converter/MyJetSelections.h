#ifndef __MyJetSelections_h__
#define __MyJetSelections_h__
#include "TMath.h"

namespace JetSelections
{
  TString EventPassedAllJetHLT();
  // https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV
  // JetID = 2 : passed tight ID
  // JetID = 6 : Passed tight ID and lepton veto
  TString JetPreselection();

  //TString JetID();

  //ROOT::VecOps::RVec<int> SelectedJetExcludingPhoton (
  //  const ROOT::VecOps::RVec<int>& goodJET,
  //  const ROOT::VecOps::RVec<float>& jetETA,
  //  const ROOT::VecOps::RVec<float>& jetPHI,
  //  int phoIDX,
  //  const ROOT::VecOps::RVec<float>& phoETA,
  //  const ROOT::VecOps::RVec<float>& phoPHI
  //  );
  //TString SelectedJetExcludingPhoton2();

};


// add detail inside the same file
#define __MyJetSelections_C__

#ifdef __MyJetSelections_C__

TString JetSelections::EventPassedAllJetHLT() // event based, not object based
{ return "HLT_PFJet40==1 || HLT_PFJet60==1 || HLT_PFJet80==1 || HLT_PFJet110==1 || HLT_PFJet140==1 || HLT_PFJet200==1 || HLT_PFJet260==1 || HLT_PFJet320==1 || HLT_PFJet400==1 || HLT_PFJet450==1 || HLT_PFJet500==1 || HLT_PFJet550==1"; }

TString JetSelections::JetPreselection()
{ return "Jet_pt > 30. && abs(Jet_eta)<2.4 && Jet_jetId!=0"; }

//ROOT::VecOps::RVec<int> JetSelections::SelectedJetExcludingPhoton (
//    const ROOT::VecOps::RVec<int>& goodJET,
//    const ROOT::VecOps::RVec<float>& jetETA,
//    const ROOT::VecOps::RVec<float>& jetPHI,
//    int phoIDX,
//    const ROOT::VecOps::RVec<float>& phoETA,
//    const ROOT::VecOps::RVec<float>& phoPHI
//    )
//{
//  ROOT::VecOps::RVec<int> selectedJetExcludingPhoton(goodJET.size());
//
//  const float phoEta = phoETA[phoIDX];
//  const float phoPhi = phoPHI[phoIDX];
//
//  const float DELTAR_CUT = 0.4;
//  for ( size_t iCand = 0; iCand < goodJET.size(); ++iCand )
//  {
//    double deltaR = 999;
//    if ( goodJET[iCand] )
//    {
//      float deltaEta = phoEta - jetETA[iCand];
//      float deltaPhi = TMath::DeltaPhi(phoPhi - jetPHI[iCand]);
//      deltaR = TMath::Sqrt(deltaEta*deltaEta - deltaPhi*deltaPhi);
//    }
//    selectedJetExcludingPhoton[iCand] = deltaR < DELTAR_CUT ? 1 : 0;
//  }
//  return selectedJetExcludingPhoton;
//}
//TString JetSelections::SelectedJetExcludingPhoton2(const char* additionalCUT)
//{ return Form("%s && DeltaR(Jet<F8>
#endif // __MyJetSelections_C__
#endif // __MyJetSelections_h__
