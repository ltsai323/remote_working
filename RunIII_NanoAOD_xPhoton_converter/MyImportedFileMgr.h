#ifndef __MyImportedFileMgr_h__
#define __MyImportedFileMgr_h__
#include <map>
#include <string>


namespace ImportedFileMgr
{
  std::map<std::string, const char*> TestingFiles();
  std::map<std::string, const char*> RelativePathFiles();
  std::map<std::string, const char*> lxplusFiles();

  std::map<std::string, const char*> Factory(const std::string& identifier);
};

#define __MyImportedFileMgr_C__
#ifdef  __MyImportedFileMgr_C__

std::map<std::string, const char*> ImportedFileMgr::TestingFiles()
{
  return std::map<string, const char*> {
    { "SScorrBarrel", "data/output_ShowerShapeCorrection_barrel_1000Bins.root" },
    { "SScorrEndcap", "data/output_ShowerShapeCorrection_endcap_1000Bins.root" },
    { "tmvaBarrel","data/TMVAClassification_BDTG.weights_Barrel.xml" },
    { "tmvaEndcap","data/TMVAClassification_BDTG.weights_Endcap.xml" },
  };
}
std::map<std::string, const char*> ImportedFileMgr::RelativePathFiles()
{
  return std::map<string, const char*> {
    { "SScorrBarrel", "data/output_ShowerShapeCorrection_barrel_1000Bins.root" },
    { "SScorrEndcap", "data/output_ShowerShapeCorrection_endcap_1000Bins.root" },
    { "tmvaBarrel","data/TMVAClassification_BDTG.weights_Barrel.xml" },
    { "tmvaEndcap","data/TMVAClassification_BDTG.weights_Endcap.xml" },
  };
}
std::map<std::string, const char*> ImportedFileMgr::lxplusFiles()
{
  return std::map<string, const char*> {
    { "SScorrBarrel", "/afs/cern.ch/work/l/ltsai/ReceivedFile/for_Lian-Sheng/data/output_ShowerShapeCorrection_barrel_1000Bins.root" },
    { "SScorrEndcap", "/afs/cern.ch/work/l/ltsai/ReceivedFile/for_Lian-Sheng/data/output_ShowerShapeCorrection_endcap_1000Bins.root" },
    { "tmvaBarrel", "/afs/cern.ch/work/l/ltsai/ReceivedFile/for_Lian-Sheng/data/TMVAClassification_BDTG.weights_Barrel.xml" },
    { "tmvaEndcap", "/afs/cern.ch/work/l/ltsai/ReceivedFile/for_Lian-Sheng/data/TMVAClassification_BDTG.weights_Endcap.xml" },
  };
}

std::map<std::string, const char*> ImportedFileMgr::Factory(const std::string& identifier)
{
  if ( identifier == "test" )
    return ImportedFileMgr::TestingFiles();
  if ( identifier == "relative" )
    return ImportedFileMgr::RelativePathFiles();
  if ( identifier == "lxplus" )
    return ImportedFileMgr::lxplusFiles();
  throw "Error";
}
#endif
#endif
