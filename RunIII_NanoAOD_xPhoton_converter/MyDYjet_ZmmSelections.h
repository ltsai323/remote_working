#ifndef __MyDYjet_ZmmSelections_h__
#define __MyDYjet_ZmmSelections_h__
#include <utility>

typedef ROOT::VecOps::RVec<Float_t> RVecFloat;
typedef ROOT::VecOps::RVec<UChar_t> RVecUChar;
typedef ROOT::VecOps::RVec<Bool_t > RVecBool;


namespace DYjet_ZmmSelections
{
  template<typename T>
  auto FindGoodPhotons(T& df);

  TString EventPassedPhoHLT();
  TString PhotonPreselection();
  TString PhotonSaikatSelection();
  TString LeadingPhotonSaikatSelection_Selection();

  TString EventPassedHLT();
  TString IsolatedMuons();
  TString JetRequirement();
  std::pair<bool, std::pair<int, int>> selectMuonPair(const RVecFloat& muon_pt, const RVecUChar& muon_tkIsoId);
  std::pair<bool, std::pair<int, int>> selectMuonPair(const RVecFloat& muon_pt, const RVecBool& muonID);

};



// detail inside the same file
#define __MyDYjet_ZmmSelections_C__
#ifdef __MyDYjet_ZmmSelections_C__
#include <numeric>

TString DYjet_ZmmSelections::EventPassedHLT()
{ return "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==1"; }
TString DYjet_ZmmSelections::IsolatedMuons()
{ return "nMuon>1"; } // tight track ID
TString DYjet_ZmmSelections::JetRequirement()
{ return "nJet>0"; } // nJet >= 1
                     //
std::pair<bool, std::pair<int, int>> DYjet_ZmmSelections::selectMuonPair(const RVecFloat& muon_pt, const RVecUChar& muon_tkIsoId)
{
    // Iterate over pairs of muons
    for (size_t i = 0; i < muon_pt.size(); ++i) {
        for (size_t j = i + 1; j < muon_pt.size(); ++j) {
            // Check the selection criteria
            if (muon_pt[i] > 20 && int(muon_tkIsoId[i]) == 2 &&
                muon_pt[j] > 12 && int(muon_tkIsoId[j]) == 2) {
                // Return true with the indices of the selected pair
                return {true, {static_cast<int>(i), static_cast<int>(j)}};
            }
        }
    }
    // Return false if no valid pair is found
    return {false, {-1, -1}};
}
std::pair<bool, std::pair<int, int>> DYjet_ZmmSelections::selectMuonPair(const RVecFloat& muon_pt, const RVecBool& muonID)
{
    // Iterate over pairs of muons
    for (size_t i = 0; i < muon_pt.size(); ++i) {
        for (size_t j = i + 1; j < muon_pt.size(); ++j) {
            // Check the selection criteria
            if (muon_pt[i] > 20 && muonID[i] &&
                muon_pt[j] > 12 && muonID[j] ) {
                // Return true with the indices of the selected pair
                return {true, {static_cast<int>(i), static_cast<int>(j)}};
            }
        }
    }
    // Return false if no valid pair is found
    return {false, {-1, -1}};
}

template <typename T>
auto DYjet_ZmmSelections::FindGoodPhotons(T &df)
{ return df.Define("goodPhoton","Photon_pt > 180 && Photon_pt<1700 && abs(Photon_eta) < 2.5").Filter("Sum(goodPhoton)>=1"); }

TString DYjet_ZmmSelections::EventPassedPhoHLT() // event based, not object based
{ return "HLT_Photon200==1"; }
TString DYjet_ZmmSelections::PhotonPreselection()
{
  std::vector<const char*> usedCuts({
   "!(abs(Photon_eta)>1.4442 && abs(Photon_eta)<1.566)",
   "Photon_pfChargedIsoWorstVtx < 11",
   "Photon_pt>180 && Photon_pt<1700 && abs(Photon_eta)<2.5",
   "Photon_electronVeto == 1",
  });
    
  TString allCuts = std::accumulate(
    usedCuts.begin() + 1, usedCuts.end(), TString(usedCuts[0]),
    [](const TString& a, const char* b) { return a + " && " + b; }
  );
  
  return allCuts;
}
TString DYjet_ZmmSelections::PhotonSaikatSelection()
{ return "Photon_pt > 180 && Photon_pt<1700 && abs(Photon_eta) < 2.5"; }


TString DYjet_ZmmSelections::LeadingPhotonSaikatSelection_Selection()
{
  std::vector<const char*> usedCuts({
      "HLT_Photon200==1",
      "Photon_pixelSeed!=1", // asdf?
      "Abs(Photon_eta)>2.5",
      "!(Abs(Photon_eta)>1.4442&&Abs(Photon_eta)<1.566)",
      "!(Abs(Photon_eta)<1.4442&& (Photon_pfChargedIsoPFPV>1.7 || Photon_sieie>0.015 || Photon_hoe>0.05 || Photon_pfChargedIsoWorstVtx>10) )",
      "!(Abs(Photon_eta)>1.566 && (Photon_pfChargedIsoPFPV>1.5 || Photon_sieie>0.04  || Photon_hoe>0.05 || Photon_pfChargedIsoWorstVtx>10) )",
      "Photon_pt_calib > 210.", // put photon pt calibration


    
  });
  bool isSignalMC = false;
  std::vector<const char*> isSignalMCCut({
    "nGenIsolatedPhoton>0",
  });
  bool isDataEraG = false;
  std::vector<const char*> isDataEraGCut({
      "!(Photon_pt>700 && Photon_pt<900 && Photon_seediEtaOriX+0==-21 && Photon_seediPhiOriY==260)"
  });

  TString allCuts = std::accumulate(
    usedCuts.begin() + 1, usedCuts.end(), TString(usedCuts[0]),
    [](const TString& a, const char* b) { return a + " && " + b; }
  );
  
  return allCuts;
}

#endif // __MyDYjet_ZmmSelections_C__
#endif // __MyDYjet_ZmmSelections_h__
  //ROOT::VecOps::RVec<float> EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA);
  //std::vector<float> EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA);
  //float* EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA);

//ROOT::VecOps::RVec<float> DYjet_ZmmSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
//std::vector<float> DYjet_ZmmSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
//  float* EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
//{
//  //ROOT::VecOps::RVec<float> effAreas(phoETA.size());
//  //std::vector<float> effAreas(phoETA.size());
//  const short arrSize(phoETA.size());
//  float* effAreas = new float[arrSize];
//
//  for ( size_t iPho = 0; iPho < phoETA.size(); ++iPho )
//  {
//    float absEta = std::fabs(phoETA[iPho]);
//    float effArea = -1;
//    if      ( absEta < 1.0 ) effArea = 0.1;
//    else if ( absEta < 1.5 ) effArea = 0.15;
//    else if ( absEta < 2.0 ) effArea = 0.2;
//
//    effAreas[iPho] = effArea;
//  }
//  return effAreas;
//}


// //ROOT::VecOps::RVec<float> DYjet_ZmmSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
// //std::vector<float> DYjet_ZmmSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
// float* DYjet_ZmmSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
// {
//   //ROOT::VecOps::RVec<float> effAreas(phoETA.size());
//   //std::vector<float> effAreas(phoETA.size());
//   const short arrSize(phoETA.size());
//   float effAreas[arrSize];
// 
//   for ( size_t iPho = 0; iPho < phoETA.size(); ++iPho )
//   {
//     float absEta = std::fabs(phoETA[iPho]);
//     float effArea = -1;
//     if      ( absEta < 1.0 ) effArea = 0.1;
//     else if ( absEta < 1.5 ) effArea = 0.15;
//     else if ( absEta < 2.0 ) effArea = 0.2;
// 
//     effAreas[iPho] = effArea;
//   }
//   return effAreas;
// }
