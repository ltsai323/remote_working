#ifndef __CTaggingMgr_h__
#define __CTaggingMgr_h__
#include <map>
#include <string>
#include <vector>
#include "BTagCalibrationStandalone.h"
#include <memory>
#include <map>
#include <TTree.h>
#include "TFile.h"
#include "TH2F.h"


#define MAXNSYST 100
#define HADRONFLAV_B 5
#define HADRONFLAV_C 4
#define HADRONFLAV_L 0

#define NOTHING -99


struct FlavourTH2
{
    TH2F* b;
    TH2F* c;
    TH2F* l;

    TH2F* GetFlavourHist(int flav)
    {
        if (flav == 4) return c;
        if (flav == 5) return b;
        return l;
    }
};

struct CTagWeightHelper
{
    CTagWeightHelper( const char* ifile );
    ~CTagWeightHelper();

    double gethistcontent( FlavourTH2& hists, int flav, float CvsBval, float CvsLval )
    {
        TH2* wtHist = hists.GetFlavourHist(flav);
        int xbin = wtHist->GetXaxis()->FindBin(CvsLval);
        int ybin = wtHist->GetYaxis()->FindBin(CvsBval);
        return wtHist->GetBinContent(xbin,ybin);
    }

    double GetWeight(int flav, float CvsBval, float CvsLval)
    { return gethistcontent(h_central , flav, CvsBval, CvsLval); }
    double GetWeightErrUp(int flav, const std::string& uncNAME, float CvsBval, float CvsLval)
    { return gethistcontent(h_UncUp[uncNAME], flav, CvsBval, CvsLval); }
    double GetWeightErrDown(int flav, const std::string& uncNAME, float CvsBval, float CvsLval)
    { return gethistcontent(h_UncDn[uncNAME], flav, CvsBval, CvsLval); }



    TFile* wtFile;

    FlavourTH2 h_central;
    std::map<std::string, FlavourTH2> h_UncUp;
    std::map<std::string, FlavourTH2> h_UncDn;

    
};

class CTaggingMgr
{
public:
    CTaggingMgr(const char* dataera, const char* algoType, bool isMC = true); // : _algoType(algoType)

    virtual void RegBranch(TTree* t) final;
    virtual void FillBranch() = 0;
    virtual void SetBranchAddress(TTree* t) = 0;
    virtual float GetWeight() { return weight_central; }

    virtual void calculation(int flav, float bval, float cval, float lval) final;
    
    virtual ~CTaggingMgr() {}

    bool IsMC() const { return _isMC; }
private:
    CTagWeightHelper* helper;
    const char* _algoType;
    float cvsb, cvsl, bscore;
    float weight_central;

    //float weight_ExtrapUp             ;
    //float weight_InterpUp             ;
    //float weight_LHEScaleWeight_muFUp ;
    //float weight_LHEScaleWeight_muRUp ;
    //float weight_PSWeightFSRFixedUp   ;
    //float weight_PSWeightISRFixedUp   ;
    float weight_PUWeightUp           ;
    float weight_StatUp               ;
    float weight_TotalUncUp           ;
    //float weight_XSec_BRUnc_DYJets_bUp;
    //float weight_XSec_BRUnc_DYJets_cUp;
    //float weight_XSec_BRunc_WJets_cUp ;
    //float weight_jerUp                ;
    //float weight_jesTotalUp           ;

    //float weight_ExtrapDown             ;
    //float weight_InterpDown             ;
    //float weight_LHEScaleWeight_muFDown ;
    //float weight_LHEScaleWeight_muRDown ;
    //float weight_PSWeightFSRFixedDown   ;
    //float weight_PSWeightISRFixedDown   ;
    float weight_PUWeightDown           ;
    float weight_StatDown               ;
    float weight_TotalUncDown           ;
    //float weight_XSec_BRUnc_DYJets_bDown;
    //float weight_XSec_BRUnc_DYJets_cDown;
    //float weight_XSec_BRunc_WJets_cDown ;
    //float weight_jerDown                ;
    //float weight_jesTotalDown           ;

    void InitVars();
    bool _isMC;
};
class CTaggingMgr_DeepFlavour : public CTaggingMgr
{
    public:
    CTaggingMgr_DeepFlavour(const char* dataera, bool isMC); // : CTaggingMgr(dataera, "DeepFlavour") {}
    virtual void SetBranchAddress(TTree* t) override;
    virtual void FillBranch() override;
    virtual ~CTaggingMgr_DeepFlavour() {}
    private:
    float _bval, _bbval, _blep, _cval, _qval, _gval;
    int _hadflvr;
};
class CTaggingMgr_DeepCSV : public CTaggingMgr
{
    public:
    CTaggingMgr_DeepCSV(const char* dataera, bool isMC); // : CTaggingMgr(dataera, "DeepCSV") {}
    virtual void SetBranchAddress(TTree* t) override;
    virtual void FillBranch() override;
    virtual ~CTaggingMgr_DeepCSV() {}
    private:
    float _bval, _bbval, _cval, _lval;
    int _hadflvr;
};















#define __CTaggingMgr_CC__
#ifdef  __CTaggingMgr_CC__

#include "ExternalFilesMgr.h"
#include <string>
#include "LogMgr.h"
 /////////////////////////////// special note ///////////////////////////////
 //  The calculated weight need to be renormalized after final selection   //
 //  The integrated weight is not promised to be 1. So a normalization     //
 //  factor would be needed.                                               //
 ////////////////////////////////////////////////////////////////////////////


CTagWeightHelper::CTagWeightHelper( const char* ifile ) : wtFile(nullptr)
{
    if ( ifile == nullptr ) return;
    wtFile = TFile::Open(ifile);


    h_central.c = (TH2F*)wtFile->Get("SFc_hist");   //For systematic variations, one can concatenate a string after "SFc_hist"
    h_central.b = (TH2F*)wtFile->Get("SFb_hist");
    h_central.l = (TH2F*)wtFile->Get("SFl_hist");




    //h_UncUp["Extrap"             ] = FlavourTH2();
    //h_UncUp["Extrap"             ].c = (TH2F*)wtFile->Get("SFc_hist_ExtrapUp");
    //h_UncUp["Extrap"             ].b = (TH2F*)wtFile->Get("SFc_hist_ExtrapUp");
    //h_UncUp["Extrap"             ].l = (TH2F*)wtFile->Get("SFl_hist_ExtrapUp");
    //h_UncUp["Interp"             ] = FlavourTH2();
    //h_UncUp["Interp"             ].c = (TH2F*)wtFile->Get("SFc_hist_InterpUp");
    //h_UncUp["Interp"             ].b = (TH2F*)wtFile->Get("SFb_hist_InterpUp");
    //h_UncUp["Interp"             ].l = (TH2F*)wtFile->Get("SFl_hist_InterpUp");
    //h_UncUp["LHEScaleWeight_muF" ] = FlavourTH2();
    //h_UncUp["LHEScaleWeight_muF" ].c = (TH2F*)wtFile->Get("SFc_hist_LHEScaleWeight_muFUp");
    //h_UncUp["LHEScaleWeight_muF" ].b = (TH2F*)wtFile->Get("SFb_hist_LHEScaleWeight_muFUp");
    //h_UncUp["LHEScaleWeight_muF" ].l = (TH2F*)wtFile->Get("SFl_hist_LHEScaleWeight_muFUp");
    //h_UncUp["LHEScaleWeight_muR" ] = FlavourTH2();
    //h_UncUp["LHEScaleWeight_muR" ].c = (TH2F*)wtFile->Get("SFc_hist_LHEScaleWeight_muRUp");
    //h_UncUp["LHEScaleWeight_muR" ].b = (TH2F*)wtFile->Get("SFb_hist_LHEScaleWeight_muRUp");
    //h_UncUp["LHEScaleWeight_muR" ].l = (TH2F*)wtFile->Get("SFl_hist_LHEScaleWeight_muRUp");
    //h_UncUp["PSWeightFSRFixed"   ] = FlavourTH2();
    //h_UncUp["PSWeightFSRFixed"   ].c = (TH2F*)wtFile->Get("SFc_hist_PSWeightFSRFixedUp");
    //h_UncUp["PSWeightFSRFixed"   ].b = (TH2F*)wtFile->Get("SFb_hist_PSWeightFSRFixedUp");
    //h_UncUp["PSWeightFSRFixed"   ].l = (TH2F*)wtFile->Get("SFl_hist_PSWeightFSRFixedUp");
    //h_UncUp["PSWeightISRFixed"   ] = FlavourTH2();
    //h_UncUp["PSWeightISRFixed"   ].c = (TH2F*)wtFile->Get("SFc_hist_PSWeightISRFixedUp");
    //h_UncUp["PSWeightISRFixed"   ].b = (TH2F*)wtFile->Get("SFb_hist_PSWeightISRFixedUp");
    //h_UncUp["PSWeightISRFixed"   ].l = (TH2F*)wtFile->Get("SFl_hist_PSWeightISRFixedUp");
    h_UncUp["PUWeight"           ] = FlavourTH2();
    h_UncUp["PUWeight"           ].c = (TH2F*)wtFile->Get("SFc_hist_PUWeightUp");
    h_UncUp["PUWeight"           ].b = (TH2F*)wtFile->Get("SFb_hist_PUWeightUp");
    h_UncUp["PUWeight"           ].l = (TH2F*)wtFile->Get("SFl_hist_PUWeightUp");
    h_UncUp["Stat"               ] = FlavourTH2();
    h_UncUp["Stat"               ].c = (TH2F*)wtFile->Get("SFc_hist_StatUp");
    h_UncUp["Stat"               ].b = (TH2F*)wtFile->Get("SFb_hist_StatUp");
    h_UncUp["Stat"               ].l = (TH2F*)wtFile->Get("SFl_hist_StatUp");
    h_UncUp["TotalUnc"           ] = FlavourTH2();
    h_UncUp["TotalUnc"           ].c = (TH2F*)wtFile->Get("SFc_hist_TotalUncUp");
    h_UncUp["TotalUnc"           ].b = (TH2F*)wtFile->Get("SFb_hist_TotalUncUp");
    h_UncUp["TotalUnc"           ].l = (TH2F*)wtFile->Get("SFl_hist_TotalUncUp");
    //h_UncUp["XSec_BRUnc_DYJets_b"] = FlavourTH2();
    //h_UncUp["XSec_BRUnc_DYJets_b"].c = (TH2F*)wtFile->Get("SFc_hist_XSec_BRUnc_DYJets_bUp");
    //h_UncUp["XSec_BRUnc_DYJets_b"].b = (TH2F*)wtFile->Get("SFb_hist_XSec_BRUnc_DYJets_bUp");
    //h_UncUp["XSec_BRUnc_DYJets_b"].l = (TH2F*)wtFile->Get("SFl_hist_XSec_BRUnc_DYJets_bUp");
    //h_UncUp["XSec_BRUnc_DYJets_c"] = FlavourTH2();
    //h_UncUp["XSec_BRUnc_DYJets_c"].c = (TH2F*)wtFile->Get("SFc_hist_XSec_BRUnc_DYJets_cUp");
    //h_UncUp["XSec_BRUnc_DYJets_c"].b = (TH2F*)wtFile->Get("SFb_hist_XSec_BRUnc_DYJets_cUp");
    //h_UncUp["XSec_BRUnc_DYJets_c"].l = (TH2F*)wtFile->Get("SFl_hist_XSec_BRUnc_DYJets_cUp");
    //h_UncUp["XSec_BRunc_WJets_c" ] = FlavourTH2();
    //h_UncUp["XSec_BRunc_WJets_c" ].c = (TH2F*)wtFile->Get("SFc_hist_XSec_BRUnc_WJets_cUp");
    //h_UncUp["XSec_BRunc_WJets_c" ].b = (TH2F*)wtFile->Get("SFb_hist_XSec_BRUnc_WJets_cUp");
    //h_UncUp["XSec_BRunc_WJets_c" ].l = (TH2F*)wtFile->Get("SFl_hist_XSec_BRUnc_WJets_cUp");
    //h_UncUp["jer"                ] = FlavourTH2();
    //h_UncUp["jer"                ].c = (TH2F*)wtFile->Get("SFc_hist_jerUp");
    //h_UncUp["jer"                ].b = (TH2F*)wtFile->Get("SFb_hist_jerUp");
    //h_UncUp["jer"                ].l = (TH2F*)wtFile->Get("SFl_hist_jerUp");
    //h_UncUp["jesTotal"           ] = FlavourTH2();
    //h_UncUp["jesTotal"           ].c = (TH2F*)wtFile->Get("SFc_hist_jesTotalUp");
    //h_UncUp["jesTotal"           ].b = (TH2F*)wtFile->Get("SFb_hist_jesTotalUp");
    //h_UncUp["jesTotal"           ].l = (TH2F*)wtFile->Get("SFl_hist_jesTotalUp");


    //h_UncDn["Extrap"             ] = FlavourTH2();
    //h_UncDn["Extrap"             ].c = (TH2F*)wtFile->Get("SFc_hist_ExtrapDown");
    //h_UncDn["Extrap"             ].b = (TH2F*)wtFile->Get("SFc_hist_ExtrapDown");
    //h_UncDn["Extrap"             ].l = (TH2F*)wtFile->Get("SFl_hist_ExtrapDown");
    //h_UncDn["Interp"             ] = FlavourTH2();
    //h_UncDn["Interp"             ].c = (TH2F*)wtFile->Get("SFc_hist_InterpDown");
    //h_UncDn["Interp"             ].b = (TH2F*)wtFile->Get("SFb_hist_InterpDown");
    //h_UncDn["Interp"             ].l = (TH2F*)wtFile->Get("SFl_hist_InterpDown");
    //h_UncDn["LHEScaleWeight_muF" ] = FlavourTH2();
    //h_UncDn["LHEScaleWeight_muF" ].c = (TH2F*)wtFile->Get("SFc_hist_LHEScaleWeight_muFDown");
    //h_UncDn["LHEScaleWeight_muF" ].b = (TH2F*)wtFile->Get("SFb_hist_LHEScaleWeight_muFDown");
    //h_UncDn["LHEScaleWeight_muF" ].l = (TH2F*)wtFile->Get("SFl_hist_LHEScaleWeight_muFDown");
    //h_UncDn["LHEScaleWeight_muR" ] = FlavourTH2();
    //h_UncDn["LHEScaleWeight_muR" ].c = (TH2F*)wtFile->Get("SFc_hist_LHEScaleWeight_muRDown");
    //h_UncDn["LHEScaleWeight_muR" ].b = (TH2F*)wtFile->Get("SFb_hist_LHEScaleWeight_muRDown");
    //h_UncDn["LHEScaleWeight_muR" ].l = (TH2F*)wtFile->Get("SFl_hist_LHEScaleWeight_muRDown");
    //h_UncDn["PSWeightFSRFixed"   ] = FlavourTH2();
    //h_UncDn["PSWeightFSRFixed"   ].c = (TH2F*)wtFile->Get("SFc_hist_PSWeightFSRFixedDown");
    //h_UncDn["PSWeightFSRFixed"   ].b = (TH2F*)wtFile->Get("SFb_hist_PSWeightFSRFixedDown");
    //h_UncDn["PSWeightFSRFixed"   ].l = (TH2F*)wtFile->Get("SFl_hist_PSWeightFSRFixedDown");
    //h_UncDn["PSWeightISRFixed"   ] = FlavourTH2();
    //h_UncDn["PSWeightISRFixed"   ].c = (TH2F*)wtFile->Get("SFc_hist_PSWeightISRFixedDown");
    //h_UncDn["PSWeightISRFixed"   ].b = (TH2F*)wtFile->Get("SFb_hist_PSWeightISRFixedDown");
    //h_UncDn["PSWeightISRFixed"   ].l = (TH2F*)wtFile->Get("SFl_hist_PSWeightISRFixedDown");
    h_UncDn["PUWeight"           ] = FlavourTH2();
    h_UncDn["PUWeight"           ].c = (TH2F*)wtFile->Get("SFc_hist_PUWeightDown");
    h_UncDn["PUWeight"           ].b = (TH2F*)wtFile->Get("SFb_hist_PUWeightDown");
    h_UncDn["PUWeight"           ].l = (TH2F*)wtFile->Get("SFl_hist_PUWeightDown");
    h_UncDn["Stat"               ] = FlavourTH2();
    h_UncDn["Stat"               ].c = (TH2F*)wtFile->Get("SFc_hist_StatDown");
    h_UncDn["Stat"               ].b = (TH2F*)wtFile->Get("SFb_hist_StatDown");
    h_UncDn["Stat"               ].l = (TH2F*)wtFile->Get("SFl_hist_StatDown");
    h_UncDn["TotalUnc"           ] = FlavourTH2();
    h_UncDn["TotalUnc"           ].c = (TH2F*)wtFile->Get("SFc_hist_TotalUncDown");
    h_UncDn["TotalUnc"           ].b = (TH2F*)wtFile->Get("SFb_hist_TotalUncDown");
    h_UncDn["TotalUnc"           ].l = (TH2F*)wtFile->Get("SFl_hist_TotalUncDown");
    //h_UncDn["XSec_BRUnc_DYJets_b"] = FlavourTH2();
    //h_UncDn["XSec_BRUnc_DYJets_b"].c = (TH2F*)wtFile->Get("SFc_hist_XSec_BRUnc_DYJets_bDown");
    //h_UncDn["XSec_BRUnc_DYJets_b"].b = (TH2F*)wtFile->Get("SFb_hist_XSec_BRUnc_DYJets_bDown");
    //h_UncDn["XSec_BRUnc_DYJets_b"].l = (TH2F*)wtFile->Get("SFl_hist_XSec_BRUnc_DYJets_bDown");
    //h_UncDn["XSec_BRUnc_DYJets_c"] = FlavourTH2();
    //h_UncDn["XSec_BRUnc_DYJets_c"].c = (TH2F*)wtFile->Get("SFc_hist_XSec_BRUnc_DYJets_cDown");
    //h_UncDn["XSec_BRUnc_DYJets_c"].b = (TH2F*)wtFile->Get("SFb_hist_XSec_BRUnc_DYJets_cDown");
    //h_UncDn["XSec_BRUnc_DYJets_c"].l = (TH2F*)wtFile->Get("SFl_hist_XSec_BRUnc_DYJets_cDown");
    //h_UncDn["XSec_BRunc_WJets_c" ] = FlavourTH2();
    //h_UncDn["XSec_BRunc_WJets_c" ].c = (TH2F*)wtFile->Get("SFc_hist_XSec_BRUnc_WJets_cDown");
    //h_UncDn["XSec_BRunc_WJets_c" ].b = (TH2F*)wtFile->Get("SFb_hist_XSec_BRUnc_WJets_cDown");
    //h_UncDn["XSec_BRunc_WJets_c" ].l = (TH2F*)wtFile->Get("SFl_hist_XSec_BRUnc_WJets_cDown");
    //h_UncDn["jer"                ] = FlavourTH2();
    //h_UncDn["jer"                ].c = (TH2F*)wtFile->Get("SFc_hist_jerDown");
    //h_UncDn["jer"                ].b = (TH2F*)wtFile->Get("SFb_hist_jerDown");
    //h_UncDn["jer"                ].l = (TH2F*)wtFile->Get("SFl_hist_jerDown");
    //h_UncDn["jesTotal"           ] = FlavourTH2();
    //h_UncDn["jesTotal"           ].c = (TH2F*)wtFile->Get("SFc_hist_jesTotalDown");
    //h_UncDn["jesTotal"           ].b = (TH2F*)wtFile->Get("SFb_hist_jesTotalDown");
    //h_UncDn["jesTotal"           ].l = (TH2F*)wtFile->Get("SFl_hist_jesTotalDown");

    return;
}
CTagWeightHelper::~CTagWeightHelper() { wtFile->Close(); wtFile = nullptr; }






CTaggingMgr::CTaggingMgr(const char* dataera, const char* algoType, bool isMC) : _algoType(algoType), _isMC(isMC)
{ helper = new CTagWeightHelper( ExternalFilesMgr::RooFile_CTagCalibs( std::string(algoType), std::string(dataera)) ); }

void CTaggingMgr::RegBranch(TTree* t)
{
    t->Branch( Form("%s.CvsB",_algoType), &cvsb, Form("%s.CvsB/F",_algoType) );
    t->Branch( Form("%s.CvsL",_algoType), &cvsl, Form("%s.CvsL/F",_algoType) );
    t->Branch( Form("%s.bScore",_algoType), &bscore, Form("%s.bScore/F",_algoType) );

    if (!IsMC() ) return;
    t->Branch( Form("%s.ctagWeight.central",_algoType), &weight_central, Form("%s.ctagWeight.central/F",_algoType) );
    //t->Branch( Form("%s.ctagWeight.TotalUncUp",_algoType), &weight_totUp, Form("%s.ctagWeight.TotalUncUp/F",_algoType) );
    //t->Branch( Form("%s.ctagWeight.TotalUncDown",_algoType), &weight_totDn, Form("%s.ctagWeight.TotalUncDown/F",_algoType) );


    //t->Branch( Form("%s.ctagWeight.ExtrapUp"             ,_algoType), &weight_ExtrapUp             , Form("%s.ctagWeight.ExtrapUp/F"             ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.InterpUp"             ,_algoType), &weight_InterpUp             , Form("%s.ctagWeight.InterpUp/F"             ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.LHEScaleWeight_muFUp" ,_algoType), &weight_LHEScaleWeight_muFUp , Form("%s.ctagWeight.LHEScaleWeight_muFUp/F" ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.LHEScaleWeight_muRUp" ,_algoType), &weight_LHEScaleWeight_muRUp , Form("%s.ctagWeight.LHEScaleWeight_muRUp/F" ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.PSWeightFSRFixedUp"   ,_algoType), &weight_PSWeightFSRFixedUp   , Form("%s.ctagWeight.PSWeightFSRFixedUp/F"   ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.PSWeightISRFixedUp"   ,_algoType), &weight_PSWeightISRFixedUp   , Form("%s.ctagWeight.PSWeightISRFixedUp/F"   ,_algoType) );
    t->Branch( Form("%s.ctagWeight.PUWeightUp"           ,_algoType), &weight_PUWeightUp           , Form("%s.ctagWeight.PUWeightUp/F"           ,_algoType) );
    t->Branch( Form("%s.ctagWeight.StatUp"               ,_algoType), &weight_StatUp               , Form("%s.ctagWeight.StatUp/F"               ,_algoType) );
    t->Branch( Form("%s.ctagWeight.TotalUncDown"           ,_algoType), &weight_TotalUncUp           , Form("%s.ctagWeight.TotalUncUp/F"           ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.XSec_BRUnc_DYJets_bUp",_algoType), &weight_XSec_BRUnc_DYJets_bUp, Form("%s.ctagWeight.XSec_BRUnc_DYJets_bUp/F",_algoType) );
    //t->Branch( Form("%s.ctagWeight.XSec_BRUnc_DYJets_cUp",_algoType), &weight_XSec_BRUnc_DYJets_cUp, Form("%s.ctagWeight.XSec_BRUnc_DYJets_cUp/F",_algoType) );
    //t->Branch( Form("%s.ctagWeight.XSec_BRunc_WJets_cUp" ,_algoType), &weight_XSec_BRunc_WJets_cUp , Form("%s.ctagWeight.XSec_BRunc_WJets_cUp/F" ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.jerUp"                ,_algoType), &weight_jerUp                , Form("%s.ctagWeight.jerUp/F"                ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.jesTotalUp"           ,_algoType), &weight_jesTotalUp           , Form("%s.ctagWeight.jesTotalUp/F"           ,_algoType) );



    //t->Branch( Form("%s.ctagWeight.ExtrapDown"             ,_algoType), &weight_ExtrapDown             , Form("%s.ctagWeight.ExtrapDown/F"             ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.InterpDown"             ,_algoType), &weight_InterpDown             , Form("%s.ctagWeight.InterpDown/F"             ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.LHEScaleWeight_muFDown" ,_algoType), &weight_LHEScaleWeight_muFDown , Form("%s.ctagWeight.LHEScaleWeight_muFDown/F" ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.LHEScaleWeight_muRDown" ,_algoType), &weight_LHEScaleWeight_muRDown , Form("%s.ctagWeight.LHEScaleWeight_muRDown/F" ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.PSWeightFSRFixedDown"   ,_algoType), &weight_PSWeightFSRFixedDown   , Form("%s.ctagWeight.PSWeightFSRFixedDown/F"   ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.PSWeightISRFixedDown"   ,_algoType), &weight_PSWeightISRFixedDown   , Form("%s.ctagWeight.PSWeightISRFixedDown/F"   ,_algoType) );
    t->Branch( Form("%s.ctagWeight.PUWeightDown"           ,_algoType), &weight_PUWeightDown           , Form("%s.ctagWeight.PUWeightDown/F"           ,_algoType) );
    t->Branch( Form("%s.ctagWeight.StatDown"               ,_algoType), &weight_StatDown               , Form("%s.ctagWeight.StatDown/F"               ,_algoType) );
    t->Branch( Form("%s.ctagWeight.TotalUncDown"           ,_algoType), &weight_TotalUncDown           , Form("%s.ctagWeight.TotalUncDown/F"           ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.XSec_BRUnc_DYJets_bDown",_algoType), &weight_XSec_BRUnc_DYJets_bDown, Form("%s.ctagWeight.XSec_BRUnc_DYJets_bDown/F",_algoType) );
    //t->Branch( Form("%s.ctagWeight.XSec_BRUnc_DYJets_cDown",_algoType), &weight_XSec_BRUnc_DYJets_cDown, Form("%s.ctagWeight.XSec_BRUnc_DYJets_cDown/F",_algoType) );
    //t->Branch( Form("%s.ctagWeight.XSec_BRunc_WJets_cDown" ,_algoType), &weight_XSec_BRunc_WJets_cDown , Form("%s.ctagWeight.XSec_BRunc_WJets_cDown/F" ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.jerDown"                ,_algoType), &weight_jerDown                , Form("%s.ctagWeight.jerDown/F"                ,_algoType) );
    //t->Branch( Form("%s.ctagWeight.jesTotalDown"           ,_algoType), &weight_jesTotalDown           , Form("%s.ctagWeight.jesTotalDown/F"           ,_algoType) );
}

void CTaggingMgr::calculation(int flav, float bval, float cval, float lval)
{
    InitVars();

    // algorithm according to https://twiki.cern.ch/twiki/bin/viewauth/CMS/CTaggerShapeCalibration?fbclid=IwAR1_BlK2OeoMwvU_w7niCAZrC2swm8OT23bOGXK_mq-ngF_C_7JAEot6EL0
    if ( (cval < 0) || ((cval+lval) == 0) || ((cval+bval) == 0 ) ) return;
    cvsb = cval/(cval+bval);
    cvsl = cval/(cval+lval);
    //bscore = (cvsl*(1.-cvsb)) / (cvsl+cvsb - cvsl*cvsb);
    bscore = bval;
    if (!IsMC() ) return;
    

    weight_central = helper->GetWeight(flav, cvsb, cvsl);
    weight_TotalUncUp = helper->GetWeightErrUp(flav, "TotalUnc", cvsb, cvsl);
    weight_TotalUncDown = helper->GetWeightErrDown(flav, "TotalUnc", cvsb, cvsl);

    //weight_ExtrapUp              = helper->GetWeightErrUp(flav, "Extrap"             , cvsb, cvsl);
    //weight_InterpUp              = helper->GetWeightErrUp(flav, "Interp"             , cvsb, cvsl);
    //weight_LHEScaleWeight_muFUp  = helper->GetWeightErrUp(flav, "LHEScaleWeight_muF" , cvsb, cvsl);
    //weight_LHEScaleWeight_muRUp  = helper->GetWeightErrUp(flav, "LHEScaleWeight_muR" , cvsb, cvsl);
    //weight_PSWeightFSRFixedUp    = helper->GetWeightErrUp(flav, "PSWeightFSRFixed"   , cvsb, cvsl);
    //weight_PSWeightISRFixedUp    = helper->GetWeightErrUp(flav, "PSWeightISRFixed"   , cvsb, cvsl);
    weight_PUWeightUp            = helper->GetWeightErrUp(flav, "PUWeight"           , cvsb, cvsl);
    weight_StatUp                = helper->GetWeightErrUp(flav, "Stat"               , cvsb, cvsl);
    weight_TotalUncUp            = helper->GetWeightErrUp(flav, "TotalUnc"           , cvsb, cvsl);
    //weight_XSec_BRUnc_DYJets_bUp = helper->GetWeightErrUp(flav, "XSec_BRUnc_DYJets_b", cvsb, cvsl);
    //weight_XSec_BRUnc_DYJets_cUp = helper->GetWeightErrUp(flav, "XSec_BRUnc_DYJets_c", cvsb, cvsl);
    //weight_XSec_BRunc_WJets_cUp  = helper->GetWeightErrUp(flav, "XSec_BRunc_WJets_c" , cvsb, cvsl);
    //weight_jerUp                 = helper->GetWeightErrUp(flav, "jer"                , cvsb, cvsl);
    //weight_jesTotalUp            = helper->GetWeightErrUp(flav, "jesTotal"           , cvsb, cvsl);

    //weight_ExtrapDown              = helper->GetWeightErrDown(flav, "Extrap"             , cvsb, cvsl);
    //weight_InterpDown              = helper->GetWeightErrDown(flav, "Interp"             , cvsb, cvsl);
    //weight_LHEScaleWeight_muFDown  = helper->GetWeightErrDown(flav, "LHEScaleWeight_muF" , cvsb, cvsl);
    //weight_LHEScaleWeight_muRDown  = helper->GetWeightErrDown(flav, "LHEScaleWeight_muR" , cvsb, cvsl);
    //weight_PSWeightFSRFixedDown    = helper->GetWeightErrDown(flav, "PSWeightFSRFixed"   , cvsb, cvsl);
    //weight_PSWeightISRFixedDown    = helper->GetWeightErrDown(flav, "PSWeightISRFixed"   , cvsb, cvsl);
    weight_PUWeightDown            = helper->GetWeightErrDown(flav, "PUWeight"           , cvsb, cvsl);
    weight_StatDown                = helper->GetWeightErrDown(flav, "Stat"               , cvsb, cvsl);
    weight_TotalUncDown            = helper->GetWeightErrDown(flav, "TotalUnc"           , cvsb, cvsl);
    //weight_XSec_BRUnc_DYJets_bDown = helper->GetWeightErrDown(flav, "XSec_BRUnc_DYJets_b", cvsb, cvsl);
    //weight_XSec_BRUnc_DYJets_cDown = helper->GetWeightErrDown(flav, "XSec_BRUnc_DYJets_c", cvsb, cvsl);
    //weight_XSec_BRunc_WJets_cDown  = helper->GetWeightErrDown(flav, "XSec_BRunc_WJets_c" , cvsb, cvsl);
    //weight_jerDown                 = helper->GetWeightErrDown(flav, "jer"                , cvsb, cvsl);
    //weight_jesTotalDown            = helper->GetWeightErrDown(flav, "jesTotal"           , cvsb, cvsl);

}

void CTaggingMgr::InitVars()
{
    cvsb = NOTHING;
    cvsl = NOTHING;
    bscore = NOTHING;
    weight_central = NOTHING;
    //weight_ExtrapUp              = NOTHING;
    //weight_InterpUp              = NOTHING;
    //weight_LHEScaleWeight_muFUp  = NOTHING;
    //weight_LHEScaleWeight_muRUp  = NOTHING;
    //weight_PSWeightFSRFixedUp    = NOTHING;
    //weight_PSWeightISRFixedUp    = NOTHING;
    weight_PUWeightUp            = NOTHING;
    weight_StatUp                = NOTHING;
    weight_TotalUncUp            = NOTHING;
    //weight_XSec_BRUnc_DYJets_bUp = NOTHING;
    //weight_XSec_BRUnc_DYJets_cUp = NOTHING;
    //weight_XSec_BRunc_WJets_cUp  = NOTHING;
    //weight_jerUp                 = NOTHING;
    //weight_jesTotalUp            = NOTHING;

    //weight_ExtrapDown              = NOTHING;
    //weight_InterpDown              = NOTHING;
    //weight_LHEScaleWeight_muFDown  = NOTHING;
    //weight_LHEScaleWeight_muRDown  = NOTHING;
    //weight_PSWeightFSRFixedDown    = NOTHING;
    //weight_PSWeightISRFixedDown    = NOTHING;
    weight_PUWeightDown            = NOTHING;
    weight_StatDown                = NOTHING;
    weight_TotalUncDown            = NOTHING;
    //weight_XSec_BRUnc_DYJets_bDown = NOTHING;
    //weight_XSec_BRUnc_DYJets_cDown = NOTHING;
    //weight_XSec_BRunc_WJets_cDown  = NOTHING;
    //weight_jerDown                 = NOTHING;
    //weight_jesTotalDown            = NOTHING;
}








CTaggingMgr_DeepFlavour::CTaggingMgr_DeepFlavour(const char* dataera, bool isMC) : CTaggingMgr(dataera, "DeepFlavour", isMC) {}
void CTaggingMgr_DeepFlavour::SetBranchAddress(TTree* t)
{
    // b = b+bb+b_lep
    // l = uds + g
    t->SetBranchAddress("jetDeepFlavourTags_bb"  ,&_bbval);
    t->SetBranchAddress("jetDeepFlavourTags_b"   , &_bval);
    t->SetBranchAddress("jetDeepFlavourTags_lepb", &_blep);
    t->SetBranchAddress("jetDeepFlavourTags_c"   , &_cval);
    t->SetBranchAddress("jetDeepFlavourTags_uds" , &_qval);
    t->SetBranchAddress("jetDeepFlavourTags_g"   , &_gval);

    if (!IsMC()) return;
    t->SetBranchAddress("jetHadFlvr", &_hadflvr);
}
void CTaggingMgr_DeepFlavour::FillBranch()
{
    this->calculation(_hadflvr, _bval+_bbval+_blep, _cval, _qval+_gval);
}





CTaggingMgr_DeepCSV::CTaggingMgr_DeepCSV(const char* dataera, bool isMC) : CTaggingMgr(dataera, "DeepCSV", isMC) {}
void CTaggingMgr_DeepCSV::SetBranchAddress(TTree* t)
{
    t->SetBranchAddress("jetDeepCSVTags_bb"  ,&_bbval);
    t->SetBranchAddress("jetDeepCSVTags_b"   , &_bval);
    t->SetBranchAddress("jetDeepCSVTags_c"   , &_cval);
    t->SetBranchAddress("jetDeepCSVTags_udsg", &_lval);

    if (!IsMC()) return;
    t->SetBranchAddress("jetHadFlvr", &_hadflvr);
}
void CTaggingMgr_DeepCSV::FillBranch()
{
    this->calculation(_hadflvr, _bval+_bbval, _cval, _lval);
}

#endif // end of __CTaggingMgr_CC__
#endif // end of __CTaggingMgr_h__

