#ifndef __MyPhoSelections_h__
#define __MyPhoSelections_h__

namespace PhoSelections
{
  template<typename T>
  auto FindGoodPhotons(T& df);

  TString EventPassedPhoHLT();
  TString PhotonPreselection();
  TString PhotonSaikatSelection();
  TString LeadingPhotonSaikatSelection_Selection();
};



// detail inside the same file
#define __MyPhoSelections_C__
#ifdef __MyPhoSelections_C__
#include <numeric>

template <typename T>
auto PhoSelections::FindGoodPhotons(T &df)
{ return df.Define("goodPhoton","Photon_pt > 180 && Photon_pt<1700 && abs(Photon_eta) < 2.5").Filter("Sum(goodPhoton)>=1"); }

TString PhoSelections::EventPassedPhoHLT() // event based, not object based
{ return "HLT_Photon200==1"; }
TString PhoSelections::PhotonPreselection()
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
TString PhoSelections::PhotonSaikatSelection()
{ return "Photon_pt > 180 && Photon_pt<1700 && abs(Photon_eta) < 2.5"; }

TString PhoSelections::LeadingPhotonSaikatSelection_Selection()
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

#endif // __MyPhoSelections_C__
#endif // __MyPhoSelections_h__
  //ROOT::VecOps::RVec<float> EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA);
  //std::vector<float> EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA);
  //float* EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA);

//ROOT::VecOps::RVec<float> PhoSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
//std::vector<float> PhoSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
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


// //ROOT::VecOps::RVec<float> PhoSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
// //std::vector<float> PhoSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
// float* PhoSelections::EffectiveArea_ChIso(const ROOT::VecOps::RVec<float>& phoETA)
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
