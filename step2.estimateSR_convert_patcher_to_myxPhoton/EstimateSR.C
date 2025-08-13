#include "TH1.h"
#include "TH2.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCut.h"
#include "TPaveText.h"
#include "TGaxis.h"
#include "TProfile.h"
#include "TCut.h"
#include "TChain.h"
#include "TString.h"
#include "TGraphErrors.h"
#include "TRandom.h"
#include "TMVA/Factory.h"

#include "TMVA/Reader.h"
#include "TMVA/Config.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/MethodCuts.h"
#include "TString.h"
#include <iostream>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include "TLorentzVector.h"
#include "extlib/correction.h"
#include "extlib/GetPhotonSF.h"
#include "extlib/ExternalFilesMgr.h"
#include "extlib/JEC_JER_Corrector.h"
#include "ROOT/RVec.hxx"

#define NO_SVMASS -0.4 // once a failed SV reconstructed, assign SVMass to -0.4 instead of 0

using correction::CorrectionSet;
using namespace std;
const bool SSCORR_ONLY_SIEIE = true; // because I found error from SS correction. So only use sieie correction


void BUG(const char* m) { printf("[DEBUG] %s\n", m); }
double TotalGenWeight(const char* inFILE)
{
    auto tFILE = TFile::Open(inFILE);
    auto hGenW = (TH1D*) tFILE->Get("totWgt");
    if ( hGenW == nullptr ) return -1; // is data
    double totalGenWeight = hGenW->GetBinContent(1);
    tFILE->Close();
    return totalGenWeight;
}
float myDeltaR( float eta0, float phi0, float eta, float phi )
{
    float delta_eta = std::fabs(eta-eta0);
    float delta_phi = std::fabs(phi-phi0);
    if (delta_phi > M_PI ) delta_phi = 2 * M_PI - delta_phi;

    return std::sqrt(delta_eta*delta_eta+delta_phi*delta_phi);
}

TString outfiles(const std::string& folderSTR) { return TString(folderSTR+"/out*.root"); }
TString histfile(const std::string& folderSTR) { return TString(folderSTR+".root"); }

//Photon scale and smearing files
auto cset_photon_scale_smearing_file = CorrectionSet::from_file("data/Photon_scale_smearing.json");
auto cset_scale = cset_photon_scale_smearing_file->at("Prompt2022FG_ScaleJSON");
auto cset_smearing = cset_photon_scale_smearing_file->at("Prompt2022FG_SmearingJSON");
const char* photon_smear_and_scale_file = "data/Photon_scale_smearing.json";
Photon_EnergySmear* phoSmearMgr = new Photon_EnergySmear(photon_smear_and_scale_file, "Prompt2022FG_SmearingJSON"); // for MC
Photon_EnergyScale* phoScaleMgr = new Photon_EnergyScale(photon_smear_and_scale_file, "Prompt2022FG_ScaleJSON"); // for data
                                                                                                                 //
// Apply b-tagging WP SF.
auto cset_btag_wp_sf_file = CorrectionSet::from_file("/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz");
auto cset_WPbL_lightQ = cset_btag_wp_sf_file->at("robustParticleTransformer_light");
//      For the working point correction multiple different uncertainty schemes are provided. If only
//      one year is analyzed, the 'up' and 'down' systematics can be used. If multiple data taking eras
//      are analyzed, 'up/down_correlated' and 'up/down_uncorrelated' systematics are provided to be
//      used instead of the 'up/down' ones, which are supposed to be correlated/decorrelated between the
//      different data years.
//      Node counts: Category: 43, Binning: 70, Formula: 35
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ systematic (string)                                                                          │
//      │ No description                                                                               │
//      │ Values: central, down, down_correlated, down_uncorrelated, up, up_correlated,                │
//      │ up_uncorrelated                                                                              │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ working_point (string)                                                                       │
//      │ L/M/T/XT/XXT                                                                                 │
//      │ Values: L, M, T, XT, XXT                                                                     │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ flavor (int)                                                                                 │
//      │ hadron flavor definition: 5=b, 4=c, 0=udsg                                                   │
//      │ Values: 0                                                                                    │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ abseta (real)                                                                                │
//      │ No description                                                                               │
//      │ Range: [0.0, 2.5)                                                                            │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ pt (real)                                                                                    │
//      │ No description                                                                               │
//      │ Range: [-inf, inf), overflow ok                                                              │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭─── ◀ output ───╮
//      │ weight (real)  │
//      │ No description │
//      ╰────────────────╯
auto cset_WPbL_heavyQ = cset_btag_wp_sf_file->at("robustParticleTransformer_mujets");
//  │   For the working point correction multiple different uncertainty schemes are provided. If only
//  │   one year is analyzed, the 'up' and 'down' systematics can be used. If multiple data taking eras
//  │   are analyzed, 'up/down_correlated' and 'up/down_uncorrelated' systematics are provided to be
//  │   used instead of the 'up/down' ones, which are supposed to be correlated/decorrelated between the
//  │   different data years. If the impact of b-tagging in the analysis is dominant a further breakdown
//  │   of uncertainties is provided. These broken-down sources consist of
//  │   'up/down_bfragmentation/jes/pileup/type3/statistic'. All of the sources can be correlated
//  │   between the years, except the 'statistic' source which is to be decorrelated between the years.
//  │   Node counts: Category: 103, Binning: 340, FormulaRef: 1450, Formula: 4
//  │   ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//  │   │ systematic (string)                                                                          │
//  │   │ No description                                                                               │
//  │   │ Values: central, down, down_bfragmentation, down_correlated, down_jes, down_pileup,          │
//  │   │ down_statistic, down_type3, down_uncorrelated, up, up_bfragmentation, up_correlated, up_jes, │
//  │   │ up_pileup, up_statistic, up_type3, up_uncorrelated                                           │
//  │   ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//  │   ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//  │   │ working_point (string)                                                                       │
//  │   │ L/M/T/XT/XXT                                                                                 │
//  │   │ Values: L, M, T, XT, XXT                                                                     │
//  │   ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//  │   ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//  │   │ flavor (int)                                                                                 │
//  │   │ hadron flavor definition: 5=b, 4=c, 0=udsg                                                   │
//  │   │ Values: 4, 5                                                                                 │
//  │   ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//  │   ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//  │   │ abseta (real)                                                                                │
//  │   │ No description                                                                               │
//  │   │ Range: [0.0, 2.5)                                                                            │
//  │   ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//  │   ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//  │   │ pt (real)                                                                                    │
//  │   │ No description                                                                               │
//  │   │ Range: [-inf, inf), overflow ok                                                              │
//  │   ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//  │   ╭─── ◀ output ───╮
//  │   │ weight (real)  │
//  │   │ No description │
//  │   ╰────────────────╯

auto cset_WPbValue = cset_btag_wp_sf_file->at("robustParticleTransformer_wp_values"); // defined WP value
const double WPbLValue(cset_WPbValue->evaluate({"L"}));
const double WPbMValue(cset_WPbValue->evaluate({"M"}));
const double WPbTValue(cset_WPbValue->evaluate({"T"}));

auto cset_ctag_reshape_file = CorrectionSet::from_file("/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2018_UL/ctagging.json.gz"); // fake
auto cset_ctag_reshape = cset_ctag_reshape_file->at("deepJet_shape");
//  deepJet reshaping scale factors for UL 2018. The scale factors have 13 default uncertainty
//  sources (Extrap, Interp, LHEScaleWeight_muF, LHEScaleWeight_muR, PSWeightFSR, PSWeightISR,
//  PUWeight, Stat, XSec_BRUnc_DYJets_b, XSec_BRUnc_DYJets_c, XSec_BRUnc_WJets_c, jer, jesTotal).
//  All uncertainty sources are to be correlated across jet flavors. All, except the 'Stat'
//  uncertainty are to be correlated between years.
//
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ systematic (string)                                                                          │
//      │ No description                                                                               │
//      │ Values: central, down_Extrap, down_Interp, down_LHEScaleWeight_muF, down_LHEScaleWeight_muR, │
//      │ down_PSWeightFSR, down_PSWeightISR, down_PUWeight, down_Stat, down_XSec_BRUnc_DYJets_b,      │
//      │ down_XSec_BRUnc_DYJets_c, down_XSec_BRUnc_WJets_c, down_jer, down_jesTotal, up_Extrap,       │
//      │ up_Interp, up_LHEScaleWeight_muF, up_LHEScaleWeight_muR, up_PSWeightFSR, up_PSWeightISR,     │
//      │ up_PUWeight, up_Stat, up_XSec_BRUnc_DYJets_b, up_XSec_BRUnc_DYJets_c, up_XSec_BRUnc_WJets_c, │
//      │ up_jer, up_jesTotal                                                                          │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ flavor (int)                                                                                 │
//      │ hadron flavor definition: 5=b, 4=c, 0=udsg                                                   │
//      │ Values: 0, 4, 5                                                                              │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ CvL (real)                                                                                   │
//      │ deepCSV CvL value                                                                            │
//      │ Range: [0.0, 1.0), overflow ok                                                               │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭────────────────────────────────────────── ▶ input ───────────────────────────────────────────╮
//      │ CvB (real)                                                                                   │
//      │ deepCSV CvB value                                                                            │
//      │ Range: [0.0, 1.0), overflow ok                                                               │
//      ╰──────────────────────────────────────────────────────────────────────────────────────────────╯
//      ╭─── ◀ output ───╮
//      │ weight (real)  │
//      │ No description │
//      ╰────────────────╯
                                                                                                                                                     //

//Jet JEC-JER files
auto cset_jet_jerc_file = CorrectionSet::from_file("data/jet_jerc.json");
correction::Correction::Ref jec_sf_L2;
correction::Correction::Ref jec_sf_L3;
correction::Correction::Ref jec_sf_L23;
TString   JER_corr = "Summer22EE_22Sep2023_JRV1_MC_ScaleFactor_AK4PFPuppi";
TString   JER_reso = "Summer22EE_22Sep2023_JRV1_MC_PtResolution_AK4PFPuppi";
auto jet_jerc_corr = cset_jet_jerc_file->at(std::string(JER_corr.Data()));
auto jet_jerc_reso = cset_jet_jerc_file->at(std::string(JER_reso.Data()));
//JEC_JER_Corrector jecjer_corr = LoadJECJER_from_JSON("data/jet_jerc.json");
const char* jec_jer_json = "data/jet_jerc.json";
JEC_JER_Corrector* jecjer_corr = nullptr;

//Jet-Veto map file
auto cset_jet_vetomap_file = CorrectionSet::from_file("data/jetvetomaps.json");
auto cset_veto = cset_jet_vetomap_file->at("Summer22EE_23Sep2023_RunEFG_V1");

#define fIDX_LXPLUS_GJetMadgraph100                0
#define fIDX_LXPLUS_GJetMadgraph200                1
#define fIDX_LXPLUS_GJetMadgraph400                2
#define fIDX_LXPLUS_GJetMadgraph40                 3
#define fIDX_LXPLUS_GJetMadgraph600                4
#define fIDX_LXPLUS_GJetMadgraph70                 5
#define fIDX_LXPLUS_PythiaFlat                     6
#define fIDX_LXPLUS_QCD4JetsMadgraph_1000to1200    7
#define fIDX_LXPLUS_QCD4JetsMadgraph_100to200      8
#define fIDX_LXPLUS_QCD4JetsMadgraph_1200to1500    9
#define fIDX_LXPLUS_QCD4JetsMadgraph_1500to2000   10
#define fIDX_LXPLUS_QCD4JetsMadgraph_2000toinf    11
#define fIDX_LXPLUS_QCD4JetsMadgraph_200to400     12
#define fIDX_LXPLUS_QCD4JetsMadgraph_400to600     13
#define fIDX_LXPLUS_QCD4JetsMadgraph_600to800     14
#define fIDX_LXPLUS_QCD4JetsMadgraph_70to100      15
#define fIDX_LXPLUS_QCD4JetsMadgraph_800to1000    16
#define fIDX_LXPLUS_DataE                         17
#define fIDX_LXPLUS_DataF                         18
#define fIDX_LXPLUS_DataG                         19

int main(int argc, char** argv){
    int INIT_EVENT = 0;
    const bool is_problematic_SS_corr_ = true;
    //std::cout << "hiii\n"; // testing
    if ( is_problematic_SS_corr_ ) std::cout << "Disable SS correction on HoverE due to failed validation\n";
    //std::cout << "got file : " << ExternalFilesMgr::RooFile_CTagCalib_DeepCSV("UL2018") << std::endl;
    //std::cout << "hiii enddd\n";

    TChain *tr = new TChain("Events");
    TFile *fout;
    string path;
    string fileName = argv[1];

    double normWgt =1.0;
    //double lumi = 26.81; // 2022EE
    double lumi = 1.0;
    bool isSignal = false;
    bool isData = false;
    bool isQCD = false;
    bool isOther = false;
    bool isEraG = false;
    bool isDataSideband = false;
    bool TEST_MODE = false;


    const std::vector<std::string> lxplus_files({
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph100to200",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph200to400",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph400to600",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph40to70",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph600",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph70to100",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_GJetPythiaFlat",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_1000to1200",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_100to200",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_1200to1500",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_1500to2000",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_2000toinf",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_200to400",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_400to600",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_600to800",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_70to100",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_800to1000",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_Run2022E",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_Run2022F",
            "/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_Run2022G",
    });
    TFile *fpu;
    //Getting the Pileup SF histos
    fpu = new TFile("data/PileupSF_DYJets_EraEFG.root");
    TH1D *h_pu_nom, *h_pu_up, *h_pu_down;
    if(isData==false){
        h_pu_nom = (TH1D*)fpu->Get("pileupSF_nom");
        //h_pu_up = (TH1D*)fpu->Get("pileupSF_up");
        //h_pu_down = (TH1D*)fpu->Get("pileupSF_down");
    }
    //JEC for MC
    if(isData==false){
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_V2_MC_L2L3Residual_AK4PFPuppi");
    }
    //Getting the CDFs for Shower shape corrections
    TFile *fss_barrel = new TFile("data/output_ShowerShapeCorrection_barrel_1000Bins.root");
    TFile *fss_endcap = new TFile("data/output_ShowerShapeCorrection_endcap_1000Bins.root");

    if(fileName=="DataE"){
        tr->Add( outfiles(lxplus_files[fIDX_LXPLUS_DataE]).Data() );
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022E.root"); // chip
        fout = new TFile("outfile_dataE_signalregion.root","RECREATE");
        isData = true;
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
        std::cout << "dataE!!!\n";
    }
    else if(fileName=="DataF"){
        tr->Add( outfiles(lxplus_files[fIDX_LXPLUS_DataF]).Data() );
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022F.root"); // chip
        fout = new TFile("outfile_dataF_signalregion.root","RECREATE");
        isData = true; 
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
    }
    else if(fileName=="DataG"){
        tr->Add( outfiles(lxplus_files[fIDX_LXPLUS_DataG]).Data() );
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022G.root"); // chip
        fout = new TFile("outfile_dataG_signalregion.root","RECREATE");
        isData = true;
        isEraG = true;
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23  = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
    }
    else if(fileName=="DataEsideband"){
        tr->Add( outfiles(lxplus_files[fIDX_LXPLUS_DataE]).Data() );
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022E.root"); // chip
        fout = new TFile("outfile_dataE_sideband.root","RECREATE");
        isData = true;
        isDataSideband = true;
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
    }
    else if(fileName=="DataFsideband"){
        tr->Add( outfiles(lxplus_files[fIDX_LXPLUS_DataF]).Data() );
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022F.root"); // chip
        fout = new TFile("outfile_dataF_sideband.root","RECREATE");
        isData = true; 
        isDataSideband = true;
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");
    }
    else if(fileName=="DataGsideband"){
        tr->Add( outfiles(lxplus_files[fIDX_LXPLUS_DataG]).Data() );
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022G.root"); // chip
        fout = new TFile("outfile_dataG_sideband.root","RECREATE");
        isData = true;
        isDataSideband = true;
        isEraG = true;
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
    }

    //tr->Add("/eos/home-l/ltsai//public/GJetPythia_20_MGG40to80.root");
    //tr->Add("/eos/home-l/ltsai//public/GJetPythia_20to40_MGG80.root");
    //tr->Add("/eos/home-l/ltsai//public/GJetPythia_40_MGG80.root");



    else if(fileName=="GJets40"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_GJetMadgraph40]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_GJetMadgraph40]).Data());

        fout = new TFile("outfile_GmJets_40To70.root","RECREATE");
        normWgt = 1.0*lumi*1000*1.506e+4*1.000000/totGenW;
        //  normWgt = 1.0*lumi*1000*1.506e+4*1.000000/4.0377335e+11;
        //1.506e+04+-1.366e+02

        isSignal = true;
    }
    else if(fileName=="GJets70"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_GJetMadgraph70]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_GJetMadgraph70]).Data());

        fout = new TFile("outfile_GmJets_70To100.root","RECREATE");
        normWgt = 1.0*lumi*1000*8.187e+03*1.000000/totGenW;
        //  normWgt = 1.0*lumi*1000*8.187e+03*1.000000/4.0377335e+11;
        //8.187e+03+-7.411e+01

        isSignal = true;
    }
    else if(fileName=="GJets100"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_GJetMadgraph100]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_GJetMadgraph100]).Data());

        fout = new TFile("outfile_GmJets_100To200.root","RECREATE");
        normWgt = 1.0*lumi*1000*7.351e+03*1.000000/totGenW;
        //  normWgt = 1.0*lumi*1000*7.351e+03*1.000000/4.0377335e+11;
        //7.351e+03+-6.671e+01

        isSignal = true;
    }
    else if(fileName=="GJets200"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_GJetMadgraph200]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_GJetMadgraph200]).Data());

        fout = new TFile("outfile_GmJets_200To400.root","RECREATE");
        normWgt = 1.0*lumi*1000*1548*1.42/totGenW;
        //normWgt = 1.0*lumi*1000*1548*1.42/4.0377335e+11;
        // 1553 +- 14.21
        isSignal = true;
    }
    else if(fileName=="GJets400"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_GJetMadgraph400]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_GJetMadgraph400]).Data());

        fout = new TFile("outfile_GmJets_400To600.root","RECREATE");
        normWgt = 1.0*lumi*1000*166.1*1.56/totGenW;
        //normWgt = 1.0*lumi*1000*166.1*1.56/4.8090040e+10;
        // 169.2+-1.57
        isSignal = true;
    }
    else if(fileName=="GJets600"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_GJetMadgraph600]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_GJetMadgraph600]).Data());

        fout = new TFile("outfile_GmJets_600_inf.root","RECREATE");
        normWgt = 1.0*lumi*1000*53.91*1.56/totGenW;
        //normWgt = 1.0*lumi*1000*53.91*1.56/2.4486741e+10;
        // 53.87+-0.5038
        isSignal = true;
    }
    else if(fileName=="GJetsPythiaFlat"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_PythiaFlat]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_PythiaFlat]).Data());

        fout = new TFile("outfile_GJetPythiaFlat.root","RECREATE");
        normWgt = 1.0*lumi*1000*295000.0/totGenW;
        //normWgt = 1.0*lumi*1000*53.91*1.56/2.4486741e+10;
        // 53.87+-0.5038
        isSignal = true;
    }



    else if(fileName=="QCD70"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_70to100]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_70to100]).Data());

        fout = new TFile("outfile_QCD_70To100.root","RECREATE");
        normWgt = 1.0*lumi*1000*5.910e+07/totGenW;
        // 5.910e+07 +- 5.258e+05
        isQCD = true;
    }
    else if(fileName=="QCD100"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_100to200]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_100to200]).Data());

        fout = new TFile("outfile_QCD_100To200.root","RECREATE");
        normWgt = 1.0*lumi*1000*2.502e+07/totGenW;
        // 2.502e+07 +- 2.238e+05
        isQCD = true;
    }
    else if(fileName=="QCD200"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_200to400]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_200to400]).Data());

        fout = new TFile("outfile_QCD_200To400.root","RECREATE");
        normWgt = 1.0*lumi*1000*1.915e+06/totGenW;
        //normWgt = 1.0*lumi*1000*1.915e+06/6.7668799e+13;
        // 1.915e+06 +- 1.776e+04
        isQCD = true;
    }
    else if(fileName=="QCD400"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_400to600]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_400to600]).Data());

        fout = new TFile("outfile_QCD_400To600.root","RECREATE");
        normWgt = 1.0*lumi*1000*96000/totGenW;
        //normWgt = 1.0*lumi*1000*96000/6.7668799e+13;
        isQCD = true;
    }
    else if(fileName=="QCD600"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_600to800]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_600to800]).Data());

        normWgt = 1.0*lumi*1000*13380/totGenW;
        //normWgt = 1.0*lumi*1000*13380/9.8935244e+12;
        fout = new TFile("outfile_QCD_600To800.root","RECREATE");
        isQCD = true;
    }

    else if(fileName=="QCD800"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_800to1000]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_800to1000]).Data());

        fout = new TFile("outfile_QCD_800To1000.root","RECREATE");
        normWgt = 1.0*lumi*1000*3083/totGenW;
        //normWgt = 1.0*lumi*1000*3083/2.4123477e+12;
        isQCD = true;
    }
    else if(fileName=="QCD1000"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_1000to1200]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_1000to1200]).Data());

        fout = new TFile("outfile_QCD_1000To1200.root","RECREATE");
        normWgt = 1.0*lumi*1000*877.2/totGenW;
        //normWgt = 1.0*lumi*1000*877.2/7.9361433e+11;
        isQCD = true;
    }
    else if(fileName=="QCD1200"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_1200to1500]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_1200to1500]).Data());

        fout = new TFile("outfile_QCD_1200To1500.root","RECREATE");
        normWgt = 1.0*lumi*1000*377.6/totGenW;
        //normWgt = 1.0*lumi*1000*377.6/3.4833910e+11;
        isQCD = true;
    }
    else if(fileName=="QCD1500"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_1500to2000]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_1500to2000]).Data());

        fout = new TFile("outfile_QCD_1500To2000.root","RECREATE");
        normWgt = 1.0*lumi*1000*125.2/totGenW;
        //normWgt = 1.0*lumi*1000*125.2/1.0634461e+11;
        isQCD = true;
    }
    else if(fileName=="QCD2000"){
        tr->Add(outfiles(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_2000toinf]).Data());
        double totGenW = TotalGenWeight(histfile(lxplus_files[fIDX_LXPLUS_QCD4JetsMadgraph_2000toinf]).Data());

        fout = new TFile("outfile_QCD_2000.root","RECREATE");
        normWgt = lumi*1000*26.32/totGenW;
        //normWgt = lumi*1000*26.32/2.2450631e+10;
        isQCD = true;
    }
    else if(fileName=="WtoLNu1Jet"){
        path = "Other_MC/WtoLNu1Jet/";
        tr->Add((path+"outFile_WtoLNu_1Jet.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WtoLNu_1Jet.root","RECREATE");
        normWgt = 1.0*lumi*1000*9084/1.2750897e+12;
        isOther = true;
    }
    else if(fileName=="WtoLNu2Jet"){
        path = "Other_MC/WtoLNu2Jet/";
        tr->Add((path+"outFile_WtoLNu_2Jets.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WtoLNu_2Jet.root","RECREATE");
        normWgt = 1.0*lumi*1000*2925/6.3699918e+11;
        isOther = true;
    }
    else if(fileName=="WtoLNu3Jet"){
        path = "Other_MC/WtoLNu3Jet/";
        tr->Add((path+"outFile_WtoLNu_3Jets.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WtoLNu_3Jet.root","RECREATE");
        normWgt = 1.0*lumi*1000*2925/3.2069025e+11;
        isOther = true;
    }
    else if(fileName=="WtoLNu4Jet"){
        path = "Other_MC/WtoLNu4Jet/";
        tr->Add((path+"outFile_WtoLNu_4Jets.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WtoLNu_4Jet.root","RECREATE");
        normWgt = 1.0*lumi*1000*2925/3.5458119e+10;
        isOther = true;
    }
    else if(fileName=="WGto2QG"){
        path = "Other_MC/WGto2QG_PTG200/";
        tr->Add((path+"outFile_WGto2QG_PTG200.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WGto2QG_PTG200.root","RECREATE");
        normWgt = 1.0*lumi*1000*0.6326/3033535.9;
        isOther = true;
    }
    else if(fileName=="WGtoLNuG200"){
        path = "Other_MC/WGtoLNuG_PTG200to400/";
        tr->Add((path+"outFile_WGtoLNuG_PTG200to400.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WGtoLNuG_PTG200to400.root","RECREATE");
        normWgt = 1.0*lumi*1000*0.2908/1441224.4;
        isOther = true;
    }
    else if(fileName=="WGtoLNuG400"){
        path = "Other_MC/WGtoLNuG_PTG400to600/";
        tr->Add((path+"outFile_WGtoLNuG_PTG400to600.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WGtoLNuG_PTG400to600.root","RECREATE");
        normWgt = 1.0*lumi*1000*0.02231/72278.417;
        isOther = true;
    }
    else if(fileName=="WGtoLNuG600"){
        path = "Other_MC/WGtoLNuG_PTG600/";
        tr->Add((path+"outFile_WGtoLNuG_PTG600.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_WGtoLNuG_PTG600.root","RECREATE");
        normWgt = 1.0*lumi*1000*0.004907/8294.4405;
        isOther = true;
    }
    else if(fileName=="DYJets"){
        path = "Other_MC/DYJets/";
        tr->Add((path+"outFile_DYJets.root").c_str());

        //fpu = new TFile((path_PU+"PileupSF_GmJets200To400.root").c_str());
        fout = new TFile("outfile_DYJets.root","RECREATE");
        normWgt = 1.0*lumi*1000*5558/94589416;
        isOther = true;
    }
    else if(fileName=="GJetsFlatPt"){
        path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJet_PT-15to6000_Flat/";
        tr->Add((path+"outFile_GmJets_DoubleEMEnriched_PT20_MGG40To80_Final4.root").c_str());
        //tr->Add((path+"outFile_GmJets_DoubleEMEnriched_PT20_MGG40To80_Final3.root").c_str());

        fout = new TFile("outFile_GJetsFlatPt_forCorrMatrix.root","RECREATE");
        normWgt = 1.0*lumi*1000*295100.0/27275.228;
        isSignal = true;
    }
    else if(fileName=="GJetsFlatPt_forVal"){
        path = "/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/ForSRStudy/GJets/GJet_PT-15to6000_Flat/";
        tr->Add((path+"outFile_GmJets_DoubleEMEnriched_PT20_MGG40To80_Final3.root").c_str());

        fout = new TFile("outFile_GJetsFlatPt_forSomeCheck.root","RECREATE");
        normWgt = 1.0*lumi*1000*295100.0/27275.228;
        isSignal = true;
    }
    else if (fileName=="test1") {
        tr->Add("/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_G4JetMadgraph200to400/outfile_2022EEGJet_G4JetMadgraph200to400_10418933.48.root");
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/G4JetsMadgraph_200to400.root"); // chip
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/QCD4JetsMadgraph_100to200.root"); // chip

        fout = new TFile("mytesting_gjetmadgraph.root", "RECREATE");
        normWgt = 1.0;
        isSignal = true;
        TEST_MODE = true;

    }
    else if (fileName=="test2") {
        tr->Add("/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_GJet/2022EEGJet_QCDMadgraph_800to1000/outfile_2022EEGJet_QCDMadgraph_800to1000_10418940.0.root");
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/GJetPythia_20_MGG40to80.root"); // chip

        fout = new TFile("mytesting_qcdmadgraph.root", "RECREATE");
        normWgt = 1.0;
        isQCD = true;
        TEST_MODE = true;
    }
    else if (fileName=="test3") {
        tr->Add("/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/Run2022E.root"); // lxplus
        //tr->Add("/data4/ltsai/ReceivedFile/2022EE_NanoAODv12/Run2022E.root"); // chip

        fout = new TFile("mytesting_data.root", "RECREATE");
        isData = true; 
        jec_sf_L2   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi");
        jec_sf_L3   = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi");
        jec_sf_L23 = cset_jet_jerc_file->at("Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");
        //jecjer_corr.LoadKey(
        //    "Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi",
        //    "Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi",
        //    "Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");

        TEST_MODE = true;
    }
    else{
        cout<<"No such sample"<<endl;
        abort();
    }
    if(isData==false && jecjer_corr == nullptr){
        jecjer_corr = new JEC_JER_Corrector( jec_jer_json,
                "Summer22EE_22Sep2023_V2_MC_L2Relative_AK4PFPuppi",
                "Summer22EE_22Sep2023_V2_MC_L3Absolute_AK4PFPuppi",
                "Summer22EE_22Sep2023_V2_MC_L2L3Residual_AK4PFPuppi");
    }

    // const char* inFILEname = "a.root";
    // tr->Add(inFILEname);
    // 
    // const char* oFILEname = "out.root";
    // fout = new TFile(oFILEname, "RECREATE");
    // normWgt = 1.0;
    // isSignal = false;

#define MAX_PHO 100
#define MAX_JET 130
#define MAX_GENPHO 100
#define MAX_SV 100
    // Declaration of leaf types
    UInt_t          run;
    UInt_t          luminosityBlock;
    ULong64_t       event;
    UInt_t          bunchCrossing;
    Float_t         PuppiMET_pt;
    Int_t           nPhoton;
    Char_t          Photon_seediEtaOriX[MAX_PHO];   //[nPhoton]
    UChar_t         Photon_cutBased[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_electronVeto[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_hasConversionTracks[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_isScEtaEB[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_isScEtaEE[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_mvaID_WP80[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_mvaID_WP90[MAX_PHO];   //[nPhoton]
    Bool_t          Photon_pixelSeed[MAX_PHO];   //[nPhoton]
    UChar_t         Photon_seedGain[MAX_PHO];   //[nPhoton]
    Short_t         Photon_electronIdx[MAX_PHO];   //[nPhoton]
    Short_t         Photon_jetIdx[MAX_PHO];   //[nPhoton]
    Int_t           Photon_seediPhiOriY[MAX_PHO];   //[nPhoton]
    Int_t           Photon_vidNestedWPBitmap[MAX_PHO];   //[nPhoton]
    Float_t         Photon_ecalPFClusterIso[MAX_PHO];   //[nPhoton]
    Float_t         Photon_energyErr[MAX_PHO];   //[nPhoton]
    Float_t         Photon_energyRaw[MAX_PHO];   //[nPhoton]
    Float_t         Photon_esEffSigmaRR[MAX_PHO];   //[nPhoton]
    Float_t         Photon_esEnergyOverRawE[MAX_PHO];   //[nPhoton]
    Float_t         Photon_eta[MAX_PHO];   //[nPhoton]
    Float_t         Photon_etaWidth[MAX_PHO];   //[nPhoton]
    Float_t         Photon_haloTaggerMVAVal[MAX_PHO];   //[nPhoton]
    Float_t         Photon_hcalPFClusterIso[MAX_PHO];   //[nPhoton]
    Float_t         Photon_hoe[MAX_PHO];   //[nPhoton]
    Float_t         Photon_hoe_PUcorr[MAX_PHO];   //[nPhoton]
    Float_t         Photon_mvaID[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pfChargedIso[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pfChargedIsoPFPV[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pfChargedIsoWorstVtx[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pfPhoIso03[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pfRelIso03_all_quadratic[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pfRelIso03_chg_quadratic[MAX_PHO];   //[nPhoton]
    Float_t         Photon_phi[MAX_PHO];   //[nPhoton]
    Float_t         Photon_phiWidth[MAX_PHO];   //[nPhoton]
    Float_t         Photon_pt[MAX_PHO];   //[nPhoton]
    Float_t         Photon_r9[MAX_PHO];   //[nPhoton]
    Float_t         Photon_s4[MAX_PHO];   //[nPhoton]
    Float_t         Photon_sieie[MAX_PHO];   //[nPhoton]
    Float_t         Photon_sieip[MAX_PHO];   //[nPhoton]
    Float_t         Photon_sipip[MAX_PHO];   //[nPhoton]
    Float_t         Photon_trkSumPtHollowConeDR03[MAX_PHO];   //[nPhoton]
    Float_t         Photon_trkSumPtSolidConeDR04[MAX_PHO];   //[nPhoton]
    Float_t         Photon_x_calo[MAX_PHO];   //[nPhoton]
    Float_t         Photon_y_calo[MAX_PHO];   //[nPhoton]
    Float_t         Photon_z_calo[MAX_PHO];   //[nPhoton]
    Float_t         Photon_MyMVA[MAX_PHO]; 
    Float_t         Rho_fixedGridRhoFastjetAll;
    Bool_t          HLT_Photon200;
    Int_t           nGenIsolatedPhoton;
    Float_t         GenIsolatedPhoton_eta[MAX_GENPHO];   //[nGenIsolatedPhoton]
    Float_t         GenIsolatedPhoton_mass[MAX_GENPHO];   //[nGenIsolatedPhoton]
    Float_t         GenIsolatedPhoton_phi[MAX_GENPHO];   //[nGenIsolatedPhoton]
    Float_t         GenIsolatedPhoton_pt[MAX_GENPHO];   //[nGenIsolatedPhoton]
    Float_t	    genWeight;
    Int_t 	    Pileup_nPU;
    Int_t           nJet;
    UChar_t         Jet_nSVs[MAX_JET];   //[nJet]
    UChar_t         Jet_jetId[MAX_JET];   //[nJet]
    ROOT::VecOps::RVec<bool> *Jet_PFMuonOverlapped;
    Float_t         Jet_chEmEF[MAX_JET];   //[nJet]
    Float_t         Jet_neEmEF[MAX_JET];
    Float_t         Jet_eta[MAX_JET];   //[nJet]
    Float_t         Jet_mass[MAX_JET];   //[nJet]
    Float_t         Jet_phi[MAX_JET];   //[nJet]
    Float_t         Jet_pt[MAX_JET];   //[nJet]
    Float_t         Jet_rawFactor[MAX_JET];   //[nJet]

    // new part
    Short_t         Jet_genJetIdx[MAX_JET];   //[nJet]
    Float_t         Jet_btagPNetB[MAX_JET];   //[nJet]
    Float_t         Jet_btagPNetCvB[MAX_JET];   //[nJet]
    Float_t         Jet_btagPNetCvL[MAX_JET];   //[nJet]
    Float_t         Jet_btagPNetQvG[MAX_JET];   //[nJet]
    Float_t         Jet_btagRobustParTAK4B[MAX_JET];   //[nJet]
    Float_t         Jet_btagRobustParTAK4CvB[MAX_JET];   //[nJet]
    Float_t         Jet_btagRobustParTAK4CvL[MAX_JET];   //[nJet]
    Float_t         Jet_btagRobustParTAK4QG[MAX_JET];   //[nJet]
    Float_t         Jet_btagDeepFlavB[MAX_JET];   //[nJet]
    Float_t         Jet_btagDeepFlavCvB[MAX_JET];   //[nJet]
    Float_t         Jet_btagDeepFlavCvL[MAX_JET];   //[nJet]
    Float_t         Jet_btagDeepFlavQG[MAX_JET];   //[nJet]
    Short_t         Jet_partonFlavour[MAX_JET];   //[nJet]
    UChar_t         Jet_hadronFlavour[MAX_JET];   //[nJet]
    //
    Int_t           nSV;
    Float_t         SV_dxySig[MAX_SV];   //[nSV]
    Float_t         SV_dlenSig[MAX_SV];   //[nSV]
    UChar_t         SV_ntracks[MAX_SV];   //[nSV]
    Float_t         SV_chi2[MAX_SV];   //[nSV]
    Float_t         SV_eta[MAX_SV];   //[nSV]
    Float_t         SV_mass[MAX_SV];   //[nSV]
    Float_t         SV_ndof[MAX_SV];   //[nSV]
    Float_t         SV_phi[MAX_SV];   //[nSV]
    Float_t         SV_pt[MAX_SV];   //[nSV]
    Float_t         SV_x[MAX_SV];   //[nSV]
    Float_t         SV_y[MAX_SV];   //[nSV]
    Float_t         SV_z[MAX_SV];   //[nSV]
    Short_t         Photon_genPartIdx[MAX_PHO];
#define MAX_GENJET 80
    Short_t         GenJet_partonFlavour[MAX_GENJET];   //[nGenJet]
    UChar_t         GenJet_hadronFlavour[MAX_GENJET];   //[nGenJet]
    Int_t           nGenJet;
    Float_t         GenJet_eta[MAX_GENJET];   //[nGenJet]
    Float_t         GenJet_mass[MAX_GENJET];   //[nGenJet]
    Float_t         GenJet_phi[MAX_GENJET];   //[nGenJet]
    Float_t         GenJet_pt[MAX_GENJET];   //[nGenJet]
    TBranch        *b_Photon_genPartIdx;
    TBranch        *b_Jet_genJetIdx;   //!


    TBranch        *b_run;   //!
    TBranch        *b_luminosityBlock;   //!
    TBranch        *b_event;   //!
    TBranch        *b_PuppiMET_pt;
    TBranch        *b_bunchCrossing;   //!
    TBranch        *b_nPhoton;   //!
    TBranch        *b_Photon_seediEtaOriX;   //!
    TBranch        *b_Photon_cutBased;   //!
    TBranch        *b_Photon_electronVeto;   //!
    TBranch        *b_Photon_hasConversionTracks;   //!
    TBranch        *b_Photon_isScEtaEB;   //!
    TBranch        *b_Photon_isScEtaEE;   //!
    TBranch        *b_Photon_mvaID_WP80;   //!
    TBranch        *b_Photon_mvaID_WP90;   //!
    TBranch        *b_Photon_pixelSeed;   //!
    TBranch        *b_Photon_seedGain;   //!
    TBranch        *b_Photon_electronIdx;   //!
    TBranch        *b_Photon_jetIdx;   //!
    TBranch        *b_Photon_seediPhiOriY;   //!
    TBranch        *b_Photon_vidNestedWPBitmap;   //!
    TBranch        *b_Photon_ecalPFClusterIso;   //!
    TBranch        *b_Photon_energyErr;   //!
    TBranch        *b_Photon_energyRaw;   //!
    TBranch        *b_Photon_esEffSigmaRR;   //!
    TBranch        *b_Photon_esEnergyOverRawE;   //!
    TBranch        *b_Photon_eta;   //!
    TBranch        *b_Photon_etaWidth;   //!
    TBranch        *b_Photon_haloTaggerMVAVal;   //!
    TBranch        *b_Photon_hcalPFClusterIso;   //!
    TBranch        *b_Photon_hoe;   //!
    TBranch        *b_Photon_hoe_PUcorr;   //!
    TBranch        *b_Photon_mvaID;   //!
    TBranch        *b_Photon_pfChargedIso;   //!
    TBranch        *b_Photon_pfChargedIsoPFPV;   //!
    TBranch        *b_Photon_pfChargedIsoWorstVtx;   //!
    TBranch        *b_Photon_pfPhoIso03;   //!
    TBranch        *b_Photon_pfRelIso03_all_quadratic;   //!
    TBranch        *b_Photon_pfRelIso03_chg_quadratic;   //!
    TBranch        *b_Photon_phi;   //!
    TBranch        *b_Photon_phiWidth;   //!
    TBranch        *b_Photon_pt;   //!
    TBranch        *b_Photon_r9;   //!
    TBranch        *b_Photon_s4;   //!
    TBranch        *b_Photon_sieie;   //!
    TBranch        *b_Photon_sieip;   //!
    TBranch        *b_Photon_sipip;   //!
    TBranch        *b_Photon_trkSumPtHollowConeDR03;   //!
    TBranch        *b_Photon_trkSumPtSolidConeDR04;   //!
    TBranch        *b_Photon_x_calo;   //!
    TBranch        *b_Photon_y_calo;   //!
    TBranch        *b_Photon_z_calo;   //!  
    TBranch        *b_Rho_fixedGridRhoFastjetAll; //!
    TBranch        *b_HLT_Photon200;   //!
    TBranch        *b_nGenIsolatedPhoton;   //!
    TBranch        *b_GenIsolatedPhoton_eta;   //!
    TBranch        *b_GenIsolatedPhoton_mass;   //!
    TBranch        *b_GenIsolatedPhoton_phi;   //!
    TBranch        *b_GenIsolatedPhoton_pt;   //!



    TBranch        *b_Jet_nSVs;   //!
    TBranch        *b_Jet_btagPNetB;   //!
    TBranch        *b_Jet_btagPNetCvB;   //!
    TBranch        *b_Jet_btagPNetCvL;   //!
    TBranch        *b_Jet_btagPNetQvG;   //!
    TBranch        *b_Jet_btagRobustParTAK4B;   //!
    TBranch        *b_Jet_btagRobustParTAK4CvB;   //!
    TBranch        *b_Jet_btagRobustParTAK4CvL;   //!
    TBranch        *b_Jet_btagRobustParTAK4QG;   //!
    TBranch        *b_Jet_btagDeepFlavB;   //!
    TBranch        *b_Jet_btagDeepFlavCvB;   //!
    TBranch        *b_Jet_btagDeepFlavCvL;   //!
    TBranch        *b_Jet_btagDeepFlavQG;   //!
    TBranch        *b_Jet_partonFlavour;   //!
    TBranch        *b_Jet_hadronFlavour;   //!
    TBranch        *b_GenJet_partonFlavour;   //!
    TBranch        *b_GenJet_hadronFlavour;   //!
    //
    TBranch        *b_nGenJet;   //!
    TBranch        *b_GenJet_eta;   //!
    TBranch        *b_GenJet_mass;   //!
    TBranch        *b_GenJet_phi;   //!
    TBranch        *b_GenJet_pt;   //!



    TBranch        *b_Photon_MyMVA;   //!
    TBranch        *b_genWeight;  //!
    TBranch	  *b_Pileup_nPU; //!
    TBranch        *b_nJet;   //!
    TBranch        *b_Jet_jetId;   //!
    TBranch        *b_Jet_PFMuonOverlapped;
    TBranch	  *b_Jet_chEmEF;
    TBranch	  *b_Jet_neEmEF;
    TBranch        *b_Jet_mass;   //!
    TBranch        *b_Jet_eta;   //!
    TBranch        *b_Jet_phi;   //!
    TBranch        *b_Jet_pt;   //!

    TBranch        *b_nSV;   //!
    TBranch        *b_SV_dxySig;   //!
    TBranch        *b_SV_dlenSig;   //!
    TBranch        *b_SV_ntracks;   //!
    TBranch        *b_SV_chi2;   //!
    TBranch        *b_SV_eta;   //!
    TBranch        *b_SV_mass;   //!
    TBranch        *b_SV_ndof;   //!
    TBranch        *b_SV_phi;   //!
    TBranch        *b_SV_pt;   //!
    TBranch        *b_SV_x;   //!
    TBranch        *b_SV_y;   //!
    TBranch        *b_SV_z;   //!
    TBranch	  *b_Jet_rawFactor;

    tr->SetBranchAddress("run", &run, &b_run);
    tr->SetBranchAddress("luminosityBlock", &luminosityBlock, &b_luminosityBlock);
    tr->SetBranchAddress("event", &event, &b_event);
    tr->SetBranchAddress("bunchCrossing", &bunchCrossing, &b_bunchCrossing); 
    tr->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt, &b_PuppiMET_pt);
    tr->SetBranchAddress("nPhoton", &nPhoton, &b_nPhoton);
    tr->SetBranchAddress("Photon_seediEtaOriX", Photon_seediEtaOriX, &b_Photon_seediEtaOriX);
    tr->SetBranchAddress("Photon_cutBased", Photon_cutBased, &b_Photon_cutBased);
    //tr->SetBranchAddress("Photon_electronVeto", Photon_electronVeto, &b_Photon_electronVeto);
    //tr->SetBranchAddress("Photon_hasConversionTracks", Photon_hasConversionTracks, &b_Photon_hasConversionTracks);
    tr->SetBranchAddress("Photon_isScEtaEB", Photon_isScEtaEB, &b_Photon_isScEtaEB);
    tr->SetBranchAddress("Photon_isScEtaEE", Photon_isScEtaEE, &b_Photon_isScEtaEE);
    tr->SetBranchAddress("Photon_mvaID_WP80", Photon_mvaID_WP80, &b_Photon_mvaID_WP80);
    tr->SetBranchAddress("Photon_mvaID_WP90", Photon_mvaID_WP90, &b_Photon_mvaID_WP90);
    tr->SetBranchAddress("Photon_pixelSeed", Photon_pixelSeed, &b_Photon_pixelSeed);
    tr->SetBranchAddress("Photon_seedGain", Photon_seedGain, &b_Photon_seedGain);
    tr->SetBranchAddress("Photon_electronIdx", Photon_electronIdx, &b_Photon_electronIdx);
    //tr->SetBranchAddress("Photon_jetIdx", Photon_jetIdx, &b_Photon_jetIdx);
    tr->SetBranchAddress("Photon_seediPhiOriY", Photon_seediPhiOriY, &b_Photon_seediPhiOriY);
    tr->SetBranchAddress("Photon_vidNestedWPBitmap", Photon_vidNestedWPBitmap, &b_Photon_vidNestedWPBitmap);
    //tr->SetBranchAddress("Photon_ecalPFClusterIso", Photon_ecalPFClusterIso, &b_Photon_ecalPFClusterIso);
    tr->SetBranchAddress("Photon_energyErr", Photon_energyErr, &b_Photon_energyErr);
    tr->SetBranchAddress("Photon_energyRaw", Photon_energyRaw, &b_Photon_energyRaw);
    tr->SetBranchAddress("Photon_esEffSigmaRR", Photon_esEffSigmaRR, &b_Photon_esEffSigmaRR);
    tr->SetBranchAddress("Photon_esEnergyOverRawE", Photon_esEnergyOverRawE, &b_Photon_esEnergyOverRawE);
    tr->SetBranchAddress("Photon_eta", Photon_eta, &b_Photon_eta);
    tr->SetBranchAddress("Photon_etaWidth", Photon_etaWidth, &b_Photon_etaWidth);
    tr->SetBranchAddress("Photon_haloTaggerMVAVal", Photon_haloTaggerMVAVal, &b_Photon_haloTaggerMVAVal);
    //tr->SetBranchAddress("Photon_hcalPFClusterIso", Photon_hcalPFClusterIso, &b_Photon_hcalPFClusterIso);
    tr->SetBranchAddress("Photon_hoe", Photon_hoe, &b_Photon_hoe);
    tr->SetBranchAddress("Photon_hoe_PUcorr", Photon_hoe_PUcorr, &b_Photon_hoe_PUcorr);
    tr->SetBranchAddress("Photon_mvaID", Photon_mvaID, &b_Photon_mvaID);
    tr->SetBranchAddress("Photon_pfChargedIso", Photon_pfChargedIso, &b_Photon_pfChargedIso);
    tr->SetBranchAddress("Photon_pfChargedIsoPFPV", Photon_pfChargedIsoPFPV, &b_Photon_pfChargedIsoPFPV);
    tr->SetBranchAddress("Photon_pfChargedIsoWorstVtx", Photon_pfChargedIsoWorstVtx, &b_Photon_pfChargedIsoWorstVtx);
    tr->SetBranchAddress("Photon_pfPhoIso03", Photon_pfPhoIso03, &b_Photon_pfPhoIso03);
    tr->SetBranchAddress("Photon_pfRelIso03_all_quadratic", Photon_pfRelIso03_all_quadratic, &b_Photon_pfRelIso03_all_quadratic);
    tr->SetBranchAddress("Photon_pfRelIso03_chg_quadratic", Photon_pfRelIso03_chg_quadratic, &b_Photon_pfRelIso03_chg_quadratic);
    tr->SetBranchAddress("Photon_phi", Photon_phi, &b_Photon_phi);
    tr->SetBranchAddress("Photon_phiWidth", Photon_phiWidth, &b_Photon_phiWidth);
    tr->SetBranchAddress("Photon_pt", Photon_pt, &b_Photon_pt);
    tr->SetBranchAddress("Photon_r9", Photon_r9, &b_Photon_r9);
    tr->SetBranchAddress("Photon_s4", Photon_s4, &b_Photon_s4);
    tr->SetBranchAddress("Photon_sieie", Photon_sieie, &b_Photon_sieie);
    tr->SetBranchAddress("Photon_sieip", Photon_sieip, &b_Photon_sieip);
    tr->SetBranchAddress("Photon_sipip", Photon_sipip, &b_Photon_sipip);
    tr->SetBranchAddress("Photon_trkSumPtHollowConeDR03", Photon_trkSumPtHollowConeDR03, &b_Photon_trkSumPtHollowConeDR03);
    tr->SetBranchAddress("Photon_trkSumPtSolidConeDR04", Photon_trkSumPtSolidConeDR04, &b_Photon_trkSumPtSolidConeDR04);
    tr->SetBranchAddress("Photon_x_calo", Photon_x_calo, &b_Photon_x_calo);
    tr->SetBranchAddress("Photon_y_calo", Photon_y_calo, &b_Photon_y_calo);
    tr->SetBranchAddress("Photon_z_calo", Photon_z_calo, &b_Photon_z_calo);
    tr->SetBranchAddress("Rho_fixedGridRhoFastjetAll", &Rho_fixedGridRhoFastjetAll, &b_Rho_fixedGridRhoFastjetAll);
    tr->SetBranchAddress("nJet", &nJet, &b_nJet);
    tr->SetBranchAddress("Jet_jetId", Jet_jetId, &b_Jet_jetId);
    Jet_PFMuonOverlapped = 0;
    tr->SetBranchAddress("Jet_PFMuonOverlapped", &Jet_PFMuonOverlapped, &b_Jet_PFMuonOverlapped);
    tr->SetBranchAddress("Jet_neEmEF", Jet_neEmEF, &b_Jet_neEmEF);
    tr->SetBranchAddress("Jet_chEmEF", Jet_chEmEF, &b_Jet_chEmEF);
    tr->SetBranchAddress("Jet_mass", Jet_mass, &b_Jet_mass);
    tr->SetBranchAddress("Jet_eta", Jet_eta, &b_Jet_eta);
    tr->SetBranchAddress("Jet_phi", Jet_phi, &b_Jet_phi);
    tr->SetBranchAddress("Jet_pt", Jet_pt, &b_Jet_pt);
    tr->SetBranchAddress("Jet_rawFactor", Jet_rawFactor, &b_Jet_rawFactor);
    tr->SetBranchAddress("HLT_Photon200", &HLT_Photon200, &b_HLT_Photon200);
    if(isData==false){
        tr->SetBranchAddress("nGenIsolatedPhoton", &nGenIsolatedPhoton, &b_nGenIsolatedPhoton);
        tr->SetBranchAddress("GenIsolatedPhoton_eta", GenIsolatedPhoton_eta, &b_GenIsolatedPhoton_eta);
        tr->SetBranchAddress("GenIsolatedPhoton_mass", GenIsolatedPhoton_mass, &b_GenIsolatedPhoton_mass);
        tr->SetBranchAddress("GenIsolatedPhoton_phi", GenIsolatedPhoton_phi, &b_GenIsolatedPhoton_phi);
        tr->SetBranchAddress("GenIsolatedPhoton_pt", GenIsolatedPhoton_pt, &b_GenIsolatedPhoton_pt);
        tr->SetBranchAddress("genWeight", &genWeight, &b_genWeight);
        tr->SetBranchAddress("Pileup_nPU", &Pileup_nPU, &b_Pileup_nPU);
        tr->SetBranchAddress("Photon_genPartIdx", &Photon_genPartIdx, &b_Photon_genPartIdx);
        //tr->SetBranchAddress("Photon_MyMVA", Photon_MyMVA, &b_Photon_MyMVA);

        tr->SetBranchAddress("Jet_genJetIdx", Jet_genJetIdx, &b_Jet_genJetIdx);
        tr->SetBranchAddress("Jet_partonFlavour", Jet_partonFlavour, &b_Jet_partonFlavour);
        tr->SetBranchAddress("Jet_hadronFlavour", Jet_hadronFlavour, &b_Jet_hadronFlavour);
        tr->SetBranchAddress("GenJet_partonFlavour", GenJet_partonFlavour, &b_GenJet_partonFlavour);
        tr->SetBranchAddress("GenJet_hadronFlavour", GenJet_hadronFlavour, &b_GenJet_hadronFlavour);
        tr->SetBranchAddress("nGenJet", &nGenJet, &b_nGenJet);
        tr->SetBranchAddress("GenJet_eta", GenJet_eta, &b_GenJet_eta);
        tr->SetBranchAddress("GenJet_mass", GenJet_mass, &b_GenJet_mass);
        tr->SetBranchAddress("GenJet_phi", GenJet_phi, &b_GenJet_phi);
        tr->SetBranchAddress("GenJet_pt", GenJet_pt, &b_GenJet_pt);
    }
    tr->SetBranchAddress("Jet_nSVs", Jet_nSVs, &b_Jet_nSVs);
    tr->SetBranchAddress("Jet_btagPNetB", Jet_btagPNetB, &b_Jet_btagPNetB);
    tr->SetBranchAddress("Jet_btagPNetCvB", Jet_btagPNetCvB, &b_Jet_btagPNetCvB);
    tr->SetBranchAddress("Jet_btagPNetCvL", Jet_btagPNetCvL, &b_Jet_btagPNetCvL);
    tr->SetBranchAddress("Jet_btagPNetQvG", Jet_btagPNetQvG, &b_Jet_btagPNetQvG);
    tr->SetBranchAddress("Jet_btagRobustParTAK4B", Jet_btagRobustParTAK4B, &b_Jet_btagRobustParTAK4B);
    tr->SetBranchAddress("Jet_btagRobustParTAK4CvB", Jet_btagRobustParTAK4CvB, &b_Jet_btagRobustParTAK4CvB);
    tr->SetBranchAddress("Jet_btagRobustParTAK4CvL", Jet_btagRobustParTAK4CvL, &b_Jet_btagRobustParTAK4CvL);
    tr->SetBranchAddress("Jet_btagRobustParTAK4QG", Jet_btagRobustParTAK4QG, &b_Jet_btagRobustParTAK4QG);
    tr->SetBranchAddress("Jet_btagDeepFlavB", Jet_btagDeepFlavB, &b_Jet_btagDeepFlavB);
    tr->SetBranchAddress("Jet_btagDeepFlavCvB", Jet_btagDeepFlavCvB, &b_Jet_btagDeepFlavCvB);
    tr->SetBranchAddress("Jet_btagDeepFlavCvL", Jet_btagDeepFlavCvL, &b_Jet_btagDeepFlavCvL);
    tr->SetBranchAddress("Jet_btagDeepFlavQG", Jet_btagDeepFlavQG, &b_Jet_btagDeepFlavQG);

    tr->SetBranchAddress("nSV", &nSV, &b_nSV);
    tr->SetBranchAddress("SV_dxySig", SV_dxySig, &b_SV_dxySig);
    tr->SetBranchAddress("SV_dlenSig", SV_dlenSig, &b_SV_dlenSig);
    tr->SetBranchAddress("SV_ntracks", SV_ntracks, &b_SV_ntracks);
    tr->SetBranchAddress("SV_chi2", SV_chi2, &b_SV_chi2);
    tr->SetBranchAddress("SV_eta", SV_eta, &b_SV_eta);
    tr->SetBranchAddress("SV_mass", SV_mass, &b_SV_mass);
    tr->SetBranchAddress("SV_ndof", SV_ndof, &b_SV_ndof);
    tr->SetBranchAddress("SV_phi", SV_phi, &b_SV_phi);
    tr->SetBranchAddress("SV_pt", SV_pt, &b_SV_pt);
    tr->SetBranchAddress("SV_x", SV_x, &b_SV_x);
    tr->SetBranchAddress("SV_y", SV_y, &b_SV_y);
    tr->SetBranchAddress("SV_z", SV_z, &b_SV_z);


    //Getting the CDFs for Shower shape corrections
    TGraphErrors *grMC_b[10], *grDataInv_b[10];
    TGraphErrors *grMC_e[10], *grDataInv_e[10];

    grMC_b[0] = (TGraphErrors*)fss_barrel->Get("mc_hoe");
    grMC_b[1] = (TGraphErrors*)fss_barrel->Get("mc_sieie");
    grDataInv_b[0] = (TGraphErrors*)fss_barrel->Get("dataInv_hoe");
    grDataInv_b[1] = (TGraphErrors*)fss_barrel->Get("dataInv_sieie");

    grMC_e[0] = (TGraphErrors*)fss_endcap->Get("mc_esEffSigmaRR");
    grMC_e[1] = (TGraphErrors*)fss_endcap->Get("mc_energyRaw");
    grMC_e[2] = (TGraphErrors*)fss_endcap->Get("mc_esEnergyOverRawE");
    grMC_e[3] = (TGraphErrors*)fss_endcap->Get("mc_etaWidth");
    grMC_e[4] = (TGraphErrors*)fss_endcap->Get("mc_hoe");
    grMC_e[5] = (TGraphErrors*)fss_endcap->Get("mc_phiWidth");
    grMC_e[6] = (TGraphErrors*)fss_endcap->Get("mc_r9");
    grMC_e[7] = (TGraphErrors*)fss_endcap->Get("mc_s4");
    grMC_e[8] = (TGraphErrors*)fss_endcap->Get("mc_sieie");
    grMC_e[9] = (TGraphErrors*)fss_endcap->Get("mc_sieip");

    grDataInv_e[0] = (TGraphErrors*)fss_endcap->Get("dataInv_esEffSigmaRR");
    grDataInv_e[1] = (TGraphErrors*)fss_endcap->Get("dataInv_energyRaw");
    grDataInv_e[2] = (TGraphErrors*)fss_endcap->Get("dataInv_esEnergyOverRawE");
    grDataInv_e[3] = (TGraphErrors*)fss_endcap->Get("dataInv_etaWidth");
    grDataInv_e[4] = (TGraphErrors*)fss_endcap->Get("dataInv_hoe");
    grDataInv_e[5] = (TGraphErrors*)fss_endcap->Get("dataInv_phiWidth");
    grDataInv_e[6] = (TGraphErrors*)fss_endcap->Get("dataInv_r9");
    grDataInv_e[7] = (TGraphErrors*)fss_endcap->Get("dataInv_s4");
    grDataInv_e[8] = (TGraphErrors*)fss_endcap->Get("dataInv_sieie");
    grDataInv_e[9] = (TGraphErrors*)fss_endcap->Get("dataInv_sieip");


    //TBranch *b_Photon_MyMVA = tr->Branch("Photon_MyMVA",Photon_MyMVA, "Photon_MyMVA[nPhoton]/F");
    //TBranch *b_passingMVAwp80 = tr->Branch("passingMVAwp80",&passingMVAwp80, "passingMVAwp80/I");
    TH1D *b_PhoPt            = new TH1D( "bALL_Pho_pt","Pho_pt", 75,210,1710);
    TH1D *b_PNetB            = new TH1D( "bALL_PNetB"          ,"PNetB"           , 100, 0.,1.);
    TH1D *b_PNetCvsB         = new TH1D( "bALL_PNetCvsB"       ,"PNetCvsB"        , 100, 0.,1.);
    TH1D *b_PNetCvsL         = new TH1D( "bALL_PNetCvsL"       ,"PNetCvsL"        , 100, 0.,1.);
    TH1D *b_PNetQvsG         = new TH1D( "bALL_PNetQvsG"       ,"PNetQvsG"        , 100, 0.,1.);
    TH1D *b_ParTB            = new TH1D( "bALL_ParTB"          ,"ParTB"           , 100, 0.,1.);
    TH1D *b_ParTCvsB         = new TH1D( "bALL_ParTCvsB"       ,"ParTCvsB"        , 100, 0.,1.);
    TH1D *b_ParTCvsL         = new TH1D( "bALL_ParTCvsL"       ,"ParTCvsL"        , 100, 0.,1.);
    TH1D *b_ParTQvsG         = new TH1D( "bALL_ParTQvsG"       ,"ParTQvsG"        , 100, 0.,1.);
    TH1D *b_DeepFlavourB     = new TH1D( "bALL_DeepFlavourB"   ,"DeepFlavourB"    , 100, 0.,1.);
    TH1D *b_DeepFlavourCvsB  = new TH1D( "bALL_DeepFlavourCvsB","DeepFlavourCvsB" , 100, 0.,1.);
    TH1D *b_DeepFlavourCvsL  = new TH1D( "bALL_DeepFlavourCvsL","DeepFlavourCvsL" , 100, 0.,1.);
    TH1D *b_DeepFlavourQvsG  = new TH1D( "bALL_DeepFlavourQvsG","DeepFlavourQvsG" , 100, 0.,1.);
    TH1D *b_PhoEta           = new TH1D( "bALL_PhoEta","", 100, -4., 4.);
    TH1D *b_PhoPhi           = new TH1D( "bALL_PhoPhi","", 100, -4., 4.);
    TH1D *b_mva              = new TH1D( "b_MyMVA","MyMVA",100, -1,1);
    TH1D *b_HoverE           = new TH1D( "b_HoverE","", 100, 0., 0.05);
    TH1D *b_sieie            = new TH1D( "b_sieie","", 100, 0., 0.05);
    TH1D *b_sieip            = new TH1D( "b_sieip","", 100, -0.001, 0.001);
    TH1D *b_pfChIso          = new TH1D( "b_pfChIso","", 100, 0., 20.);
    TH1D *b_pfChIsoWorstVtx  = new TH1D( "b_pfChIsoWorstVtx","", 100, 0., 20.);
    TH1D *b_r9               = new TH1D( "b_r9","", 100, 0., 5.);
    TH1D *b_s4               = new TH1D( "b_s4","", 100, 0., 2.);
    TH1D *b_phiWidth         = new TH1D( "b_phiWidth","", 100, 0., 0.4);
    TH1D *b_etaWidth         = new TH1D( "b_etaWidth","", 100, 0., 0.15);
    TH1D *b_esEnergyOverRawE = new TH1D( "b_esEnergyOverRawE","", 100, 0., 1.);
    TH1D *b_energyRaw        = new TH1D( "b_energyRaw","", 100, 0., 6000.);
    TH1D *b_esEffSigmaRR     = new TH1D( "b_esEffSigmaRR","", 100, 0., 15.);

    // only used in signal MC, records SS variable without corrections
    TH1D* borig_mva             = new TH1D( "borig_MyMVA","", 100, -1., 1.);
    TH1D* borig_HoverE          = new TH1D( "borig_HoverE","", 100, 0., 0.05);
    TH1D* borig_sieie           = new TH1D( "borig_sieie","", 100, 0., 0.05);
    TH1D* borig_sieip           = new TH1D( "borig_sieip","", 100, -0.001, 0.001);

    TH1D* borig_r9              = new TH1D( "borig_r9","", 100, 0., 5.);
    TH1D* borig_s4              = new TH1D( "borig_s4","", 100, 0., 2.);
    TH1D* borig_phiWidth        = new TH1D( "borig_phiWidth","", 100, 0., 0.4);
    TH1D* borig_etaWidth        = new TH1D( "borig_etaWidth","", 100, 0., 0.15);
    TH1D* borig_esEnergyOverRawE= new TH1D( "borig_esEnergyOverRawE","", 100, 0., 1.);
    TH1D* borig_energyRaw       = new TH1D( "borig_energyRaw","", 100, 0., 6000.);
    TH1D* borig_esEffSigmaRR    = new TH1D( "borig_esEffSigmaRR","", 100, 0., 15.);

    TH1D *e_PhoPt            = new TH1D( "eALL_Pho_pt","Pho_pt", 75,210,1710);
    TH1D *e_PNetB            = new TH1D( "eALL_PNetB"          ,"PNetB"           , 100, 0.,1.);
    TH1D *e_PNetCvsB         = new TH1D( "eALL_PNetCvsB"       ,"PNetCvsB"        , 100, 0.,1.);
    TH1D *e_PNetCvsL         = new TH1D( "eALL_PNetCvsL"       ,"PNetCvsL"        , 100, 0.,1.);
    TH1D *e_PNetQvsG         = new TH1D( "eALL_PNetQvsG"       ,"PNetQvsG"        , 100, 0.,1.);
    TH1D *e_ParTB            = new TH1D( "eALL_ParTB"          ,"ParTB"           , 100, 0.,1.);
    TH1D *e_ParTCvsB         = new TH1D( "eALL_ParTCvsB"       ,"ParTCvsB"        , 100, 0.,1.);
    TH1D *e_ParTCvsL         = new TH1D( "eALL_ParTCvsL"       ,"ParTCvsL"        , 100, 0.,1.);
    TH1D *e_ParTQvsG         = new TH1D( "eALL_ParTQvsG"       ,"ParTQvsG"        , 100, 0.,1.);
    TH1D *e_DeepFlavourB     = new TH1D( "eALL_DeepFlavourB"   ,"DeepFlavourB"    , 100, 0.,1.);
    TH1D *e_DeepFlavourCvsB  = new TH1D( "eALL_DeepFlavourCvsB","DeepFlavourCvsB" , 100, 0.,1.);
    TH1D *e_DeepFlavourCvsL  = new TH1D( "eALL_DeepFlavourCvsL","DeepFlavourCvsL" , 100, 0.,1.);
    TH1D *e_DeepFlavourQvsG  = new TH1D( "eALL_DeepFlavourQvsG","DeepFlavourQvsG" , 100, 0.,1.);
    TH1D *e_PhoEta           = new TH1D( "eALL_PhoEta","", 100, -4., 4.);
    TH1D *e_PhoPhi           = new TH1D( "eALL_PhoPhi","", 100, -4., 4.);

    TH1D *e_mva              = new TH1D( "e_MyMVA","MyMVA",100, -1,1);
    TH1D *e_HoverE           = new TH1D( "e_HoverE","", 100, 0., 0.05);
    TH1D *e_sieie            = new TH1D( "e_sieie","", 100, 0., 0.05);
    TH1D *e_sieip            = new TH1D( "e_sieip","", 100, -0.001, 0.001);
    TH1D *e_pfChIso          = new TH1D( "e_pfChIso","", 100, 0., 20.);
    TH1D *e_pfChIsoWorstVtx  = new TH1D( "e_pfChIsoWorstVtx","", 100, 0., 20.);
    TH1D *e_r9               = new TH1D( "e_r9","", 100, 0., 5.);
    TH1D *e_s4               = new TH1D( "e_s4","", 100, 0., 2.);
    TH1D *e_phiWidth         = new TH1D( "e_phiWidth","", 100, 0., 0.4);
    TH1D *e_etaWidth         = new TH1D( "e_etaWidth","", 100, 0., 0.3);
    TH1D *e_esEnergyOverRawE = new TH1D( "e_esEnergyOverRawE","", 100, 0., 1.);
    TH1D *e_energyRaw        = new TH1D( "e_energyRaw","", 100, 0., 6000.);
    TH1D *e_esEffSigmaRR     = new TH1D( "e_esEffSigmaRR","", 100, 0., 15.);

    TH1D* eorig_mva             = new TH1D( "eorig_MyMVA","", 100, -1., 1.);
    TH1D* eorig_HoverE          = new TH1D( "eorig_HoverE","", 100, 0., 0.05);
    TH1D* eorig_sieie           = new TH1D( "eorig_sieie","", 100, 0., 0.05);
    TH1D* eorig_sieip           = new TH1D( "eorig_sieip","", 100, -0.001, 0.001);

    TH1D* eorig_r9              = new TH1D( "eorig_r9","", 100, 0., 5.);
    TH1D* eorig_s4              = new TH1D( "eorig_s4","", 100, 0., 2.);
    TH1D* eorig_phiWidth        = new TH1D( "eorig_phiWidth","", 100, 0., 0.4);
    TH1D* eorig_etaWidth        = new TH1D( "eorig_etaWidth","", 100, 0., 0.3);
    TH1D* eorig_esEnergyOverRawE= new TH1D( "eorig_esEnergyOverRawE","", 100, 0., 1.);
    TH1D* eorig_energyRaw       = new TH1D( "eorig_energyRaw","", 100, 0., 6000.);
    TH1D* eorig_esEffSigmaRR    = new TH1D( "eorig_esEffSigmaRR","", 100, 0., 15.);

    double photonPt, photonEta, photonPhi, photonMVA, wgt;
    double o_wgt_WPbL_central;
    bool passWPbL;
    bool passWPbM;
    bool passWPbT;
    double o_wgt_WPcShape_central;

    double jetPt, jetEta, jetPhi;
    int jet_nSV; int njet;
    double jet_SVmass;
    double jet_SVpt;
    double jet_SVdr;
    int jet_SVntracks;
    double photonPfChargedIsoWorstVtx, photonPfChargedIsoPFPV, photonSieie, photonHoE;
    double genPhotonPt, genPhotonEta, genPhotonPhi;
    double photonMVAorig;
    bool isHadFlvr_C, isHadFlvr_B, isHadFlvr_L;
    int jetHadFlvr, jetPrtFlvr, genjetHadFlvr, genjetPrtFlvr;
    double PNetB, PNetCvsB , PNetCvsL , PNetQvsG;
    double ParTB, ParTCvsB , ParTCvsL , ParTQvsG;
    double DeepFlavourB , DeepFlavourCvsB, DeepFlavourCvsL, DeepFlavourQvsG;

    double gjetZmass; // four momentum sum from gamma+jet. Following Z->di-jet but one jet faked into photon.
    double MET;
    int selected_jet_idx;


    TTree *tree = new TTree("tree","tree");
    tree->Branch("photon_pt", &photonPt);
    tree->Branch("photon_eta", &photonEta);
    tree->Branch("photon_phi", &photonPhi);
    tree->Branch("photon_mva", &photonMVA);
    tree->Branch("photon_sieie", &photonSieie);
    tree->Branch("photon_hoe", &photonHoE);
    tree->Branch("photon_pfChargedIsoWorstVtx", &photonPfChargedIsoWorstVtx);
    tree->Branch("photon_pfChargedIsoPFPV", &photonPfChargedIsoPFPV);
    tree->Branch("jet_pt", &jetPt);
    tree->Branch("jet_eta", &jetEta);
    tree->Branch("jet_phi", &jetPhi);
    tree->Branch("jet_multiplicity", &njet);
    tree->Branch("jet_nSV", &jet_nSV);
    tree->Branch("jet_SVmass", &jet_SVmass);
    tree->Branch("jet_SVpt", &jet_SVpt);
    tree->Branch("jet_SVdr", &jet_SVdr);
    tree->Branch("jet_SVntracks", &jet_SVntracks);

    tree->Branch("gjetZmass", &gjetZmass);
    tree->Branch("selected_jet_idx", &selected_jet_idx);
    tree->Branch("MET", &MET);
    if (!isData )
    {
        tree->Branch("GenPhoton_pt",&genPhotonPt);
        tree->Branch("GenPhoton_eta",&genPhotonEta);
        tree->Branch("GenPhoton_phi",&genPhotonPhi);
        tree->Branch("wgt", &wgt);
        tree->Branch("renormREQUIRED_wgt_WPbL_central", &o_wgt_WPbL_central);
        tree->Branch("passWPbL", &passWPbL);
        tree->Branch("passWPbM", &passWPbM);
        tree->Branch("passWPbT", &passWPbT);
        tree->Branch("renormREQUIRED_wgt_WPcShape_central", &o_wgt_WPcShape_central);
        if ( isSignal)
            tree->Branch("photon_mva_orig", &photonMVAorig);

        tree->Branch("isHadFlvr_C", &isHadFlvr_C);
        tree->Branch("isHadFlvr_B", &isHadFlvr_B);
        tree->Branch("isHadFlvr_L", &isHadFlvr_L);

        tree->Branch("jetHadFlvr", &jetHadFlvr);
        tree->Branch("jetPrtFlvr", &jetPrtFlvr);
        tree->Branch("genjetHadFlvr", &genjetHadFlvr);
        tree->Branch("genjetPrtFlvr", &genjetPrtFlvr);
    }

    tree->Branch("PNetB"           , &PNetB             );
    tree->Branch("PNetCvsB"        , &PNetCvsB          );
    tree->Branch("PNetCvsL"        , &PNetCvsL          );
    tree->Branch("PNetQvsG"        , &PNetQvsG          );
    tree->Branch("ParTB"           , &ParTB             );
    tree->Branch("ParTCvsB"        , &ParTCvsB          );
    tree->Branch("ParTCvsL"        , &ParTCvsL          );
    tree->Branch("ParTQvsG"        , &ParTQvsG          );
    tree->Branch("DeepFlavourB"    , &DeepFlavourB      );
    tree->Branch("DeepFlavourCvsB" , &DeepFlavourCvsB   );
    tree->Branch("DeepFlavourCvsL" , &DeepFlavourCvsL   );
    tree->Branch("DeepFlavourQvsG" , &DeepFlavourQvsG   );


    //Retrieving the BDT score
    TMVA::Reader *reader_barrel = new TMVA::Reader();
    TMVA::Reader *reader_endcap = new TMVA::Reader();
    Float_t photon_esEffSigmaRR;
    Float_t photon_energyRaw;
    Float_t photon_esEnergyOverRawE;
    Float_t photon_etaWidth;
    Float_t photon_hoe;
    Float_t photon_phiWidth;
    Float_t photon_r9;
    Float_t photon_s4;
    Float_t photon_sieie;
    Float_t photon_sieip;
    Float_t photon_rho;
    Float_t photon_eta;
    reader_barrel->AddVariable("photon_esEffSigmaRR", &photon_esEffSigmaRR);
    reader_barrel->AddVariable("photon_energyRaw", &photon_energyRaw);
    reader_barrel->AddVariable("photon_esEnergyOverRawE", &photon_esEnergyOverRawE);
    reader_barrel->AddVariable("photon_etaWidth", &photon_etaWidth);
    reader_barrel->AddVariable("photon_hoe", &photon_hoe);
    reader_barrel->AddVariable("photon_phiWidth", &photon_phiWidth);
    reader_barrel->AddVariable("photon_r9", &photon_r9);
    reader_barrel->AddVariable("photon_s4", &photon_s4);
    reader_barrel->AddVariable("photon_sieie", &photon_sieie);
    reader_barrel->AddVariable("photon_sieip", &photon_sieip);
    reader_barrel->AddVariable("photon_rho", &photon_rho);
    reader_barrel->AddSpectator("photon_eta", &photon_eta);

    reader_endcap->AddVariable("photon_esEffSigmaRR", &photon_esEffSigmaRR);
    reader_endcap->AddVariable("photon_energyRaw", &photon_energyRaw);
    reader_endcap->AddVariable("photon_esEnergyOverRawE", &photon_esEnergyOverRawE);
    reader_endcap->AddVariable("photon_etaWidth", &photon_etaWidth);
    reader_endcap->AddVariable("photon_hoe", &photon_hoe);
    reader_endcap->AddVariable("photon_phiWidth", &photon_phiWidth);
    reader_endcap->AddVariable("photon_r9", &photon_r9);
    reader_endcap->AddVariable("photon_s4", &photon_s4);
    reader_endcap->AddVariable("photon_sieie", &photon_sieie);
    reader_endcap->AddVariable("photon_sieip", &photon_sieip);
    reader_endcap->AddVariable("photon_rho", &photon_rho);
    reader_endcap->AddSpectator("photon_eta", &photon_eta);

    // book the MVA of your choice (prior training of these methods, ie,
    // existence of the weight files is required)
    reader_barrel->BookMVA( "BDT",  "data/TMVAClassification_BDTG.weights_Barrel_original.xml");
    reader_endcap->BookMVA( "BDT",  "data/TMVAClassification_BDTG.weights_Endcap_original.xml");

    //Booking Histograms for Pt and Correlation matrix
    const int NBINSX = 10, NBINSY = 2;
    const int NBINSX_gen = 10, NBINSY_gen = 2;
    float binsX[NBINSX+1] = {210,230,250,300,400,500,600,800,1000,1500,2000};
    float binsY[NBINSY+1] = {0.,1.5,2.5};
    float binsX_gen[NBINSX_gen+1] = {150,210,230,250,300,400,500,600,800,1000,1500};
    float binsY_gen[NBINSY_gen+1] = {0.,1.5,2.5};
    const int NBINSX_corr = 10;
    const int NBINSY_corr = 9;
    float binsX_corr[NBINSX_corr+1] = {210,230,250,300,400,500,600,800,1000,1500,2000};
    float binsY_corr[NBINSY_corr+1] = {210,230,250,300,400,500,600,800,1000,1500};
    TH1D *h_reco_pt[40];
    TH1D *h_gen_pt[40];
    TH2D *h_corrMatrix[4];
    TH1D *h_pt_reco[4];
    TH1D *h_pt_gen[4];
    for(int i=0; i<40; ++i){
        h_reco_pt[i] = new TH1D(Form("recoPt%i",i), Form("recoPt%i",i), NBINSX, binsX);
        h_gen_pt[i] = new TH1D(Form("genPt%i",i), Form("genPt%i",i), NBINSX_gen, binsX_gen);
        //h_corrMatrix[i] = new TH2D(Form("corrMatrix%i",i), Form("corrMatrix%i",i), NBINSX,binsX,NBINSX_gen, binsX_gen);
    }
    for(int i=0; i<4; ++i){
        h_pt_reco[i] = new TH1D(Form("reco_pt%i",i), Form("reco_pt%i",i), NBINSX, binsX);
        h_pt_gen[i] = new TH1D(Form("gen_pt%i",i), Form("gen_pt%i",i), NBINSX_gen, binsX_gen);
        h_corrMatrix[i] = new TH2D(Form("corrMatrix%i",i), Form("corrMatrix%i",i), NBINSX_corr,binsX_corr,NBINSY_corr, binsY_corr);
    }


    //std::cout<<"start looping\n";
    auto nEntries = tr->GetEntries();
    auto iEvent = nEntries; iEvent = 0;

    if ( INIT_EVENT != 0 ) printf("WARNING [TestMode] Entry starting from %d\n", INIT_EVENT);
    std::cout << "n entries : " << nEntries << std::endl;
    if ( TEST_MODE ) nEntries = nEntries>10000 ? 10000 : nEntries; // for test mode
    for(iEvent = INIT_EVENT; iEvent< nEntries; ++iEvent){
        tr->GetEntry(iEvent);


        if(iEvent%100000==0){cout<<"Events completed: "<<iEvent<<endl;}
        TLorentzVector recoPho;
        TLorentzVector genPho;
        vector<TLorentzVector> SelPhoton;
        vector<int> SelPhotonIdx;
        vector<TLorentzVector> GenPhoton;
        vector<TLorentzVector> SelJet;
        vector<int> SelJetIdx;
        vector<double> MyPhotonMVA;
        vector<double> SelPhoton_pfChargedIsoPFPV;
        vector<double> SelPhoton_sieie;
        vector<double> SelPhoton_hoe;
        vector<double> SelPhoton_pfChargedIsoWorstVtx;


        vector<TLorentzVector> SelPhotonALL;
        vector<int> SelPhotonIdxALL;
        vector<double> SS_var_photon_esEffSigmaRR;
        vector<double> SS_var_photon_energyRaw;
        vector<double> SS_var_photon_esEnergyOverRawE;
        vector<double> SS_var_photon_etaWidth;
        vector<double> SS_var_photon_hoe;
        vector<double> SS_var_photon_phiWidth;
        vector<double> SS_var_photon_r9;
        vector<double> SS_var_photon_s4;
        vector<double> SS_var_photon_sieie;
        vector<double> SS_var_photon_sieip;
        vector<double> SS_var_photon_rho;
        vector<double> SS_var_photon_eta;

        vector<double> MyPhotonMVA_MC_no_calib;
        for(int ij=0; ij< nPhoton; ++ij)
        {
            if (!isSignal ) if ( HLT_Photon200 == 0 ) continue;

            if(isSignal == true && nGenIsolatedPhoton < 1) continue;
            if(abs(Photon_eta[ij])>2.5) continue;
            if(Photon_pixelSeed[ij]==1)continue;
            if(abs(Photon_eta[ij])>1.4442 && abs(Photon_eta[ij])<1.566) continue;


            if(Photon_pfChargedIsoWorstVtx[ij]>20) continue;
            if(Photon_pfChargedIsoPFPV[ij]>20) continue;
            if(Photon_hoe[ij]>0.05) continue;
            if(abs(Photon_eta[ij])<1.5&&Photon_sieie[ij]>0.015) continue;
            if(abs(Photon_eta[ij])>1.5&&Photon_sieie[ij]>0.04 ) continue;

            bool reco_photon_in_signalregion_or_datasideband = false;
            if (!isDataSideband ) // is signal region
            {
                if(abs(Photon_eta[ij])<1.5 && Photon_pfChargedIsoPFPV[ij]<1.7 && Photon_pfChargedIsoWorstVtx[ij]<10) reco_photon_in_signalregion_or_datasideband = true;
                if(abs(Photon_eta[ij])>1.5 && Photon_pfChargedIsoPFPV[ij]<1.5 && Photon_pfChargedIsoWorstVtx[ij]<10) reco_photon_in_signalregion_or_datasideband = true;
                //if ( reco_photon_in_signalregion_or_datasideband ) std::cout << "Accepting signal region photon at entry " << iEvent << " \n";
            }
            else  // is data sideband
            {
                if(abs(Photon_eta[ij])<1.5 && Photon_pfChargedIsoPFPV[ij]>7.0) reco_photon_in_signalregion_or_datasideband = true;
                if(abs(Photon_eta[ij])>1.5 && Photon_pfChargedIsoPFPV[ij]>7.0) reco_photon_in_signalregion_or_datasideband = true;
                //if ( reco_photon_in_signalregion_or_datasideband ) std::cout << "Accepting sideband region photon at entry " << iEvent << " \n";
            }



            if(Photon_pt[ij]>700 && Photon_pt[ij]<900 && Photon_seediEtaOriX[ij]+0==-21 && Photon_seediPhiOriY[ij]==260 && isEraG==true) continue; //Only for Era G
            //Applying the photon scales and smearing

            Float_t Photon_pt_nom = isData ?
                phoScaleMgr->EvaluatePt(Photon_pt[ij], Photon_eta[ij], Photon_r9[ij], Photon_seedGain[ij], run) :
                phoSmearMgr->EvaluatePt(Photon_pt[ij], Photon_eta[ij], Photon_r9[ij]);
            recoPho.SetPtEtaPhiM(Photon_pt_nom, Photon_eta[ij], Photon_phi[ij],0.);

            if(recoPho.Pt()<210) continue;
            //      std::cout<<"pass all pho selections\n";
            //cout<<Photon_pt_nom<<"	"<<Photon_pt[ij]<<endl;
            //recoPho.SetPtEtaPhiM(Photon_pt[ij], Photon_eta[ij], Photon_phi[ij], 0.);

            photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
            photon_energyRaw = Photon_energyRaw[ij];
            photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
            photon_etaWidth = Photon_etaWidth[ij];
            photon_hoe = Photon_hoe[ij];
            photon_phiWidth = Photon_phiWidth[ij];
            photon_r9 = Photon_r9[ij];
            photon_s4 = Photon_s4[ij];
            photon_sieie = Photon_sieie[ij];
            photon_sieip = Photon_sieip[ij];
            photon_rho = Rho_fixedGridRhoFastjetAll;
            photon_eta = Photon_eta[ij];

            // only reco_photon passing gen requirement would be recorded.
            // data: pass, gjet: pass if reco photon is gen-matched
            // QCD: if event exists gen-photon, pass it if reco photon is gen-matched
            // QCD: if no gen-photon in event, pass it
            bool reco_photon_is_gen_required = false;
            // this block selects source and apply SS corr
            if(isData==true || isOther==true){
                reco_photon_is_gen_required = true;
            }

            if(isSignal == true){

                for(int ik=0; ik< nGenIsolatedPhoton; ++ik){
                    genPho.SetPtEtaPhiM(GenIsolatedPhoton_pt[ik], GenIsolatedPhoton_eta[ik], GenIsolatedPhoton_phi[ik], GenIsolatedPhoton_mass[ik]);
                    if(recoPho.DeltaR(genPho)> 0.1) continue;
                    reco_photon_is_gen_required = true;
                    if ( reco_photon_in_signalregion_or_datasideband )
                        GenPhoton.push_back(genPho);

                    if ( reco_photon_in_signalregion_or_datasideband )
                    {
                        if(abs(Photon_eta[ij])<1.5)
                        {MyPhotonMVA_MC_no_calib.push_back(reader_barrel->EvaluateMVA("BDT"));}
                        else
                        {MyPhotonMVA_MC_no_calib.push_back(reader_endcap->EvaluateMVA("BDT"));}
                        // not calibrated MVA calculation end

                        if(abs(Photon_eta[ij])<1.5){ // barrel SS corr
                            photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
                            photon_energyRaw = Photon_energyRaw[ij];
                            photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
                            photon_etaWidth = Photon_etaWidth[ij];
                            if ( is_problematic_SS_corr_ )
                                photon_hoe = Photon_hoe[ij];
                            else
                                photon_hoe = SSCORR_ONLY_SIEIE ? Photon_hoe[ij] : grDataInv_b[0]->Eval(grMC_b[0]->Eval(Photon_hoe[ij]));
                            photon_phiWidth = Photon_phiWidth[ij];
                            photon_r9 = Photon_r9[ij];
                            photon_s4 = Photon_s4[ij];
                            photon_sieie = grDataInv_b[1]->Eval(grMC_b[1]->Eval(Photon_sieie[ij]));
                            photon_sieip = Photon_sieip[ij];
                            photon_rho = Rho_fixedGridRhoFastjetAll;
                            photon_eta = Photon_eta[ij];
                        } // end of barrel SS corr
                        else{ // endcap SS corr
                            photon_esEnergyOverRawE = SSCORR_ONLY_SIEIE ? Photon_esEnergyOverRawE[ij] : grDataInv_e[2]->Eval(grMC_e[2]->Eval(Photon_esEnergyOverRawE[ij]));
                            photon_etaWidth         = SSCORR_ONLY_SIEIE ? Photon_etaWidth[ij] : grDataInv_e[3]->Eval(grMC_e[3]->Eval(Photon_etaWidth[ij]));
                            if ( is_problematic_SS_corr_ )
                            {
                                photon_hoe = Photon_hoe[ij];
                                photon_esEffSigmaRR     = Photon_esEffSigmaRR[ij];
                                photon_energyRaw        = Photon_energyRaw[ij];
                                photon_phiWidth         = Photon_phiWidth[ij];
                            }
                            else
                            {
                                photon_hoe              = SSCORR_ONLY_SIEIE ? Photon_hoe[ij]          : grDataInv_e[4]->Eval(grMC_e[4]->Eval(Photon_hoe[ij]));
                                photon_esEffSigmaRR     = SSCORR_ONLY_SIEIE ? Photon_esEffSigmaRR[ij] : grDataInv_e[0]->Eval(grMC_e[0]->Eval(Photon_esEffSigmaRR[ij]));
                                photon_energyRaw        = SSCORR_ONLY_SIEIE ? Photon_energyRaw[ij]    : grDataInv_e[1]->Eval(grMC_e[1]->Eval(Photon_energyRaw[ij]));
                                photon_phiWidth         = SSCORR_ONLY_SIEIE ? Photon_phiWidth[ij]     : grDataInv_e[5]->Eval(grMC_e[5]->Eval(Photon_phiWidth[ij]));
                            }
                            photon_r9               = SSCORR_ONLY_SIEIE ? Photon_r9[ij]    : grDataInv_e[6]->Eval(grMC_e[6]->Eval(Photon_r9[ij]));
                            photon_s4               = SSCORR_ONLY_SIEIE ? Photon_s4[ij]    : grDataInv_e[7]->Eval(grMC_e[7]->Eval(Photon_s4[ij]));
                            photon_sieie            = grDataInv_e[8]->Eval(grMC_e[8]->Eval(Photon_sieie[ij]));
                            photon_sieip            = SSCORR_ONLY_SIEIE ? Photon_sieip[ij] : grDataInv_e[9]->Eval(grMC_e[9]->Eval(Photon_sieip[ij]));
                            photon_rho              = Rho_fixedGridRhoFastjetAll;
                            photon_eta              = Photon_eta[ij];
                        } // end of endcap SS corr
                        /* orig block
                           if(abs(Photon_eta[ij])<1.5){ // barrel SS corr
                           photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
                           photon_energyRaw = Photon_energyRaw[ij];
                           photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
                           photon_etaWidth = Photon_etaWidth[ij];
                           photon_hoe = grDataInv_b[0]->Eval(grMC_b[0]->Eval(Photon_hoe[ij]));
                           photon_phiWidth = Photon_phiWidth[ij];
                           photon_r9 = Photon_r9[ij];
                           photon_s4 = Photon_s4[ij];
                           photon_sieie = grDataInv_b[1]->Eval(grMC_b[1]->Eval(Photon_sieie[ij]));
                           photon_sieip = Photon_sieip[ij];
                           photon_rho = Rho_fixedGridRhoFastjetAll;
                           photon_eta = Photon_eta[ij];
                           } // end of barrel SS corr
                           else{ // endcap SS corr
                           photon_esEffSigmaRR     = grDataInv_e[0]->Eval(grMC_e[0]->Eval(Photon_esEffSigmaRR[ij]));
                           photon_energyRaw        = grDataInv_e[1]->Eval(grMC_e[1]->Eval(Photon_energyRaw[ij]));
                           photon_esEnergyOverRawE = grDataInv_e[2]->Eval(grMC_e[2]->Eval(Photon_esEnergyOverRawE[ij]));
                           photon_etaWidth         = grDataInv_e[3]->Eval(grMC_e[3]->Eval(Photon_etaWidth[ij]));
                           photon_hoe              = grDataInv_e[4]->Eval(grMC_e[4]->Eval(Photon_hoe[ij]));
                           photon_phiWidth         = grDataInv_e[5]->Eval(grMC_e[5]->Eval(Photon_phiWidth[ij]));
                           photon_r9               = grDataInv_e[6]->Eval(grMC_e[6]->Eval(Photon_r9[ij]));
                           photon_s4               = grDataInv_e[7]->Eval(grMC_e[7]->Eval(Photon_s4[ij]));
                           photon_sieie            = grDataInv_e[8]->Eval(grMC_e[8]->Eval(Photon_sieie[ij]));
                           photon_sieip            = grDataInv_e[9]->Eval(grMC_e[9]->Eval(Photon_sieip[ij]));
                           photon_rho              = Rho_fixedGridRhoFastjetAll;
                           photon_eta              = Photon_eta[ij];
                           } // end of endcap SS corr
                           orig block */
                    }

                    break;
                } // end of nGenIsolatedPhoton
            } // end of isSignal

            // if ( isQCD ) 
            //     if ( Photon_genPartIdx[ij] < 0 ) reco_photon_is_gen_required = true;
            if ( isQCD )// Record di-jet event in QCD sample.
            {
                reco_photon_is_gen_required = true; // by default, set it to TRUE
                TLorentzVector gen_photon;
                for(int ik=0; ik< nGenIsolatedPhoton; ++ik) {
                    gen_photon.SetPtEtaPhiM(GenIsolatedPhoton_pt[ik], GenIsolatedPhoton_eta[ik], GenIsolatedPhoton_phi[ik], GenIsolatedPhoton_mass[ik]);
                    if(recoPho.DeltaR(gen_photon) < 0.1) { reco_photon_is_gen_required = false; break; }
                    // However, once this reco photon matched with gen_photon, set flag to FALSE to reject such event
                }
            }

            if ( reco_photon_is_gen_required )
            {
                SelPhotonALL.push_back(recoPho);
                SelPhotonIdxALL.push_back(ij);

                if ( reco_photon_in_signalregion_or_datasideband )
                {
                    if(abs(Photon_eta[ij])<1.44)
                    {MyPhotonMVA.push_back(reader_barrel->EvaluateMVA("BDT"));}
                    else
                    {MyPhotonMVA.push_back(reader_endcap->EvaluateMVA("BDT"));}
                    if (!isSignal ) MyPhotonMVA_MC_no_calib.push_back(0);

                    SelPhoton.push_back(recoPho);
                    SelPhotonIdx.push_back(ij);
                    SelPhoton_pfChargedIsoPFPV.push_back(Photon_pfChargedIsoPFPV[ij]);
                    SelPhoton_sieie.push_back(Photon_sieie[ij]);
                    SelPhoton_hoe.push_back(Photon_hoe[ij]);
                    SelPhoton_pfChargedIsoWorstVtx.push_back(Photon_pfChargedIsoWorstVtx[ij]);

                    SS_var_photon_esEffSigmaRR    .push_back(photon_esEffSigmaRR    );
                    SS_var_photon_energyRaw       .push_back(photon_energyRaw       );
                    SS_var_photon_esEnergyOverRawE.push_back(photon_esEnergyOverRawE);
                    SS_var_photon_etaWidth        .push_back(photon_etaWidth        );
                    SS_var_photon_hoe             .push_back(photon_hoe             );
                    SS_var_photon_phiWidth        .push_back(photon_phiWidth        );
                    SS_var_photon_r9              .push_back(photon_r9              );
                    SS_var_photon_s4              .push_back(photon_s4              );
                    SS_var_photon_sieie           .push_back(photon_sieie           );
                    SS_var_photon_sieip           .push_back(photon_sieip           );
                    SS_var_photon_rho             .push_back(photon_rho             );
                    SS_var_photon_eta             .push_back(photon_eta             );
                }
            } // end of reco_photon_is_gen_required
        } // loop for ij ( index of isolated photon )
        //    std::cout<<"Passing SelPhoton size\n";


        int selected_jet_idx_all = -1;
        bool event_containing_jet_failing_vetomap = false;
        for(int ij=0; ij<nJet; ++ij){
            //Applying the JEC
            Float_t jet_pt_raw = (1-Jet_rawFactor[ij])*Jet_pt[ij];
            Float_t jet_mass_raw = (1-Jet_rawFactor[ij])*Jet_mass[ij];
            Float_t jet_eta_raw = Jet_eta[ij];
            Float_t jet_phi_raw = Jet_phi[ij];

            // Float_t jet_raw_jec_sf_L2 = jec_sf_L2->evaluate({jet_eta_raw,jet_pt_raw});
            // Float_t jet_raw_jec_sf_L3 = jec_sf_L3->evaluate({jet_eta_raw,jet_pt_raw*jet_raw_jec_sf_L2});	   
            // Float_t jet_raw_sf_L23   = jec_sf_L23->evaluate({jet_eta_raw,jet_pt_raw*jet_raw_jec_sf_L2*jet_raw_jec_sf_L3});

            // jet_raw4v.SetPtEtaPhiM(jet_pt_raw, jet_eta_raw, jet_phi_raw, jet_mass_raw);
            // jet_corr4v = jet_raw4v*(jet_raw_jec_sf_L2*jet_raw_jec_sf_L3*jet_raw_sf_L23);

            TLorentzVector jet_raw4v;
            jet_raw4v.SetPtEtaPhiM(jet_pt_raw, jet_eta_raw, jet_phi_raw, jet_mass_raw);

            TLorentzVector jet_corr4v = jecjer_corr->JEC_Corrected(jet_raw4v);

            if (!isData )
            { // apply JER
                Float_t ptscale = 1;
                Float_t factor = jet_jerc_corr->evaluate({jet_corr4v.Eta(), jet_corr4v.Pt(), "nom"});
                Float_t res = jet_jerc_reso->evaluate({jet_corr4v.Eta(), jet_corr4v.Pt(), Rho_fixedGridRhoFastjetAll});
                bool isSmeared = false;

                int genjet_idx = Jet_genJetIdx[ij];
                if ( genjet_idx >= 0 )
                { // if reco jet matched with gen jet
                    double ptratio = jet_corr4v.Pt()/GenJet_pt[genjet_idx];
                    ptscale = max(0.0, ptratio + factor*(1 - ptratio));
                    isSmeared = true;	
                }

                // If that didn't work, use Gaussian smearing with a reproducible seed
                if(!isSmeared && factor > 1)
                {
                    TRandom3 JERrand;

                    JERrand.SetSeed(abs(static_cast<int>(jet_corr4v.Phi()*1e4)));
                    ptscale = max(0.0, 1.0 + JERrand.Gaus(0,res)*sqrt(factor*factor - 1.0)); 
                }

                Float_t jecjet_pt = jet_corr4v.Pt();
                Float_t jecjet_eta = jet_corr4v.Eta();
                Float_t jecjet_phi = jet_corr4v.Phi();
                Float_t jecjet_mass = jet_corr4v.M();
                jet_corr4v.SetPtEtaPhiM(jecjet_pt, jecjet_eta, jecjet_phi, jecjet_mass);
            } // apply JER ended

            //Checking Jet veto
            double 	jet_in_vetomap = cset_veto->evaluate({"jetvetomap", jet_corr4v.Eta(), jet_corr4v.Phi()});
            if ( abs(jet_in_vetomap) > 0 && jet_corr4v.Pt()>15 && Jet_jetId[ij]==6 && (Jet_neEmEF[ij]+Jet_chEmEF[ij])<0.9 && (Jet_PFMuonOverlapped->at(ij)==false) )
            { event_containing_jet_failing_vetomap = true; break; } // once there exists a jet failing vetomap, reject this event

            //std::cout << "calibrated jet pt is " << jet_corr4v.Pt() << " and orig jet pt is " << jet_raw4v.Pt() << std::endl;
            if ( jet_corr4v.Pt()<25 ) continue;
            if ( abs(jet_corr4v.Eta())>2.5 ) continue;
            if ( int(Jet_jetId[ij])!=6 ) continue; // tight jet ID

            if ( SelPhoton.size()>0 )
                if ( jet_corr4v.DeltaR(SelPhoton[0])>0.4 )
                { SelJet.push_back(jet_corr4v); SelJetIdx.push_back(ij); }

            // find a good photon and a good jet matching. (Only first matching jet selected)
            if ( SelPhotonALL.size()>0 )
                if ( jet_corr4v.DeltaR(SelPhotonALL[0])>0.4 && selected_jet_idx_all < 0 )
                    selected_jet_idx_all = ij;

        } // end of ij < nJet
        //  std::cout<<"Passing SelJet size\n";

        bool fill_histo = selected_jet_idx_all < 0 ? false : true;

        if ( fill_histo )
        {
            double evt_weight = 1;
            if ( isData==false )
            {
                double pileup_weight = h_pu_nom->GetBinContent(h_pu_nom->FindBin(Pileup_nPU));
                evt_weight = genWeight*normWgt*pileup_weight*GetPhotonSF(SelPhotonALL[0].Pt(), SelPhotonALL[0].Eta(), "nom")*GetTriggerSF(SelPhotonALL[0].Pt(), SelPhotonALL[0].Eta(), "nom");
            }
            // start filling histogram without signal region cut
            float abseta = fabs(Photon_eta[ SelPhotonIdxALL[0] ]);
            float _PNetB               = Jet_btagPNetB[ selected_jet_idx_all ];
            float _PNetCvsB            = Jet_btagPNetCvB[ selected_jet_idx_all ];
            float _PNetCvsL            = Jet_btagPNetCvL[ selected_jet_idx_all ];
            float _PNetQvsG            = Jet_btagPNetQvG[ selected_jet_idx_all ];
            float _ParTB               = Jet_btagRobustParTAK4B[ selected_jet_idx_all ];
            float _ParTCvsB            = Jet_btagRobustParTAK4CvB[ selected_jet_idx_all ];
            float _ParTCvsL            = Jet_btagRobustParTAK4CvL[ selected_jet_idx_all ];
            float _ParTQvsG            = Jet_btagRobustParTAK4QG[ selected_jet_idx_all ];
            float _DeepFlavourB        = Jet_btagDeepFlavB[ selected_jet_idx_all ];
            float _DeepFlavourCvsB     = Jet_btagDeepFlavCvB[ selected_jet_idx_all ];
            float _DeepFlavourCvsL     = Jet_btagDeepFlavCvL[ selected_jet_idx_all ];
            float _DeepFlavourQvsG     = Jet_btagDeepFlavQG[ selected_jet_idx_all ];
            if ( abseta < 1.5 ) // barrel
            {
                b_PhoPt->Fill(SelPhotonALL[0].Pt() , evt_weight);
                b_PNetB            ->Fill( _PNetB          , evt_weight);
                b_PNetCvsB         ->Fill( _PNetCvsB       , evt_weight);
                b_PNetCvsL         ->Fill( _PNetCvsL       , evt_weight);
                b_PNetQvsG         ->Fill( _PNetQvsG       , evt_weight);
                b_ParTB            ->Fill( _ParTB          , evt_weight);
                b_ParTCvsB         ->Fill( _ParTCvsB       , evt_weight);
                b_ParTCvsL         ->Fill( _ParTCvsL       , evt_weight);
                b_ParTQvsG         ->Fill( _ParTQvsG       , evt_weight);
                b_DeepFlavourB     ->Fill( _DeepFlavourB   , evt_weight);
                b_DeepFlavourCvsB  ->Fill( _DeepFlavourCvsB, evt_weight);
                b_DeepFlavourCvsL  ->Fill( _DeepFlavourCvsL, evt_weight);
                b_DeepFlavourQvsG  ->Fill( _DeepFlavourQvsG, evt_weight);
                b_PhoEta           ->Fill( Photon_eta[ SelPhotonIdxALL[0] ], evt_weight); 
                b_PhoPhi           ->Fill( Photon_phi[ SelPhotonIdxALL[0] ], evt_weight); 
                b_pfChIso          ->Fill( Photon_pfChargedIsoPFPV[ SelPhotonIdxALL[0] ], evt_weight); 
                b_pfChIsoWorstVtx  ->Fill( Photon_pfChargedIsoWorstVtx[ SelPhotonIdxALL[0] ], evt_weight); 
            }
            else // endcap
            {
                e_PhoPt->Fill(SelPhotonALL[0].Pt() , evt_weight);
                e_PNetB            ->Fill( _PNetB          , evt_weight);
                e_PNetCvsB         ->Fill( _PNetCvsB       , evt_weight);
                e_PNetCvsL         ->Fill( _PNetCvsL       , evt_weight);
                e_PNetQvsG         ->Fill( _PNetQvsG       , evt_weight);
                e_ParTB            ->Fill( _ParTB          , evt_weight);
                e_ParTCvsB         ->Fill( _ParTCvsB       , evt_weight);
                e_ParTCvsL         ->Fill( _ParTCvsL       , evt_weight);
                e_ParTQvsG         ->Fill( _ParTQvsG       , evt_weight);
                e_DeepFlavourB     ->Fill( _DeepFlavourB   , evt_weight);
                e_DeepFlavourCvsB  ->Fill( _DeepFlavourCvsB, evt_weight);
                e_DeepFlavourCvsL  ->Fill( _DeepFlavourCvsL, evt_weight);
                e_DeepFlavourQvsG  ->Fill( _DeepFlavourQvsG, evt_weight);
                e_PhoEta           ->Fill( Photon_eta[ SelPhotonIdxALL[0] ], evt_weight); 
                e_PhoPhi           ->Fill( Photon_phi[ SelPhotonIdxALL[0] ], evt_weight); 
                e_pfChIso          ->Fill( Photon_pfChargedIsoPFPV[ SelPhotonIdxALL[0] ], evt_weight); 
                e_pfChIsoWorstVtx  ->Fill( Photon_pfChargedIsoWorstVtx[ SelPhotonIdxALL[0] ], evt_weight); 
            }
        } // end of fill_histo


        // sel photon is filtered by reco_photon_in_signalregion_or_datasideband

        //std::cout << "SelPhoton size " << SelPhoton.size() << ", Seljet size " << SelJet.size() << std::endl;
        if ( event_containing_jet_failing_vetomap ) continue; // totally skip this event
        if(SelPhoton.size() == 0) continue;
        if(SelJet.size() == 0) continue;

        double wgt_gen = 1;
        if ( isData )
            wgt = 1;
        else
        {
            double puWgt = h_pu_nom->GetBinContent(h_pu_nom->FindBin(Pileup_nPU));
            double phoSF = GetPhotonSF(SelPhoton[0].Pt(), SelPhoton[0].Eta(), "nom");
            double trigSF = GetTriggerSF(SelPhoton[0].Pt(), SelPhoton[0].Eta(), "nom");
            wgt = genWeight*normWgt*puWgt*phoSF*trigSF;
            wgt_gen = genWeight * normWgt;

            int jet_flav = int(Jet_hadronFlavour[SelJetIdx[0]]);
            auto cset_WPbL = jet_flav == 0 ? cset_WPbL_lightQ : cset_WPbL_heavyQ;
            o_wgt_WPbL_central = cset_WPbL->evaluate( {"central","L", jet_flav, fabs(SelJet[0].Eta()), SelJet[0].Pt()} );
            // central, down, down_bfragmentation, down_correlated, down_jes, down_pileup,
            // down_statistic, down_type3, down_uncorrelated, up, up_bfragmentation, up_correlated, up_jes,
            // up_pileup, up_statistic, up_type3, up_uncorrelated

            o_wgt_WPcShape_central = cset_ctag_reshape->evaluate( {"central",jet_flav, 
                                      Jet_btagRobustParTAK4CvL[ SelJetIdx[0] ],
                                      Jet_btagRobustParTAK4CvB[ SelJetIdx[0] ]} );
//      │ Values: central, down_Extrap, down_Interp, down_LHEScaleWeight_muF, down_LHEScaleWeight_muR, │
//      │ down_PSWeightFSR, down_PSWeightISR, down_PUWeight, down_Stat, down_XSec_BRUnc_DYJets_b,      │
//      │ down_XSec_BRUnc_DYJets_c, down_XSec_BRUnc_WJets_c, down_jer, down_jesTotal, up_Extrap,       │
//      │ up_Interp, up_LHEScaleWeight_muF, up_LHEScaleWeight_muR, up_PSWeightFSR, up_PSWeightISR,     │
//      │ up_PUWeight, up_Stat, up_XSec_BRUnc_DYJets_b, up_XSec_BRUnc_DYJets_c, up_XSec_BRUnc_WJets_c, │
//      │ up_jer, up_jesTotal                                                                          │

        }


        photonPt = SelPhoton[0].Pt();
        photonEta = SelPhoton[0].Eta();
        photonPhi = SelPhoton[0].Phi();
        photonMVA = MyPhotonMVA[0];

        photonMVAorig = isSignal ? MyPhotonMVA_MC_no_calib[0] : 0.;

        photonPfChargedIsoWorstVtx = SelPhoton_pfChargedIsoWorstVtx[0];
        photonPfChargedIsoPFPV = SelPhoton_pfChargedIsoPFPV[0];
        photonSieie = SelPhoton_sieie[0];
        photonHoE = SelPhoton_hoe[0];
        jetPt = SelJet[0].Pt();
        jetEta = SelJet[0].Eta();
        jetPhi = SelJet[0].Phi();
        jet_nSV = int(Jet_nSVs[ SelJetIdx[0] ]);
        njet = nJet;
        //for ( int ijet = 0; ijet < nJet; ++ijet )
        //{ std::cout << ijet << "th jet contains nSV = " << int(Jet_nSVs[ijet]) << std::endl; }
        //printf("[Jet_nSV] %d. Orig = %c and uint = %u\n", jet_nSV, Jet_nSVs[SelJetIdx[0]], Jet_nSVs[SelJetIdx[0]]);
        //std::cout << "[cout] Jet_nSV = " << jet_nSV << " and orig = " <<  Jet_nSVs[SelJetIdx[0]] << std::endl; break;

        jet_SVmass = NO_SVMASS;
        jet_SVpt = 0;
        jet_SVdr = -1;
        jet_SVntracks = 0;
        if ( jet_nSV > 0 )
        { // use deltaR matching to SV because jet PT is very huge.
            int SV_idx = -1;

            float SV_min_dr = 999;
            for ( int iSV = 0 ; iSV < nSV; ++iSV )
            {
                float sv_dr = myDeltaR(SelJet[0].Eta(),SelJet[0].Phi(), SV_eta[iSV], SV_phi[iSV]);
                if ( sv_dr < SV_min_dr )
                { SV_min_dr = sv_dr; SV_idx = iSV; }
            }

            if ( SV_min_dr < 0.3 ) // only record the deltaR < 0.3 events
            {
                jet_SVmass = SV_mass[SV_idx];
                jet_SVpt = SV_pt[SV_idx];
                jet_SVdr = SV_min_dr;
                jet_SVntracks = int(SV_ntracks[SV_idx]);
            }
        }

        gjetZmass = (SelJet[0]+SelPhoton[0]).M();
        MET = PuppiMET_pt;
        genPhotonPt  = GenPhoton.size()>0 ? GenPhoton[0].Pt()  : -999;
        genPhotonEta = GenPhoton.size()>0 ? GenPhoton[0].Eta() : -999;
        genPhotonPhi = GenPhoton.size()>0 ? GenPhoton[0].Phi() : -999;

        int genjet_idx = Jet_genJetIdx[SelJetIdx[0]];
        bool has_gen_get = isData ? false : true;
        if ( has_gen_get )
            has_gen_get = SelJetIdx[0] >= 0 ? true : false; 
        if ( has_gen_get )
            has_gen_get = Jet_genJetIdx[SelJetIdx[0]] >= 0 ? true : false; 

        selected_jet_idx = SelJetIdx[0];
        //isHadFlvr_C = has_gen_get ? int(GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ])==4 : false;
        //isHadFlvr_B = has_gen_get ? int(GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ])==5 : false;
        //isHadFlvr_L = has_gen_get ? int(GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ])==0 : false;
        isHadFlvr_C = int(Jet_hadronFlavour[ SelJetIdx[0] ])==4;
        isHadFlvr_B = int(Jet_hadronFlavour[ SelJetIdx[0] ])==5;
        isHadFlvr_L = int(Jet_hadronFlavour[ SelJetIdx[0] ])==0;
        jetHadFlvr = isData ? -1 : int(Jet_hadronFlavour[SelJetIdx[0]]);
        jetPrtFlvr = isData ? -1 : int(Jet_partonFlavour[SelJetIdx[0]]);
        genjetHadFlvr = has_gen_get ? int(GenJet_hadronFlavour[ Jet_genJetIdx[SelJetIdx[0]] ]) : -1;
        genjetPrtFlvr = has_gen_get ? int(GenJet_partonFlavour[ Jet_genJetIdx[SelJetIdx[0]] ]) : -1;

        PNetB               = Jet_btagPNetB[ SelJetIdx[0] ];
        PNetCvsB            = Jet_btagPNetCvB[ SelJetIdx[0] ];
        PNetCvsL            = Jet_btagPNetCvL[ SelJetIdx[0] ];
        PNetQvsG            = Jet_btagPNetQvG[ SelJetIdx[0] ];
        ParTB               = Jet_btagRobustParTAK4B[ SelJetIdx[0] ];
        ParTCvsB            = Jet_btagRobustParTAK4CvB[ SelJetIdx[0] ];
        ParTCvsL            = Jet_btagRobustParTAK4CvL[ SelJetIdx[0] ];
        ParTQvsG            = Jet_btagRobustParTAK4QG[ SelJetIdx[0] ];
        DeepFlavourB        = Jet_btagDeepFlavB[ SelJetIdx[0] ];
        DeepFlavourCvsB     = Jet_btagDeepFlavCvB[ SelJetIdx[0] ];
        DeepFlavourCvsL     = Jet_btagDeepFlavCvL[ SelJetIdx[0] ];
        DeepFlavourQvsG     = Jet_btagDeepFlavQG[ SelJetIdx[0] ];

        passWPbL = ParTB > WPbLValue;
        passWPbM = ParTB > WPbMValue;
        passWPbT = ParTB > WPbTValue;

        tree->Fill();

        // fill shower shape distribution, only in signal region or data sideband
        if ( abs(SelPhoton[0].Eta()) < 1.5 )
        {
            b_mva              ->Fill( MyPhotonMVA[0], wgt);
            b_HoverE           ->Fill( SS_var_photon_hoe[0],  wgt); 
            b_sieie            ->Fill( SS_var_photon_sieie[0], wgt); 
            b_sieip            ->Fill( SS_var_photon_sieip[0], wgt); 
            b_r9               ->Fill( SS_var_photon_r9[0], wgt); 
            b_s4               ->Fill( SS_var_photon_s4[0], wgt); 
            b_phiWidth         ->Fill( SS_var_photon_phiWidth[0], wgt); 
            b_etaWidth         ->Fill( SS_var_photon_etaWidth[0], wgt); 
            b_esEnergyOverRawE ->Fill( SS_var_photon_esEnergyOverRawE[0], wgt); 
            b_energyRaw        ->Fill( SS_var_photon_energyRaw[0], wgt); 
            b_esEffSigmaRR     ->Fill( SS_var_photon_esEffSigmaRR[0], wgt); 

            if ( isSignal)
            {
                borig_mva              ->Fill( MyPhotonMVA_MC_no_calib[0], wgt); 
                borig_HoverE           ->Fill( Photon_hoe             [ SelPhotonIdx[0] ], wgt); 
                borig_sieie            ->Fill( Photon_sieie           [ SelPhotonIdx[0] ], wgt); 
                borig_sieip            ->Fill( Photon_sieip           [ SelPhotonIdx[0] ], wgt); 
                borig_r9               ->Fill( Photon_r9              [ SelPhotonIdx[0] ], wgt); 
                borig_s4               ->Fill( Photon_s4              [ SelPhotonIdx[0] ], wgt); 
                borig_phiWidth         ->Fill( Photon_phiWidth        [ SelPhotonIdx[0] ], wgt); 
                borig_etaWidth         ->Fill( Photon_etaWidth        [ SelPhotonIdx[0] ], wgt); 
                borig_esEnergyOverRawE ->Fill( Photon_esEnergyOverRawE[ SelPhotonIdx[0] ], wgt); 
                borig_energyRaw        ->Fill( Photon_energyRaw       [ SelPhotonIdx[0] ], wgt); 
                borig_esEffSigmaRR     ->Fill( Photon_esEffSigmaRR    [ SelPhotonIdx[0] ], wgt); 
            }
        } else {
            e_mva              ->Fill( MyPhotonMVA[0], wgt);
            e_HoverE           ->Fill( SS_var_photon_hoe[0],  wgt); 
            e_sieie            ->Fill( SS_var_photon_sieie[0], wgt); 
            e_sieip            ->Fill( SS_var_photon_sieip[0], wgt); 
            e_r9               ->Fill( SS_var_photon_r9[0], wgt); 
            e_s4               ->Fill( SS_var_photon_s4[0], wgt); 
            e_phiWidth         ->Fill( SS_var_photon_phiWidth[0], wgt); 
            e_etaWidth         ->Fill( SS_var_photon_etaWidth[0], wgt); 
            e_esEnergyOverRawE ->Fill( SS_var_photon_esEnergyOverRawE[0], wgt); 
            e_energyRaw        ->Fill( SS_var_photon_energyRaw[0], wgt); 
            e_esEffSigmaRR     ->Fill( SS_var_photon_esEffSigmaRR[0], wgt); 

            if ( isSignal)
            {
                eorig_mva              ->Fill( MyPhotonMVA_MC_no_calib[0], wgt); 
                eorig_HoverE           ->Fill( Photon_hoe             [ SelPhotonIdx[0] ], wgt); 
                eorig_sieie            ->Fill( Photon_sieie           [ SelPhotonIdx[0] ], wgt); 
                eorig_sieip            ->Fill( Photon_sieip           [ SelPhotonIdx[0] ], wgt); 
                eorig_r9               ->Fill( Photon_r9              [ SelPhotonIdx[0] ], wgt); 
                eorig_s4               ->Fill( Photon_s4              [ SelPhotonIdx[0] ], wgt); 
                eorig_phiWidth         ->Fill( Photon_phiWidth        [ SelPhotonIdx[0] ], wgt); 
                eorig_etaWidth         ->Fill( Photon_etaWidth        [ SelPhotonIdx[0] ], wgt); 
                eorig_esEnergyOverRawE ->Fill( Photon_esEnergyOverRawE[ SelPhotonIdx[0] ], wgt); 
                eorig_energyRaw        ->Fill( Photon_energyRaw       [ SelPhotonIdx[0] ], wgt); 
                eorig_esEffSigmaRR     ->Fill( Photon_esEffSigmaRR    [ SelPhotonIdx[0] ], wgt); 
            }
        }
        // fill shower shape distribution, only in signal region or data sideband end





        if ( GenPhoton.size() > 0 ) {
            if(abs(SelPhoton[0].Eta())<=1.5 && abs(SelJet[0].Eta())<1.5){
                if(GenPhoton[0].Pt()>=210){
                    //cout<<SelPhoton[0].Pt()<<endl;
                    h_pt_reco[0]->Fill(SelPhoton[0].Pt(),wgt);
                    h_pt_gen[0]->Fill(GenPhoton[0].Pt(),wgt_gen);
                }
                if(GenPhoton[0].Pt()<210){h_reco_pt[0]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[0]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[1]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[1]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[2]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[2]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[3]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[3]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[4]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[4]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[5]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[5]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[6]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[6]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[7]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[7]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[8]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[8]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[9]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[9]->Fill(GenPhoton[0].Pt(),wgt);}
            }
            if(abs(SelPhoton[0].Eta())<=1.5 && abs(SelJet[0].Eta())>1.5 && abs(SelJet[0].Eta())<2.5){
                if(GenPhoton[0].Pt()>=210){
                    h_pt_reco[1]->Fill(SelPhoton[0].Pt(),wgt);
                    h_pt_gen[1]->Fill(GenPhoton[0].Pt(),wgt_gen);
                }
                if(GenPhoton[0].Pt()<210){h_reco_pt[10]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[10]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[11]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[11]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[12]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[12]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[13]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[13]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[14]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[14]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[15]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[15]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[16]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[16]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[17]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[17]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[18]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[18]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[19]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[19]->Fill(GenPhoton[0].Pt(),wgt);}
            }
            if(abs(SelPhoton[0].Eta())>1.5 && abs(SelPhoton[0].Eta())<=2.5 && abs(SelJet[0].Eta())<1.5){
                if(GenPhoton[0].Pt()>=210){
                    h_pt_reco[2]->Fill(SelPhoton[0].Pt(),wgt);
                    h_pt_gen[2]->Fill(GenPhoton[0].Pt(),wgt_gen);
                }
                if(GenPhoton[0].Pt()<210){h_reco_pt[20]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[20]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[21]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[21]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[22]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[22]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[23]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[23]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[24]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[24]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[25]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[25]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[26]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[26]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[27]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[27]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[28]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[28]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[29]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[29]->Fill(GenPhoton[0].Pt(),wgt);}
            }
            if(abs(SelPhoton[0].Eta())>1.5 && abs(SelPhoton[0].Eta())<=2.5 && abs(SelJet[0].Eta())>1.5 && abs(SelJet[0].Eta())<=2.5){
                if(GenPhoton[0].Pt()>=210){
                    h_pt_reco[3]->Fill(SelPhoton[0].Pt(),wgt);
                    h_pt_gen[3]->Fill(GenPhoton[0].Pt(),wgt_gen);
                }
                if(GenPhoton[0].Pt()<210){h_reco_pt[30]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[30]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=210 && GenPhoton[0].Pt()<230){h_reco_pt[31]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[31]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=230 && GenPhoton[0].Pt()<250){h_reco_pt[32]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[32]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=250 && GenPhoton[0].Pt()<300){h_reco_pt[33]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[33]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=300 && GenPhoton[0].Pt()<400){h_reco_pt[34]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[34]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=400 && GenPhoton[0].Pt()<500){h_reco_pt[35]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[35]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=500 && GenPhoton[0].Pt()<600){h_reco_pt[36]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[36]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=600 && GenPhoton[0].Pt()<800){h_reco_pt[37]->Fill(SelPhoton[0].Pt(),wgt); h_gen_pt[37]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=800 && GenPhoton[0].Pt()<1000){h_reco_pt[38]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[38]->Fill(GenPhoton[0].Pt(),wgt);}
                if(GenPhoton[0].Pt()>=1000 && GenPhoton[0].Pt()<1500){h_reco_pt[39]->Fill(SelPhoton[0].Pt(),wgt);h_gen_pt[39]->Fill(GenPhoton[0].Pt(),wgt);}
            }
        } // if gen photon size > 0

    }
    BUG("HI end of loop\n");

    for(int j=0;j<NBINSX_gen;++j){
        for(int i=0;i<NBINSX;++i){
            h_corrMatrix[0]->SetBinContent(i+1,j,h_reco_pt[j]->GetBinContent(i+1)/h_gen_pt[j]->Integral());
            h_corrMatrix[0]->SetBinError(i+1,j,h_reco_pt[j]->GetBinError(i+1)/h_gen_pt[j]->Integral());

            h_corrMatrix[1]->SetBinContent(i+1,j,h_reco_pt[j+NBINSX_gen]->GetBinContent(i+1)/h_gen_pt[j+NBINSX_gen]->Integral());
            h_corrMatrix[1]->SetBinError(i+1,j,h_reco_pt[j+NBINSX_gen]->GetBinError(i+1)/h_gen_pt[j+NBINSX_gen]->Integral());

            h_corrMatrix[2]->SetBinContent(i+1,j,h_reco_pt[j+2*NBINSX_gen]->GetBinContent(i+1)/h_gen_pt[j+2*NBINSX_gen]->Integral());
            h_corrMatrix[2]->SetBinError(i+1,j,h_reco_pt[j+2*NBINSX_gen]->GetBinError(i+1)/h_gen_pt[j+2*NBINSX_gen]->Integral());

            h_corrMatrix[3]->SetBinContent(i+1,j,h_reco_pt[j+3*NBINSX_gen]->GetBinContent(i+1)/h_gen_pt[j+3*NBINSX_gen]->Integral());
            h_corrMatrix[3]->SetBinError(i+1,j,h_reco_pt[j+3*NBINSX_gen]->GetBinError(i+1)/h_gen_pt[j+3*NBINSX_gen]->Integral());
        }
    }
    for(int i=1;i<NBINSX+1;++i){
        h_corrMatrix[0]->SetBinContent(i,0,0);
        h_corrMatrix[0]->SetBinError(i,0,0);
        h_corrMatrix[1]->SetBinContent(i,0,0);
        h_corrMatrix[1]->SetBinError(i,0,0);
        h_corrMatrix[2]->SetBinContent(i,0,0);
        h_corrMatrix[2]->SetBinError(i,0,0);
        h_corrMatrix[3]->SetBinContent(i,0,0);
        h_corrMatrix[3]->SetBinError(i,0,0);
    }
    fout->cd();
    for(int i=0; i<4; ++i){
        h_pt_reco[i]->Write();
        h_pt_gen[i]->Write();
        h_corrMatrix[i]->Write();
    }
    for(int i=0; i<40; ++i){
        h_reco_pt[i]->Write();
        h_gen_pt[i]->Write();
    }

    b_mva->Write();
    b_PhoPt->Write();
    b_PNetB           ->Write();
    b_PNetCvsB        ->Write();
    b_PNetCvsL        ->Write();
    b_PNetQvsG        ->Write();
    b_ParTB           ->Write();
    b_ParTCvsB        ->Write();
    b_ParTCvsL        ->Write();
    b_ParTQvsG        ->Write();
    b_DeepFlavourB    ->Write();
    b_DeepFlavourCvsB ->Write();
    b_DeepFlavourCvsL ->Write();
    b_DeepFlavourQvsG ->Write();
    b_PhoEta          ->Write();
    b_PhoPhi          ->Write();
    b_HoverE          ->Write();
    b_sieie           ->Write();
    b_sieip           ->Write();
    b_pfChIso         ->Write();
    b_pfChIsoWorstVtx ->Write();
    b_r9              ->Write();
    b_s4              ->Write();
    b_phiWidth        ->Write();
    b_etaWidth        ->Write();
    b_esEnergyOverRawE->Write();
    b_energyRaw       ->Write();
    b_esEffSigmaRR    ->Write();

    if ( isSignal)
    {
        borig_mva              ->Write();
        borig_HoverE           ->Write();
        borig_sieie            ->Write();
        borig_sieip            ->Write();
        borig_r9               ->Write();
        borig_s4               ->Write();
        borig_phiWidth         ->Write();
        borig_etaWidth         ->Write();
        borig_esEnergyOverRawE ->Write();
        borig_energyRaw        ->Write();
        borig_esEffSigmaRR     ->Write();
    }

    e_mva->Write();
    e_PhoPt->Write();
    e_PNetB           ->Write();
    e_PNetCvsB        ->Write();
    e_PNetCvsL        ->Write();
    e_PNetQvsG        ->Write();
    e_ParTB           ->Write();
    e_ParTCvsB        ->Write();
    e_ParTCvsL        ->Write();
    e_ParTQvsG        ->Write();
    e_DeepFlavourB    ->Write();
    e_DeepFlavourCvsB ->Write();
    e_DeepFlavourCvsL ->Write();
    e_DeepFlavourQvsG ->Write();
    e_PhoEta          ->Write();
    e_PhoPhi          ->Write();
    e_HoverE          ->Write();
    e_sieie           ->Write();
    e_sieip           ->Write();
    e_pfChIso         ->Write();
    e_pfChIsoWorstVtx ->Write();
    e_r9              ->Write();
    e_s4              ->Write();
    e_phiWidth        ->Write();
    e_etaWidth        ->Write();
    e_esEnergyOverRawE->Write();
    e_energyRaw       ->Write();
    e_esEffSigmaRR    ->Write();
    if ( isSignal)
    {
        eorig_mva              ->Write();
        eorig_HoverE           ->Write();
        eorig_sieie            ->Write();
        eorig_sieip            ->Write();
        eorig_r9               ->Write();
        eorig_s4               ->Write();
        eorig_phiWidth         ->Write();
        eorig_etaWidth         ->Write();
        eorig_esEnergyOverRawE ->Write();
        eorig_energyRaw        ->Write();
        eorig_esEffSigmaRR     ->Write();
    }

    tree->Write();
    delete fout;
}
