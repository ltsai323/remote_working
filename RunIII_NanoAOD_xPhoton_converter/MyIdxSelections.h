#ifndef __MyIdxSelections_h__
#define __MyIdxSelections_h__

namespace IdxSelections
{
  float GetFloat ( short theIDX, const ROOT::VecOps::RVec<float>& vecINFO);
  int   GetInt   ( short theIDX, const ROOT::VecOps::RVec<int  >& vecINFO);
  short GetShort ( short theIDX, const ROOT::VecOps::RVec<short>& vecINFO);
  short GetShort2( unsigned long theIDX, const ROOT::VecOps::RVec<short>& vecINFO);
  unsigned char GetUChar( short theIDX, const ROOT::VecOps::RVec<unsigned char>& vecINFO);
  unsigned short GetUShort( short theIDX, const ROOT::VecOps::RVec<unsigned short>& vecINFO);
  unsigned long GetULong ( short theIDX, const ROOT::VecOps::RVec<unsigned long>& vecINFO);
  ROOT::VecOps::RVec<float> GetFloatArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<float>& vecINFO);
  ROOT::VecOps::RVec<int  > GetIntArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<int  >& vecINFO);
  ROOT::VecOps::RVec<short> GetShortArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<short>& vecINFO);
  ROOT::VecOps::RVec<unsigned short> GetUShortArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<unsigned short>& vecINFO);

  int IndexOfSelectedLeadingCandidate(const ROOT::VecOps::RVec<int>& isSELECTED, const ROOT::VecOps::RVec<float>& candPT);
};



// detail inside the same file
#define __MyIdxSelections_C__
#ifdef  __MyIdxSelections_C__
float IdxSelections::GetFloat ( short theIDX, const ROOT::VecOps::RVec<float>& vecINFO)
{ return theIDX<0 ? -999 : vecINFO[theIDX]; }
int   IdxSelections::GetInt   ( short theIDX, const ROOT::VecOps::RVec<int  >& vecINFO)
{ return theIDX<0 ? -999 : vecINFO[theIDX]; }
short IdxSelections::GetShort ( short theIDX, const ROOT::VecOps::RVec<short>& vecINFO)
{ return theIDX<0 ? -999 : vecINFO[theIDX]; }
short IdxSelections::GetShort2( unsigned long theIDX, const ROOT::VecOps::RVec<short>& vecINFO)
{ return theIDX<0 ? -999 : vecINFO[theIDX]; }
unsigned char IdxSelections::GetUChar( short theIDX, const ROOT::VecOps::RVec<unsigned char>& vecINFO)
{ return theIDX<0 ? 'Q' : vecINFO[theIDX]; }
unsigned short IdxSelections::GetUShort( short theIDX, const ROOT::VecOps::RVec<unsigned short>& vecINFO)
{ return theIDX<0 ? -999 : vecINFO[theIDX]; }
unsigned long IdxSelections::GetULong( short theIDX, const ROOT::VecOps::RVec<unsigned long>& vecINFO)
{ return theIDX<0 ? -999 : vecINFO[theIDX]; }

ROOT::VecOps::RVec<float> IdxSelections::GetFloatArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<float>& vecINFO)
{
  ROOT::VecOps::RVec<float> matchedVars(loadedIDXs.size());
  for ( size_t idx = 0; idx < loadedIDXs.size(); ++idx )
  {
    short loadedIDX = loadedIDXs[idx];
    float matchedVar = loadedIDX<0 ? -999 : vecINFO[loadedIDX];
    matchedVars[idx] = matchedVar;
  }
  return matchedVars;
}


ROOT::VecOps::RVec<int  > IdxSelections::GetIntArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<int  >& vecINFO)
{
  ROOT::VecOps::RVec<int  > matchedVars(loadedIDXs.size());
  for ( size_t idx = 0; idx < loadedIDXs.size(); ++idx )
  {
    short loadedIDX = loadedIDXs[idx];
    int   matchedVar = loadedIDX<0 ? -999 : vecINFO[loadedIDX];
    matchedVars[idx] = matchedVar;
  }
  return matchedVars;
}


ROOT::VecOps::RVec<short> IdxSelections::GetShortArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<short>& vecINFO)
{
  ROOT::VecOps::RVec<short> matchedVars(loadedIDXs.size());
  for ( size_t idx = 0; idx < loadedIDXs.size(); ++idx )
  {
    short loadedIDX = loadedIDXs[idx];
    short matchedVar = loadedIDX<0 ? -999 : vecINFO[loadedIDX];
    matchedVars[idx] = matchedVar;
  }
  return matchedVars;
}


ROOT::VecOps::RVec<unsigned short> IdxSelections::GetUShortArray(
      const ROOT::VecOps::RVec<short>& loadedIDXs,
      const ROOT::VecOps::RVec<unsigned short>& vecINFO)
{
  ROOT::VecOps::RVec<unsigned short> matchedVars(loadedIDXs.size());
  for ( size_t idx = 0; idx < loadedIDXs.size(); ++idx )
  {
    short loadedIDX = loadedIDXs[idx];
    unsigned short matchedVar = loadedIDX<0 ? -999 : vecINFO[loadedIDX];
    matchedVars[idx] = matchedVar;
  }
  return matchedVars;
}
int IdxSelections::IndexOfSelectedLeadingCandidate(const ROOT::VecOps::RVec<int>& isSELECTED, const ROOT::VecOps::RVec<float>& candPT)
{
  float ptMAX = -1;
  int outIDX = -1;
  for ( int iCand = 0; iCand < isSELECTED.size(); ++iCand )
  {
    if ( isSELECTED[iCand] == 0 ) continue;
    if ( candPT[iCand] > ptMAX )
    { outIDX = iCand; ptMAX = candPT[iCand]; }
  }
  return outIDX;
}
#endif // __MyIdxSelections_C__
#endif // __MyIdxSelections_h__


