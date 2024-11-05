#ifndef __ShowerShapeCorrector_h__
#define __ShowerShapeCorrector_h__
#include "TFile.h"
#include "TGraphErrors.h"

#include <map>
#include <string>

namespace ShowerShapeCorrector
{
  TGraphErrors* GetSSCorrGraph(TFile* fIN, const char* nIN);
  std::map<std::string,TGraphErrors*> loadTGraph_dataInv(const char* inFILE);
  std::map<std::string,TGraphErrors*> loadTGraph_mc     (const char* inFILE);
  ROOT::VecOps::RVec<float> apply_calibration(
    const TGraphErrors* gBARREL_dataINV, const TGraphErrors* gBARREL_MC,
    const TGraphErrors* gENDCAP_dataINV, const TGraphErrors* gENDCAP_MC,
    const ROOT::VecOps::RVec<float>& columnPHOeta,
    const ROOT::VecOps::RVec<float>& columnData);
  
  class ShowerShapeCalibGraphManager
  {
    public:
      ShowerShapeCalibGraphManager(const char* fBARREL, const char* fENDCAP) :
        barrel_dataInv( loadTGraph_dataInv(fBARREL) ), barrel_MC( loadTGraph_mc(fBARREL) ),
        endcap_dataInv( loadTGraph_dataInv(fENDCAP) ), endcap_MC( loadTGraph_mc(fENDCAP) ) {}
      ROOT::VecOps::RVec<float> ApplyCalibration( const std::string& varNAME,
          const ROOT::VecOps::RVec<float>& colPHOeta,
          const ROOT::VecOps::RVec<float>& colDATA ) const
      {
        const TGraphErrors* gBd = barrel_dataInv.at(varNAME);
        const TGraphErrors* gBm = barrel_MC     .at(varNAME);
        const TGraphErrors* gEd = endcap_dataInv.at(varNAME);
        const TGraphErrors* gEm = endcap_MC     .at(varNAME);
        return apply_calibration(gBd,gBm,gEd,gEm, colPHOeta, colDATA);
      }

    const std::map<std::string,TGraphErrors*> barrel_dataInv;
    const std::map<std::string,TGraphErrors*> barrel_MC;
    const std::map<std::string,TGraphErrors*> endcap_dataInv;
    const std::map<std::string,TGraphErrors*> endcap_MC;
  };
};

#define __ShowerShapeCorrector_C__
#ifdef  __ShowerShapeCorrector_C__
TGraphErrors* ShowerShapeCorrector::GetSSCorrGraph(TFile* fIN, const char* nIN)
{
  auto g = (TGraphErrors*) fIN->Get(nIN);
  //g->SetDirectory(0);
  return g;
}
std::map<std::string,TGraphErrors*> ShowerShapeCorrector::loadTGraph_dataInv(const char* inFILE)
{
  auto tFILE = TFile::Open(inFILE);
  std::map<std::string,TGraphErrors*> SSCorrGraph;
  SSCorrGraph["Photon_sieie"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_sieie");
  SSCorrGraph["Photon_esEffSigmaRR"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_esEffSigmaRR");
  SSCorrGraph["Photon_esEnergyOverRawE"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_esEnergyOverRawE");
  SSCorrGraph["Photon_energyRaw"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_energyRaw");
  SSCorrGraph["Photon_phiWidth"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_phiWidth");
  SSCorrGraph["Photon_etaWidth"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_etaWidth");
  SSCorrGraph["Photon_r9"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_r9");
  SSCorrGraph["Photon_s4"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_s4");
  SSCorrGraph["Photon_sieip"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_sieip");
  SSCorrGraph["Photon_hoe"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "dataInv_hoe");
  tFILE->Close();

  return SSCorrGraph;
}
std::map<std::string,TGraphErrors*> ShowerShapeCorrector::loadTGraph_mc(const char* inFILE)
{
  auto tFILE = TFile::Open(inFILE);
  std::map<std::string,TGraphErrors*> SSCorrGraph;
  SSCorrGraph["Photon_sieie"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_sieie");
  SSCorrGraph["Photon_esEffSigmaRR"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_esEffSigmaRR");
  SSCorrGraph["Photon_esEnergyOverRawE"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_esEnergyOverRawE");
  SSCorrGraph["Photon_energyRaw"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_energyRaw");
  SSCorrGraph["Photon_phiWidth"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_phiWidth");
  SSCorrGraph["Photon_etaWidth"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_etaWidth");
  SSCorrGraph["Photon_r9"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_r9");
  SSCorrGraph["Photon_s4"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_s4");
  SSCorrGraph["Photon_sieip"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_sieip");
  SSCorrGraph["Photon_hoe"] = ShowerShapeCorrector::GetSSCorrGraph(tFILE, "mc_hoe");
  tFILE->Close();

  return SSCorrGraph;
}
ROOT::VecOps::RVec<float> ShowerShapeCorrector::apply_calibration(
    const TGraphErrors* gBARREL_dataINV, const TGraphErrors* gBARREL_MC,
    const TGraphErrors* gENDCAP_dataINV, const TGraphErrors* gENDCAP_MC,
    const ROOT::VecOps::RVec<float>& columnPHOeta,
    const ROOT::VecOps::RVec<float>& columnData)
{

    std::vector<float> calibratedData(columnData.size());
    for ( std::size_t i = 0; i< columnPHOeta.size(); ++i )
    {
      float val = columnData.at(i);
      calibratedData[i] = fabs(columnPHOeta.at(i)) < 1.5 ?
        gBARREL_dataINV->Eval( gBARREL_MC->Eval(val) ) : gENDCAP_dataINV->Eval( gENDCAP_MC->Eval(val) );
    }
    return calibratedData;
}

#endif // __ShowerShapeCorrector_C__
#endif // __ShowerShapeCorrector_h__
