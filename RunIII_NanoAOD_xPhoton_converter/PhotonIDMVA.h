#ifndef __PhotonIDMVA_h__
#define __PhotonIDMVA_h__
#include "TMVA/Reader.h"
#include "TMVA/RReader.hxx"
#include "TMVA/RInferenceUtils.hxx"

//  <Variables NVar="11">
//    <Variable VarIndex="0"  Expression="photon_esEffSigmaRR" Label="photon_esEffSigmaRR" Title="photon_esEffSigmaRR" Unit="F" Internal="photon_esEffSigmaRR" Type="F" Min="0.00000000e+00" Max="1.41421356e+01"/>
//    <Variable VarIndex="1"  Expression="photon_energyRaw" Label="photon_energyRaw" Title="photon_energyRaw" Unit="F" Internal="photon_energyRaw" Type="F" Min="7.53515625e+00" Max="5.23200000e+03"/>
//    <Variable VarIndex="2"  Expression="photon_esEnergyOverRawE" Label="photon_esEnergyOverRawE" Title="photon_esEnergyOverRawE" Unit="F" Internal="photon_esEnergyOverRawE" Type="F" Min="0.00000000e+00" Max="1.27978861e+00"/>
//    <Variable VarIndex="3"  Expression="photon_etaWidth" Label="photon_etaWidth" Title="photon_etaWidth" Unit="F" Internal="photon_etaWidth" Type="F" Min="1.34241418e-09" Max="8.51562500e-01"/>
//    <Variable VarIndex="4"  Expression="photon_hoe" Label="photon_hoe" Title="photon_hoe" Unit="F" Internal="photon_hoe" Type="F" Min="0.00000000e+00" Max="2.05625000e+01"/>
//    <Variable VarIndex="5"  Expression="photon_phiWidth" Label="photon_phiWidth" Title="photon_phiWidth" Unit="F" Internal="photon_phiWidth" Type="F" Min="3.20869731e-09" Max="1.77734375e+00"/>
//    <Variable VarIndex="6"  Expression="photon_r9" Label="photon_r9" Title="photon_r9" Unit="F" Internal="photon_r9" Type="F" Min="1.18652344e-01" Max="1.65000000e+02"/>
//    <Variable VarIndex="7"  Expression="photon_s4" Label="photon_s4" Title="photon_s4" Unit="F" Internal="photon_s4" Type="F" Min="6.16455078e-03" Max="1.00000000e+00"/>
//    <Variable VarIndex="8"  Expression="photon_sieie" Label="photon_sieie" Title="photon_sieie" Unit="F" Internal="photon_sieie" Type="F" Min="0.00000000e+00" Max="7.51953125e-02"/>
//    <Variable VarIndex="9"  Expression="photon_sieip" Label="photon_sieip" Title="photon_sieip" Unit="F" Internal="photon_sieip" Type="F" Min="-2.06756592e-03" Max="2.19726562e-03"/>
//    <Variable VarIndex="10" Expression="photon_rho" Label="photon_rho" Title="photon_rho" Unit="F" Internal="photon_rho" Type="F" Min="6.14492536e-01" Max="7.68899689e+01"/>
//  </Variables>
class PhotonMVACalculator
{
  public:
    PhotonMVACalculator(const char* xmlFILE_trainingRESULTbarrel,
                        const char* xmlFILE_trainingRESULTendcap );
    template<typename T>
    auto DefineMVAScore(
        T& df,
        const char* outVAR,
        const std::vector<const char*>& inputVARcolumns,
        const char* phoETAcolumn);
    
  TMVA::Experimental::RReader modelBarrel;
  TMVA::Experimental::RReader modelEndcap;
  float vars[12]; // 11 vars + 1 spectators
  bool columnDefined;
};
#define __PhotonIDMVA_C__
#ifdef  __PhotonIDMVA_C__
PhotonMVACalculator::PhotonMVACalculator(
    const char* xmlFILE_trainingRESULTbarrel,
    const char* xmlFILE_trainingRESULTendcap
    ) :
  modelBarrel(xmlFILE_trainingRESULTbarrel), modelEndcap(xmlFILE_trainingRESULTendcap),
  columnDefined(false) {}
template<typename T>
auto PhotonMVACalculator::DefineMVAScore(
    T& df,
    const char* outVAR,
    const std::vector<const char*>& inputVARcolumns,
    const char* phoETAcolumn)
{
  auto dataFRAME = df;
  if ( columnDefined )
    dataFRAME = dataFRAME.Redefine("photon_eta", phoETAcolumn);
  else
    dataFRAME = dataFRAME.Define("photon_eta", phoETAcolumn);
  // checker for inputVARcolumn and variables size.
  auto variables = modelBarrel.GetVariableNames();

  const int varSize = variables.size();
  for ( int idx=0 ; idx < varSize; ++idx )
    if (!columnDefined )
      dataFRAME = dataFRAME.Define( variables[idx], inputVARcolumns[idx] );
    else
      dataFRAME = dataFRAME.Redefine( variables[idx], inputVARcolumns[idx] );

  const char* nBarrel_tmp = Form("%s_barrel",outVAR);
  const char* nEndcap_tmp = Form("%s_endcap",outVAR);
  const char* nBarrel_tmp0= Form("%s_barrel[0]",outVAR);
  const char* nEndcap_tmp0= Form("%s_endcap[0]",outVAR);
  const char* nBarrel = Form("%s_Barrel",outVAR);
  const char* nEndcap = Form("%s_Endcap",outVAR);
  dataFRAME = dataFRAME
    .Define( nBarrel_tmp, TMVA::Experimental::Compute<11,float>(modelBarrel), variables ) // 11 == varSize
    .Define( nEndcap_tmp, TMVA::Experimental::Compute<11,float>(modelEndcap), variables ) // 11 == varSize
    .Define(nBarrel, nBarrel_tmp0)
    .Define(nEndcap, nEndcap_tmp0)
    .Define(outVAR,
            [](float eta, float mvaBARREL, float mvaENDCAP) { return fabs(eta)<1.5 ? mvaBARREL:mvaENDCAP; },
            {"photon_eta", nBarrel, nEndcap});

  columnDefined = true;
  return dataFRAME;

  // original code example...
  // auto newF = df__.Define("photon_esEffSigmaRR"    , "Photon_esEffSigmaRR[0]"    ) // declare variables inside xml file.
  //                 .Define("photon_energyRaw"       , "Photon_energyRaw[0]"       )
  //                 .Define("photon_esEnergyOverRawE", "Photon_esEnergyOverRawE[0]")
  //                 .Define("photon_etaWidth"        , "Photon_etaWidth[0]"        )
  //                 .Define("photon_hoe"             , "Photon_hoe[0]"             )
  //                 .Define("photon_phiWidth"        , "Photon_phiWidth[0]"        )
  //                 .Define("photon_r9"              , "Photon_r9[0]"              )
  //                 .Define("photon_s4"              , "Photon_s4[0]"              )
  //                 .Define("photon_sieie"           , "Photon_sieie[0]"           )
  //                 .Define("photon_sieip"           , "Photon_sieip[0]"           )
  //                 .Define("photon_rho"             , "Rho_fixedGridRhoFastjetAll")
  //                 .Define("photon_eta_"             , "Photon_eta[0]")
  //                 .Define("mvaoutputbarrel", TMVA::Experimental::Compute<11,float>(modelBarrel), variables)
  //                 .Define("mvaoutputendcap", TMVA::Experimental::Compute<11,float>(modelEndcap), variables)
  //                 .Define("mvaOutputBarrel", "mvaoutputbarrel[0]")
  //                 .Define("mvaOutputEndcap", "mvaoutputendcap[0]")
  //                 .Define("mvaOutput",
  //                     [](float eta, float mvaBARREL, float mvaENDCAP) { return fabs(eta)<1.5 ? mvaBARREL:mvaENDCAP; },
  //                     {"photon_eta", "mvaOutputBarrel", "mvaOutputEndcap"});
}
#endif // __PhotonIDMVA_C__
#endif // __PhotonIDMVA_h__
