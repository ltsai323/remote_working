#include "ExternalFilesMgr.h"
#include "LogMgr.h"
#include <stdio.h>

const char* ExternalFilesMgr::csvFile_BTagCalib_DeepFlavour(std::string era)
{
    if      ( era == "2016ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/2016_94XReReco/DeepJet_2016LegacySF_V1_TuneCP5.csv";
    else if ( era == "2017ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/2017_94XReReco/DeepFlavour_94XSF_V4_B_F.csv";
    else if ( era == "2018ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/2018_102XReReco/reshaping_deepJet_106XUL17_v3.csv";
// https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
    else if ( era == "UL2016PostVFP" )
return "/home/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2016postVFP/reshaping_deepJet_106XUL16postVFP_v3.csv"; 
    else if ( era == "UL2016PreVFP" )
return "/home/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2016preVFP/reshaping_deepJet_106XUL16preVFP_v2.csv"; 
    else if ( era == "UL2017"     )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2017/reshaping_deepJet_106XUL17_v3.csv";
    else if ( era == "UL2018"     )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2018/reshaping_deepJet_106XUL18_v2.csv";
    LOG_FATAL( "Unknown input argument era '%s'", era.c_str() );
    return nullptr;
}
const char* ExternalFilesMgr::csvFile_BTagCalib_DeepCSV(std::string era)
{
    if      ( era == "2016ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/2016_94XReReco/DeepCSV_2016LegacySF_V1_TuneCP5.csv";
    else if ( era == "2017ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/2017_94XReReco/DeepCSV_94XSF_V5_B_F.csv";
    else if ( era == "2018ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/2018_102XReReco/reshaping_deepCSV_106XUL17_v3.csv";
// https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
    else if ( era == "UL2016PreVFP"     )
return "/home/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2016preVFP/reshaping_deepCSV_106XUL16preVFP_v2.csv"; 
    else if ( era == "UL2016PostVFP"     )
return "/home/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2016postVFP/reshaping_deepCSV_106XUL16postVFP_v3.csv"; 
    else if ( era == "UL2017"     )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2017/reshaping_deepCSV_106XUL17_v3.csv";
    else if ( era == "UL2018"     )
        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/csvfiles/UL2018/reshaping_deepCSV_106XUL18_v2.csv";
    LOG_FATAL( "Unknown input argument era '%s'", era.c_str() );
    return nullptr;
}

const char* ExternalFilesMgr::csvFile_BTagCalibs(std::string name, std::string era)
{
    //if ( name == "CSVv2"                  ) return csvFile_BTagCalib_CSVv2(era);
    if ( name == "DeepCSV"                ) return csvFile_BTagCalib_DeepCSV(era);
    if ( name == "DeepFlavour"            ) return csvFile_BTagCalib_DeepFlavour(era);
    //if ( name == "DeepFlavour_JESReduced" ) return csvFile_BTagCalib_DeepFlavour_JESreduced(era);
    LOG_FATAL( "Unknown input argument name '%s'", name.c_str() );
    //throw std::invalid_argument("ExternalFilesMgr : Unknown input argument name ");
    return nullptr;
}

/*
const char* ExternalFilesMgr::csvFile_BTagCalibs(std::string name)
{
    if ( name == "CSVv2"                  ) return csvFile_BTagCalib_CSVv2();
    if ( name == "DeepCSV"                ) return csvFile_BTagCalib_DeepCSV();
    if ( name == "DeepFlavour"            ) return csvFile_BTagCalib_DeepFlavour();
    if ( name == "DeepFlavour_JESReduced" ) return csvFile_BTagCalib_DeepFlavour_JESreduced();
    LOG_FATAL( "Unknown input argument name '%s'", name.c_str() );
    //throw std::invalid_argument("ExternalFilesMgr : Unknown input argument name ");
    return nullptr;
}
*/

const char* ExternalFilesMgr::RooFile_CTagCalib_DeepFlavour(std::string era)
{
    if ( era == "2016ReReco" )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/2016ReReco/DeepJet_ctagSF_MiniAOD94X_2016_pTincl_01Nov20.root";
    if ( era == "2017ReReco" ) return nullptr;
    if ( era == "2018ReReco" ) return nullptr;
    if ( era == "UL2016PostVFP" )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2016PostVFP/DeepJet_ctagSF_Summer20UL16PostVFP_interp_withJEC.root";
    if ( era == "UL2016PreVFP" )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2016PreVFP/DeepJet_ctagSF_Summer20UL16PreVFP_interp_withJEC.root";
    if ( era == "UL2017"     )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2017/DeepJet_ctagSF_Summer20UL17_interp_withJEC.root";
    if ( era == "UL2018"     )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2018/DeepJet_ctagSF_Summer20UL18_interp_withJEC.root";
    LOG_FATAL( "Unknown input argument era '%s'", era.c_str() );
    return nullptr;
}
const char* ExternalFilesMgr::RooFile_CTagCalib_DeepCSV(std::string era)
{
    if ( era == "2016ReReco" )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/2016ReReco/DeepCSV_ctagSF_MiniAOD94X_2016_pTincl_01Nov20.root";
    if ( era == "2017ReReco" ) return nullptr;
    if ( era == "2018ReReco" ) return nullptr;

    if ( era == "UL2016PreVFP"     )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2016PreVFP/DeepCSV_ctagSF_Summer20UL16PreVFP_interp_withJEC.root";
    if ( era == "UL2016PostVFP"     )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2016PostVFP/DeepCSV_ctagSF_Summer20UL16PostVFP_interp_withJEC.root";
    if ( era == "UL2017"     )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2017/DeepCSV_ctagSF_Summer20UL17_interp_withJEC.root";
    if ( era == "UL2018"     )
return "/home/ltsai/ReceivedFile/GJet/CTagCalibrations/UL2018/DeepCSV_ctagSF_Summer20UL18_interp_withJEC.root";
    LOG_FATAL( "Unknown input argument era '%s'", era.c_str() );
    return nullptr;
}

const char* ExternalFilesMgr::RooFile_CTagCalibs(std::string name, std::string era)
{
    if ( name == "DeepCSV"                ) return RooFile_CTagCalib_DeepCSV(era);
    if ( name == "DeepFlavour"            ) return RooFile_CTagCalib_DeepFlavour(era);
    LOG_FATAL( "Unknown input argument name '%s'", name.c_str() );
    return nullptr;
}

const char* ExternalFilesMgr::RooFile_PileUp(std::string era)
{
    if      ( era == "2016ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/PileupWeight/2016ReReco_Moriond17/puweights_PileupHistogram-goldenJSON-13tev-2016-69200ub.root";
    else if ( era == "2017ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/PileupWeight/2017ReReco_WinterMC/puweights_PileupHistogram-goldenJSON-13tev-2017-69200ub.root";
    else if ( era == "2018ReReco" )
        return "/wk_cms/ltsai/ReceivedFile/PileupWeight/2018ReReco_JuneProjectionFull18/puweights_PileupHistogram-goldenJSON-13tev-2018-69200ub.root";
    else if ( era == "UL2016PostVFP" || era == "UL2016PreVFP" )
        return "/wk_cms/ltsai/ReceivedFile/PileupWeight/UL2016_PoissonOOTPU/puweights_PileupHistogram-goldenJSON-13tev-2016-69200ub-99bins.root";
    else if ( era == "UL2017"     )
        return "/wk_cms/ltsai/ReceivedFile/PileupWeight/UL2017_PoissonOOTPU/puweights_PileupHistogram-goldenJSON-13tev-2017-69200ub-99bins.root";
    else if ( era == "UL2018"     )
        return "/wk_cms/ltsai/ReceivedFile/PileupWeight/UL2018_PoissonOOTPU/puweights_PileupHistogram-goldenJSON-13tev-2018-69200ub-99bins.root";
    return nullptr;
}
//const char* ExternalFilesMgr::RooFile_ShowerShapeCorrection(std::string era)
//{
//    if      ( era == "2016ReReco" )
//        return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/rootfiles/external/transformation5x5_Legacy2016_v1.root";
//    else if ( era == "2017ReReco" )
//        return nullptr;
//    else if ( era == "2018ReReco" )
//        return nullptr;
//    else if ( era == "UL2016PreVFP"     ) return nullptr; // waiting for update.
//    else if ( era == "UL2016PostVFP"     ) return nullptr; // waiting for update.
//    else if ( era == "UL2017"     )
//        return nullptr;
//    else if ( era == "UL2018"     )
//        return nullptr;
//    return nullptr;
//}
const char* ExternalFilesMgr::xmlFile_MVAweight(int isEndcap, std::string era)
{
    if ( isEndcap )
    {
        if      ( era == "2016ReReco" )
            return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/xmlfiles/external/spring16_80x_EE_TMVAnalysis_BDT.weights.xml";
        else if ( era == "2017ReReco" )
            return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/xmlfiles/external/fall17_94X_EE_TMVAnalysis_BDT.weights.xml";
        else if ( era == "2018ReReco" )
            return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/xmlfiles/external/autumn18_EE_TMVAnalysis_BDT.weights.xml";
        else if ( era == "UL2016PostVFP" || era == "UL2016PreVFP" )
return "/home/ltsai/ReceivedFile/GJet/TMVATrainingResult/UL2016/UL2016_EE/weights/TMVAnalysis_BDT.weights.xml";
        else if ( era == "UL2017"     )
            return nullptr;
        else if ( era == "UL2018"     )
            return "/home/ltsai/ReceivedFile/hii/TMVA_UL2018_EE/weights/TMVAnalysis_BDT.weights.xml";
            //return "/home/ltsai/ReceivedFile/GJet/TMVATrainingResult/UL2018/TMVA_UL2018_EE/weights/TMVAnalysis_BDT.weights.xml";
    }
    else
    {
        if      ( era == "2016ReReco" )
            return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/xmlfiles/external/spring16_80x_EB_TMVAnalysis_BDT.weights.xml";
        else if ( era == "2017ReReco" )
            return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/xmlfiles/external/fall17_94X_EB_TMVAnalysis_BDT.weights.xml";
        else if ( era == "2018ReReco" )
            return "/wk_cms/ltsai/ReceivedFile/RSprocessedFiles/xmlfiles/external/autumn18_EB_TMVAnalysis_BDT.weights.xml";
        else if ( era == "UL2016PostVFP" || era == "UL2016PreVFP" )
return "/home/ltsai/ReceivedFile/GJet/TMVATrainingResult/UL2016/UL2016_EB/weights/TMVAnalysis_BDT.weights.xml";
        else if ( era == "UL2017"     )
            return nullptr;
        else if ( era == "UL2018"     )
            return "/home/ltsai/ReceivedFile/hii/TMVA_UL2018_EB/weights/TMVAnalysis_BDT.weights.xml";
            //return "/home/ltsai/ReceivedFile/GJet/TMVATrainingResult/UL2018/TMVA_UL2018_EB/weights/TMVAnalysis_BDT.weights.xml";
    }
    LOG_FATAL( "Unknown input argument era '%s'", era.c_str() );
    return nullptr;
}
