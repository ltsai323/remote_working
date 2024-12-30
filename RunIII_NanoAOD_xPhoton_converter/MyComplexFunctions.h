#ifndef __MyComplexFunctions_h__
#define __MyComplexFunctions_h__
#include "TLorentzVector.h"
namespace ComplexFunctions
{
  ROOT::VecOps::RVec<TLorentzVector> Particle_PtEtaPhiM(
      const ROOT::VecOps::RVec<float>& thePT,
      const ROOT::VecOps::RVec<float>& theETA,
      const ROOT::VecOps::RVec<float>& thePHI,
      const ROOT::VecOps::RVec<float>& theMASS);
  int SecondaryIdx(const ROOT::VecOps::RVec<float>& theVAR);
};



// detail inside the same file
#define __MyComplexFunctions_C__
#ifdef  __MyComplexFunctions_C__
ROOT::VecOps::RVec<TLorentzVector> ComplexFunctions::Particle_PtEtaPhiM(
    const ROOT::VecOps::RVec<float>& thePT,
    const ROOT::VecOps::RVec<float>& theETA,
    const ROOT::VecOps::RVec<float>& thePHI,
    const ROOT::VecOps::RVec<float>& theMASS)
{
  ROOT::VecOps::RVec<TLorentzVector> particles(thePT.size());

  for ( size_t idx = 0; idx < theETA.size(); ++idx )
  {
    TLorentzVector p;
    p.SetPtEtaPhiM(
      thePT[idx],
      theETA[idx],
      thePHI[idx],
      theMASS[idx]
    );
    particles[idx] = p;
  }
  return particles;
}

int ComplexFunctions::SecondaryIdx(const ROOT::VecOps::RVec<float>& theVAR)
{
  float max_val = -1;
  float sec_val = -1;
  int max_idx = -1;
  int sec_idx = -1;
  for ( int idx = 0; idx < theVAR.size(); ++idx )
  {
    float v = theVAR[idx];
    if ( v > sec_val )
    { sec_val = v; sec_idx = idx; }
    if ( v > max_val )
    {
      sec_val = max_val; sec_idx = max_idx;
      max_val = v;       max_idx = idx;
    }
  }
  return sec_idx;
}
#endif // __MyComplexFunctions_C__
#endif // __MyComplexFunctions_h__
