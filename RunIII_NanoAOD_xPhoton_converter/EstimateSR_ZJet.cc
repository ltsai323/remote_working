#include <ROOT/RDataFrame.hxx>
#include <TLorentzVector.h>
#include <ROOT/RVec.hxx>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <iostream>
#include "MyDYjet_ZmmSelections.h"
#include "MyJetSelections.h"
#include "MyGeneralFuncs.h"
#include "MyImportedFileMgr.h"
#include "TSystemDirectory.h"

#include "extlib/JEC_JER_Corrector.h"

using namespace ROOT;
using namespace ROOT::VecOps;


std::vector<std::string> list_of_dir (const std::string& thePATH) {
    if ( thePATH.find(".root") != std::string::npos ) return std::vector<std::string>({ thePATH });

        // Get the list of ROOT files in a directory
    TSystemDirectory dir( thePATH.c_str(), thePATH.c_str() );
    TList* files = dir.GetListOfFiles();
    std::vector<std::string> fileList;

    if (files) {
        TIter next(files);
        TObject* obj;
        while ((obj = next())) {
            std::string fileName = obj->GetName();
            if (fileName.find(".root") != std::string::npos) {
                fileList.push_back( thePATH + "/" +fileName);
            }
        }
    }

    return fileList;
}

template <typename T>
T access_array_by_idx(const RVec<T>& theARRAY, Short_t idx)
{
  try {
    // not to raise error if -1 put. (means nothing)
    if ( idx<0 ) return -1;
    if (idx >= theARRAY.size()) {
    //if (idx < 0 || idx >= theARRAY.size()) {
      throw std::out_of_range(
          Form("[OutOfRange] Accessing array(size %zu) with index(%d) is out of bounds!", theARRAY.size(), idx)
          );
    }
    return theARRAY[idx];  // Safe access
  } 
  catch (const std::out_of_range &e) {
    std::cerr << "Error: " << e.what() << std::endl;
    exit(EXIT_FAILURE);
  }
}
Short_t MuonMother_iterative_search_mother_genpartidx(Short_t genIDX, const RVec<int>& genPARTpid, const RVec<Short_t>& genMOMidx)
{
  Short_t currentPID = access_array_by_idx(genPARTpid, genIDX);  // Safe access
  if ( abs(currentPID) != 13 ) return genIDX;
  Short_t motherIDX = access_array_by_idx(genMOMidx, genIDX);
  return MuonMother_iterative_search_mother_genpartidx( motherIDX, genPARTpid, genMOMidx );
}
RVec<Short_t> MuonMother_GenIdx(
  const RVec<Short_t>& muonGENidx,
  const RVec<Int_t>  & genPARTpid,
  const RVec<Short_t>& genMOMidx)
{
  if ( muonGENidx.size() == 0 ) return RVec<Short_t>();
  RVec<Short_t> muon_mother_idx;
  for ( auto muon_gen_idx : muonGENidx )
    if (muon_gen_idx>0)
      muon_mother_idx.push_back( MuonMother_iterative_search_mother_genpartidx(muon_gen_idx,genPARTpid,genMOMidx) );
    else
      muon_mother_idx.push_back( -1 );
  return muon_mother_idx;
}


  





















// Function to define new columns for the DataFrame
ROOT::RDF::RNode reconstruct_zjet_in_data(ROOT::RDF::RNode df, std::shared_ptr<JEC_JER_Corrector> jecjer_corr) {
    return df
      //------------------------------- muon selections -------------------------------
      .Define("muoncomb_2indices", "Combinations(Muon_pt,2)")
      .Define("mupair_mu0idxs", "muoncomb_2indices[0]")
      .Define("mupair_mu1idxs", "muoncomb_2indices[1]")

      .Define("mupair_mu0eta","Take(Muon_eta,mupair_mu0idxs)")
      .Define("mupair_mu1eta","Take(Muon_eta,mupair_mu1idxs)")
      .Define("mupair_abs_eta", "abs(mupair_mu0eta-mupair_mu1eta)")
      .Define("mupair_cut_abs_eta", "mupair_abs_eta < 2.4") // cut

      .Define("mupair_mu0charge", "Take(Muon_charge,mupair_mu0idxs)")
      .Define("mupair_mu1charge", "Take(Muon_charge,mupair_mu1idxs)")
      .Define("mupair_charge_product", "mupair_mu0charge*mupair_mu1charge")
      .Define("mupair_cut_charge_product", "mupair_charge_product == -1") // cut

      .Define("mupair_mu0pt", "Take(Muon_pt,mupair_mu0idxs)")
      .Define("mupair_mu1pt", "Take(Muon_pt,mupair_mu1idxs)")
      .Define("mupair_cut_pt", "mupair_mu0pt>25 && mupair_mu1pt>20") // cut
      
      .Define("mupair_mu0tightID", "Take(Muon_tightId,mupair_mu0idxs)")
      .Define("mupair_mu1tightID", "Take(Muon_tightId,mupair_mu1idxs)")
      .Define("mupair_cut_tightID", "mupair_mu0tightID==1&&mupair_mu1tightID==1") // cut


      .Define("mupair_mu0pfIsoID", "Take(Muon_pfIsoId,mupair_mu0idxs)")
      .Define("mupair_mu1pfIsoID", "Take(Muon_pfIsoId,mupair_mu1idxs)")
      .Define("mupair_cut_pfIsoID", "mupair_mu0pfIsoID>=4 && mupair_mu1pfIsoID>=4") // 4 tight, 5 very tight, 6 very very tight
      .Define("mupair_overallcut", "mupair_cut_abs_eta*mupair_cut_charge_product*mupair_cut_pt*mupair_cut_tightID*mupair_cut_pfIsoID")
      .Define("mupair_selected_idx",
          [](const RVec<Int_t>& cuts) {
            auto indices_from_descent_sorted_array = StableArgsort(cuts, [](Int_t a,Int_t b){return a>b;});
            Short_t found_idx = indices_from_descent_sorted_array[0];
            Int_t cut = cuts[found_idx];
            if ( cut == 0 ) found_idx = -1; // set it to none
            return found_idx;
            }, {"mupair_overallcut"})
      .Filter("mupair_selected_idx>=0") // cut entry found no muon pair

      .Define("muon_cand0idx", "mupair_mu0idxs[mupair_selected_idx]")
      .Define("muon_cand1idx", "mupair_mu1idxs[mupair_selected_idx]")


      //-------------------------------  Z  selections -------------------------------
      .Define("mucand0P4", "ROOT::Math::PtEtaPhiMVector(Muon_pt[muon_cand0idx],Muon_eta[muon_cand0idx],Muon_phi[muon_cand0idx],Muon_mass[muon_cand0idx])")
      .Define("mucand1P4", "ROOT::Math::PtEtaPhiMVector(Muon_pt[muon_cand1idx],Muon_eta[muon_cand1idx],Muon_phi[muon_cand1idx],Muon_mass[muon_cand1idx])")
      .Define("recZP4", "mucand0P4+mucand1P4")
      .Define("recZmass", "recZP4.M()")
      .Define("recZpt"  , "recZP4.Pt()")
      .Filter("recZmass>(90-30) && recZmass<(90+30)") // cut Z mass window
      .Filter("recZpt>15") // cut Z pt

      //------------------------------- jet selections -------------------------------
      .Define("Jet_P4", GeneralFuncs::ConstructJetP4, {"Jet_pt", "Jet_eta", "Jet_phi", "Jet_mass", "nJet"})
      .Define("Jet_JECCorrP4" , [jecjer_corr](const RVec<TLorentzVector>& pARRAY) { RVec<TLorentzVector> o; for ( const auto& p : pARRAY ) o.push_back(jecjer_corr->JEC_Corrected(p)); return o; }, {"Jet_P4"})
      // Redefine the jet pt and mass according to JEC correction. Such as the preselection using updated information
      .Redefine("Jet_pt"  , [&](const RVec<TLorentzVector>& pARRAY) { RVec<Float_t> o; for ( const auto& p: pARRAY ) o.push_back(p.Pt()); return o; }, {"Jet_JECCorrP4"})
      .Redefine("Jet_mass", [&](const RVec<TLorentzVector>& pARRAY) { RVec<Float_t> o; for ( const auto& p: pARRAY ) o.push_back(p.M ()); return o; }, {"Jet_JECCorrP4"})
      .Define("Jet_selectionpased", JetSelections::JetPreselection().Data() ) // So preselection uses JEC corrected pt instead of original pt


      .Define("Jet_selectionpased_pt", "Jet_selectionpased*Jet_pt")
      .Define("muon0_related_jetIdx", "Muon_jetIdx[muon_cand0idx]")
      .Define("muon1_related_jetIdx", "Muon_jetIdx[muon_cand1idx]")
      .Define("Jet_selidx", GeneralFuncs::GetLeadingJetIdx_ignore2indices, {"Jet_selectionpased_pt","muon0_related_jetIdx", "muon1_related_jetIdx"})
      .Filter("Jet_selidx>=0 && Jet_selidx<nJet") // reject no preselected jet situation (-1)

      .Define("selrawjet", "Jet_P4[Jet_selidx]")
      .Define("seljet",    "Jet_JECCorrP4[Jet_selidx]")
      ;
}

// Function to define output variables
ROOT::RDF::RNode define_data_variables(ROOT::RDF::RNode df_selected) {
    return  df_selected
      .Define("recoZ_pt"      , "recZP4.Pt()")
      .Define("recoZ_eta"     , "recZP4.Eta()")
      .Define("recoZ_phi"     , "recZP4.Phi()")
      .Define("recoZ_mass"    , "recZP4.M()")
      .Define("recoMuon0_pt"  , "Muon_pt[muon_cand0idx]")
      .Define("recoMuon0_eta" , "Muon_eta[muon_cand0idx]")
      .Define("recoMuon0_phi" , "Muon_phi[muon_cand0idx]")
      .Define("recoMuon1_pt"  , "Muon_pt[muon_cand1idx]")
      .Define("recoMuon1_eta" , "Muon_eta[muon_cand1idx]")
      .Define("recoMuon1_phi" , "Muon_phi[muon_cand1idx]")
      .Define("dR_mu0_jet"    , "ROOT::Math::VectorUtil::DeltaR(mucand0P4,seljet)")
      .Define("dR_mu1_jet"    , "ROOT::Math::VectorUtil::DeltaR(mucand1P4,seljet)")

      .Define("recoJet_btagPNetB",                 "Jet_btagPNetB[Jet_selidx]")
      .Define("recoJet_btagPNetCvB",               "Jet_btagPNetCvB[Jet_selidx]")
      .Define("recoJet_btagPNetCvL",               "Jet_btagPNetCvL[Jet_selidx]")
      .Define("recoJet_btagPNetQvG",               "Jet_btagPNetQvG[Jet_selidx]")
      .Define("recoJet_btagRobustParTAK4B",        "Jet_btagRobustParTAK4B[Jet_selidx]")
      .Define("recoJet_btagRobustParTAK4CvB",      "Jet_btagRobustParTAK4CvB[Jet_selidx]")
      .Define("recoJet_btagRobustParTAK4CvL",      "Jet_btagRobustParTAK4CvL[Jet_selidx]")
      .Define("recoJet_btagRobustParTAK4QG",       "Jet_btagRobustParTAK4QG[Jet_selidx]")
      .Define("recoJet_btagDeepFlavB",             "Jet_btagDeepFlavB[Jet_selidx]")
      .Define("recoJet_btagDeepFlavCvB",           "Jet_btagDeepFlavCvB[Jet_selidx]")
      .Define("recoJet_btagDeepFlavCvL",           "Jet_btagDeepFlavCvL[Jet_selidx]")
      .Define("recoJet_btagDeepFlavQG",            "Jet_btagDeepFlavQG[Jet_selidx]")
      .Define("recoJet_nConstituents",             "Jet_nConstituents[Jet_selidx]")
      .Define("recoJet_PNetRegPtRawCorr",          "Jet_PNetRegPtRawCorr[Jet_selidx]")
      .Define("recoJet_PNetRegPtRawCorrNeutrino",  "Jet_PNetRegPtRawCorrNeutrino[Jet_selidx]")
      .Define("recoJet_PNetRegPtRawRes",           "Jet_PNetRegPtRawRes[Jet_selidx]")
      .Define("recoJet_chEmEF",                    "Jet_chEmEF[Jet_selidx]")
      .Define("recoJet_chHEF",                     "Jet_chHEF[Jet_selidx]")
      .Define("recoJet_hfsigmaEtaEta",             "Jet_hfsigmaEtaEta[Jet_selidx]")
      .Define("recoJet_hfsigmaPhiPhi",             "Jet_hfsigmaPhiPhi[Jet_selidx]")
      .Define("recoJet_rawFactor",                 "Jet_rawFactor[Jet_selidx]")

      .Define("recoJet_pt",                        "seljet.Pt()")
      .Define("recoJet_eta",                       "seljet.Eta()")
      .Define("recoJet_phi",                       "seljet.Phi()")
      .Define("recoJet_mass",                      "seljet.M()")
      .Define("recoJet_rawpt",                     "selrawjet.Pt()")
      .Define("recoJet_rawmass",                   "selrawjet.M()")
      ;
}

int mainfunc_Data_2(const char* inFILE, const char* outFILE, const std::string& dataERA) {
    std::vector<std::string> infiles = list_of_dir(inFILE);

    ROOT::RDataFrame df("Events", infiles);
    
    // Load JEC/JER corrections
    std::map<std::string, const char*> usedfiles = ImportedFileMgr::Factory("relative");
    std::shared_ptr<JEC_JER_Corrector>  jecjer_corr = nullptr;

    if ( dataERA == "2022EE_RunE" )
      jecjer_corr = std::make_shared<JEC_JER_Corrector>( usedfiles["JEC"],
          "Summer22EE_22Sep2023_RunE_V2_DATA_L2Relative_AK4PFPuppi",
          "Summer22EE_22Sep2023_RunE_V2_DATA_L3Absolute_AK4PFPuppi",
          "Summer22EE_22Sep2023_RunE_V2_DATA_L2L3Residual_AK4PFPuppi");

    if ( dataERA == "2022EE_RunF" )
      jecjer_corr = std::make_shared<JEC_JER_Corrector>( usedfiles["JEC"],
          "Summer22EE_22Sep2023_RunF_V2_DATA_L2Relative_AK4PFPuppi",
          "Summer22EE_22Sep2023_RunF_V2_DATA_L3Absolute_AK4PFPuppi",
          "Summer22EE_22Sep2023_RunF_V2_DATA_L2L3Residual_AK4PFPuppi");

    if ( dataERA == "2022EE_RunG" )
      jecjer_corr = std::make_shared<JEC_JER_Corrector>( usedfiles["JEC"],
          "Summer22EE_22Sep2023_RunG_V2_DATA_L2Relative_AK4PFPuppi",
          "Summer22EE_22Sep2023_RunG_V2_DATA_L3Absolute_AK4PFPuppi",
          "Summer22EE_22Sep2023_RunG_V2_DATA_L2L3Residual_AK4PFPuppi");
    if ( jecjer_corr == nullptr ) throw std::invalid_argument( Form("[InvalidDataEra] input data '%s' is invalid\n", dataERA.c_str()) );


    // Process DataFrame
    auto df_processed = reconstruct_zjet_in_data(df, jecjer_corr)
      .Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==1"); // apply HLT
    auto df_final = define_data_variables(df_processed);

    // Save output
    df_final.Snapshot("Events", outFILE, {
        "recoZ_pt"      ,
        "recoZ_eta"     ,
        "recoZ_phi"     ,
        "recoZ_mass"    ,

        "recoMuon0_pt"  ,
        "recoMuon0_eta" ,
        "recoMuon0_phi" ,
        "recoMuon1_pt"  ,
        "recoMuon1_eta" ,
        "recoMuon1_phi" ,
        "dR_mu0_jet"    ,
        "dR_mu1_jet"    ,



        "recoJet_btagPNetB",                 
        "recoJet_btagPNetCvB",               
        "recoJet_btagPNetCvL",               
        "recoJet_btagPNetQvG",               
        "recoJet_btagRobustParTAK4B",        
        "recoJet_btagRobustParTAK4CvB",      
        "recoJet_btagRobustParTAK4CvL",      
        "recoJet_btagRobustParTAK4QG",       
        "recoJet_btagDeepFlavB",             
        "recoJet_btagDeepFlavCvB",           
        "recoJet_btagDeepFlavCvL",           
        "recoJet_btagDeepFlavQG",            
        "recoJet_nConstituents",             
        "recoJet_PNetRegPtRawCorr",          
        "recoJet_PNetRegPtRawCorrNeutrino",  
        "recoJet_PNetRegPtRawRes",           
        "recoJet_chEmEF",                    
        "recoJet_chHEF",                     
        "recoJet_hfsigmaEtaEta",             
        "recoJet_hfsigmaPhiPhi",             
        "recoJet_rawFactor",                 

        "recoJet_pt",      // JEC corrected pt
        "recoJet_eta",    
        "recoJet_phi",    
        "recoJet_mass",    // JEC corrected mass
        "recoJet_rawpt",  
        //"recoJet_raweta", 
        //"recoJet_rawphi", 
        "recoJet_rawmass",

        "PV_npvsGood",
        "PV_npvs",

        });

    return 0;
}
// processCROSSSECTION uses fb. If you got a pb, *1000
int mainfunc_MC_2(const char* inFILE, const char* outFILE, const double integratedLUMINOSITY, const double processCROSSSECTION) {
    std::vector<std::string> infiles = list_of_dir(inFILE);

    TH1* h_load = nullptr;
    std::cout << "input folder : " << inFILE << std::endl;
    std::cout << "infiles size  = " << infiles.size() << std::endl;
    for ( auto infile : infiles )
    {
      std::cout << "used file : " << infile << std::endl;
      std::cout << infile << std::endl;
      auto intfile = TFile::Open(infile.c_str());
      auto h_load_ = (TH1*) intfile->Get("totWgt");
      if ( h_load == nullptr ) { h_load = (TH1*) h_load_->Clone(); std::cout << 0 << std::endl; h_load->SetDirectory(0); }
      else { h_load->Add(h_load_); std::cout << 1 << std::endl; }
      std::cout << "totEvt " << h_load->GetBinContent(2) << " ---- newEvt " << h_load_->GetBinContent(2) << std::endl;

      intfile->Close();
    }
    std::cout << "totEvt " << h_load->GetBinContent(2) << std::endl;
    std::cout << "hiiii \n";

    //auto intfile = TFile::Open(inFILE);
    //auto h_load = (TH1*) intfile->Get("totWgt");
    const double integrated_gen_weight = h_load->GetBinContent(1);
    const double total_gen_entries = h_load->GetBinContent(2);

    // Create RDataFrame for the "Events" tree
    ROOT::RDataFrame df("Events", infiles);
    const double entries_tot = df.Count().GetValue();
    std::map<std::string,const char*> usedfiles = ImportedFileMgr::Factory("relative");
    std::shared_ptr<JEC_JER_Corrector>  jecjer_corr = std::make_shared<JEC_JER_Corrector>( usedfiles["JEC"],
          "Summer22EE_22Sep2023_V2_MC_L2Relative_AK4PFPuppi",
          "Summer22EE_22Sep2023_V2_MC_L3Absolute_AK4PFPuppi",
          "Summer22EE_22Sep2023_V2_MC_L2L3Residual_AK4PFPuppi");

    std::shared_ptr<GeneralFuncs::PileupWgtMgr> pileup_mgr = std::make_shared<GeneralFuncs::PileupWgtMgr>( usedfiles["PileUp"] );



    // Define the new column "jetP4" based on input jet variables
    //auto take_float = [](const RVec<Float_t>& val, Short_t idx){ return access_array_by_idx(val,idx); };
    auto take_float = [](const RVec<Float_t>& val, Short_t idx){ return access_array_by_idx(val,idx); };
    auto take_short = [](const RVec<Short_t>& val, Short_t idx){ return access_array_by_idx(val,idx); };
    auto take_uchar = [](const RVec<UChar_t>& val, Short_t idx){ return access_array_by_idx(val,idx); };
    auto take_int   = [](const RVec<Int_t  >& val, Short_t idx){ return access_array_by_idx(val,idx); };

    auto df_processed = reconstruct_zjet_in_data(df, jecjer_corr)
      .Define("muon_mom_genidx", MuonMother_GenIdx, { "Muon_genPartIdx", "GenPart_pdgId", "GenPart_genPartIdxMother" })
      //.Define("muon_mom_pid", "Take(GenPart_pdgId,muon_mom_genidx, -1)") // return an array with default value -1 // only for ROOT version > 6.34
      .Define("muon_mom_pid", [](const RVec<Int_t>& vals, const RVec<Short_t>& idxs) { RVec<Int_t> o; for ( auto idx : idxs ) { o.push_back(access_array_by_idx(vals,idx)); } return o; }, {"GenPart_pdgId","muon_mom_genidx"} )
      .Define("mucand0mompid", "muon_mom_pid[muon_cand0idx]")
      .Define("mucand1mompid", "muon_mom_pid[muon_cand1idx]")
      .Define("is_gen_level_Z", "mucand0mompid==23 && mucand1mompid==23");

    auto df_final = define_data_variables(df_processed)
      .Define("weight_pu", [pileup_mgr](Int_t npu) { return Double_t( pileup_mgr->GetWeight(npu) ); }, {"Pileup_nPU"})
      .Define("integrated_gen_weight", [&]() { return Double_t(integrated_gen_weight); })
      .Define("cross_section", [&]() { return Double_t(processCROSSSECTION); })
      .Define("integrated_luminosity", [&]() { return Double_t(integratedLUMINOSITY); })
      .Define("event_weight", "cross_section * integrated_luminosity * weight_pu * genWeight / integrated_gen_weight")

      .Define("isMatchedZ"    , "is_gen_level_Z")
      .Define("recoJet_partonFlavour",             "Jet_partonFlavour[Jet_selidx]")
      .Define("recoJet_hadronFlavour",             "Jet_hadronFlavour[Jet_selidx]")

      .Define("genjet_idx",                    "Jet_genJetIdx[Jet_selidx]")
      .Define("genjet_pt",   take_float, {"GenJet_pt",    "genjet_idx"})
      .Define("genjet_eta",  take_float, {"GenJet_eta",   "genjet_idx"})
      .Define("genjet_phi",  take_float, {"GenJet_phi",   "genjet_idx"})
      .Define("genjet_mass", take_float, {"GenJet_mass",  "genjet_idx"})
      .Define("genjet_partonFlavour", take_short, {"GenJet_partonFlavour",  "genjet_idx"})
      .Define("genjet_hadronFlavour", take_uchar, {"GenJet_hadronFlavour",  "genjet_idx"})

      ;
    df_final.Snapshot("Events", outFILE, {
        "recoZ_pt"      ,
        "recoZ_eta"     ,
        "recoZ_phi"     ,
        "recoZ_mass"    ,
        "isMatchedZ"    ,

        "recoMuon0_pt"  ,
        "recoMuon0_eta" ,
        "recoMuon0_phi" ,
        "recoMuon1_pt"  ,
        "recoMuon1_eta" ,
        "recoMuon1_phi" ,
        "dR_mu0_jet"    ,
        "dR_mu1_jet"    ,


        "genjet_pt",  
        "genjet_eta", 
        "genjet_phi", 
        "genjet_mass",
        "genjet_partonFlavour",
        "genjet_hadronFlavour",

        "recoJet_btagPNetB",                 
        "recoJet_btagPNetCvB",               
        "recoJet_btagPNetCvL",               
        "recoJet_btagPNetQvG",               
        "recoJet_btagRobustParTAK4B",        
        "recoJet_btagRobustParTAK4CvB",      
        "recoJet_btagRobustParTAK4CvL",      
        "recoJet_btagRobustParTAK4QG",       
        "recoJet_btagDeepFlavB",             
        "recoJet_btagDeepFlavCvB",           
        "recoJet_btagDeepFlavCvL",           
        "recoJet_btagDeepFlavQG",            
        "recoJet_partonFlavour",             
        "recoJet_hadronFlavour",             
        "recoJet_nConstituents",             
        "recoJet_PNetRegPtRawCorr",          
        "recoJet_PNetRegPtRawCorrNeutrino",  
        "recoJet_PNetRegPtRawRes",           
        "recoJet_chEmEF",                    
        "recoJet_chHEF",                     
        "recoJet_hfsigmaEtaEta",             
        "recoJet_hfsigmaPhiPhi",             
        "recoJet_rawFactor",                 

        "recoJet_pt",      // JEC corrected pt
        "recoJet_eta",    
        "recoJet_phi",    
        "recoJet_mass",    // JEC corrected mass
        "recoJet_rawpt",  
        //"recoJet_raweta", 
        //"recoJet_rawphi", 
        "recoJet_rawmass",

        "weight_pu",
        "genWeight",
        "integrated_gen_weight",
        "cross_section",
        "integrated_luminosity",
        "event_weight",

        "PV_npvsGood",
        "PV_npvs",
        });



    auto out_file = new TFile(outFILE, "UPDATE");
    out_file->cd();

    auto hEFF_muonSel = new TH1F("effMuonSel", "MuonSelectionEfficiency bin1:total bin2:pass filter", 2, 0., 2.);
    hEFF_muonSel->SetBinContent(1, entries_tot);
    //hEFF_muonSel->SetBinContent(2, entries_muonsel);
    hEFF_muonSel->Write();

    out_file->Close();

    
    return 0;
}

void invalid_dataera(const std::string& dataERA, const std::vector<std::string>& availableDATAERA) {
    std::string available_dataera = "";
    for ( auto dataera : availableDATAERA )
        available_dataera += "\n  > '" + dataera + "'";

    throw std::invalid_argument(
        Form( "[InvalidDataEra] data era(%s) is rejected. The available options are %s\n",
          dataERA.c_str(), available_dataera.c_str() )
        );
}

int main(int argc, char** argv) {
    if (argc < 3+1) {
        std::cerr << Form("Usage %s <input_root_file> <output_root_file> <data_era>\n", argv[0]);
        return 1;
    }
    const char* fIN = argv[1];
    //const char* fOUT = argv[2];
    const char* fOUT = argv[2];
    // available data_era: "2022EERunE", "2022EERunF", "2022EERunG", "2022EE_MC"
    std::string dataERA = argv[3];
    const double lumi = 26.81; // fb-1

    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_PTLL40to100_1J"  ) return mainfunc_MC_2(fIN,fOUT,lumi, 477100.0);
    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_PTLL100to200_1J" ) return mainfunc_MC_2(fIN,fOUT,lumi, 44490.0);
    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_PTLL200to400_1J" ) return mainfunc_MC_2(fIN,fOUT,lumi, 3354.0);
    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_PTLL400to600_1J" ) return mainfunc_MC_2(fIN,fOUT,lumi, 117.2);
    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_PTLL600_1J"      ) return mainfunc_MC_2(fIN,fOUT,lumi, 13.99);

    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_0J"              ) return mainfunc_MC_2(fIN,fOUT,lumi, 5357.0 * 1000.);
    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_1J"              ) return mainfunc_MC_2(fIN,fOUT,lumi, 1010.0 * 1000.);
    if ( dataERA == "2022EE_DYto2L2Jets_MLL50_2J"              ) return mainfunc_MC_2(fIN,fOUT,lumi, 385.3  * 1000.);

    if ( dataERA == "2022EE_RunE" ) return mainfunc_Data_2(fIN,fOUT, dataERA);
    if ( dataERA == "2022EE_RunF" ) return mainfunc_Data_2(fIN,fOUT, dataERA);
    if ( dataERA == "2022EE_RunG" ) return mainfunc_Data_2(fIN,fOUT, dataERA);

    invalid_dataera( dataERA, {
            "2022EE_DYto2L2Jets_MLL50_PTLL40to100_1J"  ,
            "2022EE_DYto2L2Jets_MLL50_PTLL100to200_1J" ,
            "2022EE_DYto2L2Jets_MLL50_PTLL200to400_1J" ,
            "2022EE_DYto2L2Jets_MLL50_PTLL400to600_1J" ,
            "2022EE_DYto2L2Jets_MLL50_PTLL600_1J"      ,
            "2022EE_DYto2L2Jets_MLL50_0J",
            "2022EE_DYto2L2Jets_MLL50_1J",
            "2022EE_DYto2L2Jets_MLL50_2J",

            "2022EE_RunE",
            "2022EE_RunF",
            "2022EE_RunG",
            } );
    return 9;
}
