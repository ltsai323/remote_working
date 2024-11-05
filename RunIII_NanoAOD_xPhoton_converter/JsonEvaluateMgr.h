#ifndef __JsonEvaluateMgr_h__
#define __JsonEvaluateMgr_h__
#include <map>
#include <string>
#include "extlib/correction.h"
#include "TRandom3.h"

/*
auto cset_photon_scale_smearing_file = CorrectionSet::from_file("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/EGmSFs/SS.json");
auto cset_scale = cset_photon_scale_smearing_file->at("Prompt2022FG_ScaleJSON");
auto cset_smearing = cset_photon_scale_smearing_file->at("Prompt2022FG_SmearingJSON");
Float_t rho    = cset_smearing->evaluate({"rho",Photon_eta[ij], Photon_r9[ij]});
*/
typedef ROOT::VecOps::RVec<float> RVecFloat;
typedef ROOT::VecOps::RVec<UChar_t> RVecUChar;
namespace JsonEvaluateMgr
{
  class JsonEvaluateMgr
  {
    public:
      JsonEvaluateMgr(const char* jsonFILEname, const char* entryKEY) :
        jsonContent( correction::CorrectionSet::from_file(jsonFILEname) ),
        entry( jsonContent->at(entryKEY) ) { }
      std::unique_ptr<correction::CorrectionSet> jsonContent;
      correction::Correction::Ref entry;
  };
  RVecFloat PhotonPtSmearing_RandomRho_forMC(
    const correction::Correction::Ref& jsonENTRY, TRandom3* rnd,
    const RVecFloat& phoPT, const RVecFloat& phoETA, const RVecFloat& phoR9);
RVecFloat PhotonPtScaling_forData(
    const correction::Correction::Ref& jsonENTRY,
    const RVecFloat& phoPT, const RVecUChar& phoSEEDgain, UInt_t evtRUN, const RVecFloat& phoETA, const RVecFloat& phoR9);
};

#define __JsonEvaluateMgr_C__
#ifdef  __JsonEvaluateMgr_C__

RVecFloat JsonEvaluateMgr::PhotonPtSmearing_RandomRho_forMC(
    const correction::Correction::Ref& jsonENTRY, TRandom3* rnd,
    const RVecFloat& phoPT, const RVecFloat& phoETA, const RVecFloat& phoR9)
{
// photon pt smearing for MC from gaussian of rho
//auto cset_photon_scale_smearing_file = CorrectionSet::from_file("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/EGmSFs/SS.json");
//auto cset_smearing = cset_photon_scale_smearing_file->at("Prompt2022FG_SmearingJSON");
//Float_t rho    = cset_smearing->evaluate({"rho",Photon_eta[ij], Photon_r9[ij]});
//Float_t smearing = gRandom->Gaus(1,rho);
//Photon_pt_nom = Photon_pt[ij]*smearing;
  
    RVecFloat calibratedPhotonPt(phoPT.size());
    for ( std::size_t i = 0; i< phoPT.size(); ++i )
    {
      float new_rho = jsonENTRY->evaluate({"rho", phoETA.at(i), phoR9.at(i)});
      float smearing = rnd->Gaus(1,new_rho);
      calibratedPhotonPt[i] = phoPT.at(i) * smearing;
    }
    return calibratedPhotonPt;
}
RVecFloat JsonEvaluateMgr::PhotonPtScaling_forData(
    const correction::Correction::Ref& jsonENTRY,
    const RVecFloat& phoPT, const RVecUChar& phoSEEDgain, UInt_t evtRUN, const RVecFloat& phoETA, const RVecFloat& phoR9)
{
// photon pt scaling for data
//auto cset_scale = cset_photon_scale_smearing_file->at("Prompt2022FG_ScaleJSON");
//Float_t scale = 1.0*cset_scale->evaluate({"total_correction",Photon_seedGain[ij],Run,Photon_eta[ij],Photon_r9[ij],Photon_pt[ij]});
//Photon_pt_nom = Photon_pt[ij]*scale;
  
    float run = evtRUN;
    RVecFloat calibratedPhotonPt(phoPT.size());
    for ( std::size_t i = 0; i< phoPT.size(); ++i )
    {
      float scale = jsonENTRY->evaluate({"total_correction", phoSEEDgain.at(i), run, phoETA.at(i), phoR9.at(i), phoPT.at(i)});
      calibratedPhotonPt[i] = phoPT.at(i) * scale;
    }
    return calibratedPhotonPt;
}
#endif // __JsonEvaluateMgr_C__
#endif // __JsonEvaluateMgr_h__
