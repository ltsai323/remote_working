#ifndef __MyGenMatching_h__
#define __MyGenMatching_h__

namespace GenMatching
{
  ROOT::VecOps::RVec<float> GenVarFloat(
      const ROOT::VecOps::RVec<short>& genIDX,
      const ROOT::VecOps::RVec<float>& genPARTICLEinfo);
  ROOT::VecOps::RVec<int  > GenVarInt(
      const ROOT::VecOps::RVec<short>& genIDX,
      const ROOT::VecOps::RVec<int  >& genPARTICLEinfo);
};



// detail inside the same file
#define __MyGenMatching_C__
#ifdef  __MyGenMatching_C__
#include <numeric>
ROOT::VecOps::RVec<float> GenMatching::GenVarFloat(
    const ROOT::VecOps::RVec<short>& genIDX,
    const ROOT::VecOps::RVec<float>& genPARTICLEinfo)
{
  ROOT::VecOps::RVec<float> matchedVars(genIDX.size());
  for ( size_t iGenIdx = 0; iGenIdx < genIDX.size(); ++iGenIdx )
  {
    short genIdx = genIDX[iGenIdx];
    float matchedVar = genIdx<0 ? -999 : genPARTICLEinfo[genIdx];
    matchedVars[iGenIdx] = matchedVar;
  }
  return matchedVars;
}


ROOT::VecOps::RVec<int  > GenMatching::GenVarFloat(
    const ROOT::VecOps::RVec<short>& genIDX,
    const ROOT::VecOps::RVec<int  >& genPARTICLEinfo)
{
  ROOT::VecOps::RVec<int  > matchedVars(genIDX.size());
  for ( size_t iGenIdx = 0; iGenIdx < genIDX.size(); ++iGenIdx )
  {
    short genIdx = genIDX[iGenIdx];
    float matchedVar = genIdx<0 ? -999 : genPARTICLEinfo[genIdx];
    matchedVars[iGenIdx] = matchedVar;
  }
  return matchedVars;
}

#endif // __MyGenMatching_C__
#endif // __MyGenMatching_h__

