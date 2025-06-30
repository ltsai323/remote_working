#include "correction.h"
#include "TLorentzVector.h"
#include "TRandom3.h"

#ifndef __JEC_JER_Corrector_h__
#define __JEC_JER_Corrector_h__

class JsonMgr
{
  public:
    //JsonMgr(const char* jsonFILE) : json_instance(correction::CorrectionSet::from_file(jsonFILE)) {}
    JsonMgr(const char* jsonFILE);
    correction::Correction::Ref GetKey(const char* key) { return this->json_instance->at(key); }
    
  private:
    std::unique_ptr<correction::CorrectionSet> json_instance;

};

struct JEC_JER_Corrector
{
  public:
    JEC_JER_Corrector(const char* jsonFILE,
        const char* jecSF_L2,
        const char* jecSF_L3,
        const char* jecSF_L23 );
    TLorentzVector JEC_Corrected(const TLorentzVector& origP4);

  
  private:
    JsonMgr json_ins;
    correction::Correction::Ref jec_sf_L2;
    correction::Correction::Ref jec_sf_L3;
    correction::Correction::Ref jec_sf_L23;
};

// MC requires energy smearing
struct Photon_EnergySmear
{
  public:
    Photon_EnergySmear(const char* jsonFILE,
      const char* phoSMEAR
    );
    Float_t EvaluatePt(float phoPT, float phoETA, float phoR9);


  private:
    JsonMgr json_ins;
    TRandom3 rnd;
    correction::Correction::Ref cset_smear;
  public:
    Float_t tmp_rho;
};

// data requires energy scaling
struct Photon_EnergyScale
{
  public:
    Photon_EnergyScale(const char* jsonFILE,
      const char* phoSCALE
    );
    Float_t EvaluatePt(float phoPT, float phoETA, float phoR9, UChar_t phoSEEDgain, UInt_t runNUMBER);

  private:
    JsonMgr json_ins;
    correction::Correction::Ref cset_scale;
};



#ifndef __JEC_JER_Corrector_CC__
JsonMgr::JsonMgr(const char* jsonFILE) {
    try { this->json_instance = correction::CorrectionSet::from_file(jsonFILE); }
    catch (const std::runtime_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        std::cerr << "\n\n" << Form("[UsedJsonFile] '%s'", jsonFILE) << std::endl;
        exit(EXIT_FAILURE);
    }
}
JEC_JER_Corrector::JEC_JER_Corrector(const char* jsonFILE,
    const char* jecSF_L2,
    const char* jecSF_L3,
    const char* jecSF_L23 ) : json_ins(jsonFILE)
{

    printf("[JEC_JER_Corrector] Loaded file %s\n -> Key L2 : %s\n -> Key L3 : %s\n -> Key L23: %s\n",
            jsonFILE, jecSF_L2, jecSF_L3, jecSF_L23);
    this->jec_sf_L2  = this->json_ins.GetKey(jecSF_L2);
    this->jec_sf_L3  = this->json_ins.GetKey(jecSF_L3);
    this->jec_sf_L23 = this->json_ins.GetKey(jecSF_L23);
}
TLorentzVector JEC_JER_Corrector::JEC_Corrected(const TLorentzVector& origP4)
{
  Float_t raw_pt = origP4.Pt();
  Float_t raw_eta= origP4.Eta();
  Float_t jet_raw_jec_sf_L2 = jec_sf_L2->evaluate({raw_eta,raw_pt});
  Float_t jet_raw_jec_sf_L3 = jec_sf_L3->evaluate({raw_eta,raw_pt*jet_raw_jec_sf_L2});	   
  Float_t jet_raw_sf_L23   = jec_sf_L23->evaluate({raw_eta,raw_pt*jet_raw_jec_sf_L2*jet_raw_jec_sf_L3});
  return origP4 * (jet_raw_jec_sf_L2*jet_raw_jec_sf_L3*jet_raw_sf_L23);
}


Photon_EnergySmear::Photon_EnergySmear(const char* jsonFILE,
      const char* phoSMEAR
    ) : json_ins(jsonFILE), rnd(0) // 0 computed seed via UUID object
{ cset_smear = this->json_ins.GetKey(phoSMEAR); }

Float_t Photon_EnergySmear::EvaluatePt(float phoPT, float phoETA, float phoR9)
{
  this->tmp_rho = -99;
  Float_t rho    = this->cset_smear->evaluate({"rho",phoETA,phoR9});
  Float_t smear  = this->rnd.Gaus(1,rho);
  this->tmp_rho = rho; // check the identity without run.Gaus()
  return phoPT * smear;
}

Photon_EnergyScale::Photon_EnergyScale(const char* jsonFILE,
      const char* phoSCALE
    ) : json_ins(jsonFILE)
{ this->cset_scale = this->json_ins.GetKey(phoSCALE); }

Float_t Photon_EnergyScale::EvaluatePt(float phoPT, float phoETA, float phoR9, UChar_t phoSEEDgain, UInt_t runNUMBER)
{
  Float_t Run = runNUMBER;
  Float_t scale = 1.0*this->cset_scale->evaluate({"total_correction",phoSEEDgain,Run,phoETA,phoR9,phoPT});
  return phoPT * scale;
}
#endif
#define __JEC_JER_Corrector_CC__
#endif
